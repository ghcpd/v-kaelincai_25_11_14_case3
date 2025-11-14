from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List

import pytest
import requests
from playwright.sync_api import sync_playwright

from tests.utils.layout_metrics import evaluate_acceptance, summarize_metrics

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parent
SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"
LOG_DIR = PROJECT_ROOT / "logs"
RESULTS_DIR = PROJECT_ROOT / "results"
VARIANT = os.getenv("UI_VARIANT", "pre")
RESULTS_FILE = RESULTS_DIR / f"results_{VARIANT}.json"
LOG_FILE = LOG_DIR / f"log_{VARIANT}.txt"
TIME_FILE = RESULTS_DIR / f"time_{VARIANT}.txt"

for path in (SCREENSHOT_DIR, LOG_DIR, RESULTS_DIR):
    path.mkdir(parents=True, exist_ok=True)

with (WORKSPACE_ROOT / "test_data.json").open("r", encoding="utf-8") as handle:
    TEST_CASES: List[Dict] = json.load(handle)


def wait_for_server(url: str, timeout: float = 10.0) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(url, timeout=0.3)
            if response.ok:
                return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError("Server did not become ready in time")


@pytest.fixture(scope="session", autouse=True)
def server() -> None:
    env = os.environ.copy()
    env.setdefault("FLASK_ENV", "production")
    process = subprocess.Popen(
        [sys.executable, "src/app.py"],
        cwd=PROJECT_ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    wait_for_server("http://127.0.0.1:3000/health")
    yield
    process.terminate()
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()


def capture_case(page, case_id: str) -> Dict:
    page.goto(f"http://127.0.0.1:3000/?case={case_id}")
    page.wait_for_selector("[data-task-item]")
    page.wait_for_timeout(150)
    boxes = page.evaluate("window.__captureLayout && window.__captureLayout()")
    globals_payload = page.evaluate("window.__measureGlobal && window.__measureGlobal()") or {}
    if boxes is None:
        raise AssertionError("Layout capture did not return data")
    metrics = summarize_metrics(
        boxes,
        css_collisions=globals_payload.get("cssCollisions", 0),
        hover_latency=globals_payload.get("hoverLatency", 999),
        dom_snapshot=globals_payload.get("domSnapshot"),
    )
    verdict = evaluate_acceptance(metrics)
    return {
        "boxes": boxes,
        "metrics": metrics.__dict__,
        "verdict": verdict,
        "status": "pass" if verdict["overall"] else "fail",
        "dom_snapshot": globals_payload.get("domSnapshot"),
        "css_collisions": globals_payload.get("cssCollisions"),
    }


def test_before_ui_layout_and_metrics(server):
    start_time = time.time()
    entries: List[Dict] = []
    log_lines: List[str] = []

    previous_dom = None
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        for case in TEST_CASES:
            result = capture_case(page, case_id=case["id"])
            screenshot_path = SCREENSHOT_DIR / f"screenshot_{VARIANT}_{case['id']}.png"
            page.screenshot(path=str(screenshot_path))
            expected_status = case["expected"][VARIANT]
            dom_changed = result["dom_snapshot"] != previous_dom
            log_lines.append(
                f"case={case['id']} expected={expected_status} actual={result['status']} spacing_var={result['metrics']['spacing_variance']:.2f} css={result['css_collisions']} dom_changed={dom_changed}"
            )
            assert (
                result["status"] == expected_status
            ), f"Case {case['id']} expected {expected_status} got {result['status']}"
            entries.append(
                {
                    "id": case["id"],
                    "metrics": result["metrics"],
                    "verdict": result["verdict"],
                    "status": result["status"],
                    "dom_changed": dom_changed,
                }
            )
            previous_dom = result["dom_snapshot"]
        browser.close()

    if entries:
        avg_spacing = sum(item["metrics"]["spacing_variance"] for item in entries) / len(entries)
        avg_hover = sum(item["metrics"]["hover_latency"] for item in entries) / len(entries)
        total_misaligned = sum(item["metrics"]["misaligned_icons"] for item in entries)
    else:
        avg_spacing = avg_hover = 0.0
        total_misaligned = 0

    payload = {
        "variant": VARIANT,
        "summary": {
            "avg_spacing_variance": avg_spacing,
            "avg_hover_latency": avg_hover,
            "total_misaligned_icons": total_misaligned,
        },
        "cases": entries,
    }

    RESULTS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    LOG_FILE.write_text("\n".join(log_lines), encoding="utf-8")
    duration = time.time() - start_time
    TIME_FILE.write_text(f"{duration:.2f}", encoding="utf-8")
