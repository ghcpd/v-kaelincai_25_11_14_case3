import json
import statistics
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT = ROOT / "screenshots" / "screenshot_pre_1.png"
RESULTS_FILE = ROOT / "results" / "results_pre.json"
LOG_FILE = ROOT / "logs" / "log_pre.txt"
TIME_FILE = ROOT / "results" / "time_pre.txt"
URL = "http://127.0.0.1:3000"


def capture_metrics(page):
    boxes = []
    icons = []
    for element in page.locator(".task-card").element_handles():
        bb = element.bounding_box()
        if bb:
            boxes.append(bb)
    for icon in page.locator(".task-icon").element_handles():
        bb = icon.bounding_box()
        if bb:
            icons.append(bb)
    spacing_values = []
    for prev, curr in zip(boxes, boxes[1:]):
        bottom = prev["y"] + prev["height"]
        spacing = curr["y"] - bottom
        spacing_values.append(spacing)
    spacing_std = statistics.pstdev(spacing_values) if spacing_values else 0
    alignment = 0
    if icons:
        baseline = icons[0]["y"]
        alignment = sum(1 for icon in icons if abs(icon["y"] - baseline) > 3)
    hover_start = time.perf_counter()
    page.hover(".task-actions .primary")
    hover_end = time.perf_counter()
    hover_latency_ms = (hover_end - hover_start) * 1000
    css_sample = page.evaluate("""
        () => {
            const card = document.querySelector('.task-card');
            if (!card) return {};
            const style = getComputedStyle(card);
            return {
                padding: style.padding,
                margin: style.margin,
                gap: style.gap,
                background: style.background
            };
        }
    """)
    dom_snapshot = page.content()
    return {
        "spacing_deviation": round(spacing_std, 2),
        "misaligned_icons": alignment,
        "hover_latency_ms": round(hover_latency_ms, 2),
        "css_sample": css_sample,
        "dom_snapshot_length": len(dom_snapshot),
        "dom_snapshot": dom_snapshot[:800],
        "spacing_values": [round(v, 2) for v in spacing_values],
    }


def test_task_list_layout(server):
    start = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 800})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_selector(".task-card")
        metrics = capture_metrics(page)
        SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(SCREENSHOT), full_page=True)
        browser.close()
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(json.dumps({"metrics": metrics}, indent=2), encoding="utf-8")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as log:
        log.write(f"Metrics: {json.dumps(metrics)}\n")
    elapsed = time.time() - start
    TIME_FILE.write_text(f"{elapsed:.2f}\n", encoding="utf-8")
