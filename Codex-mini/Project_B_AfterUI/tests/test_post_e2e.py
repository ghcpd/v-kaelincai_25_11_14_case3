import json
import statistics
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT = ROOT / "screenshots" / "screenshot_post_1.png"
RESULTS_FILE = ROOT / "results" / "results_post.json"
LOG_FILE = ROOT / "logs" / "log_post.txt"
TIME_FILE = ROOT / "results" / "time_post.txt"
URL = "http://127.0.0.1:3000"

def analyze(page):
    cards = page.locator(".task-card")
    boxes = [handle.bounding_box() for handle in cards.element_handles()]
    icons = [handle.bounding_box() for handle in page.locator(".task-icon").element_handles()]
    spacing = []
    columns = {}
    for box in boxes:
        if not box:
            continue
        key = round(box["x"] / 220)
        if key not in columns:
            columns[key] = []
        columns[key].append(box)
    for col in columns.values():
        col.sort(key=lambda b: b["y"])
        for prev, curr in zip(col, col[1:]):
            spacing.append(round(curr["y"] - (prev["y"] + prev["height"]), 2))
    spacing_std = statistics.pstdev(spacing) if spacing else 0
    alignment = 0
    if icons:
        baseline = icons[0]["y"]
        alignment = sum(1 for icon in icons if abs(icon["y"] - baseline) > 2)
    hover_start = time.perf_counter()
    page.hover(".actions .secondary")
    hover_latency = (time.perf_counter() - hover_start) * 1000
    css_sample = page.evaluate("""
        () => {
            const card = document.querySelector('.task-card');
            if (!card) return {};
            const computed = getComputedStyle(card);
            return {
                padding: computed.padding,
                borderRadius: computed.borderRadius,
                gap: computed.gap,
                background: computed.background
            };
        }
    """)
    dom = page.content()
    return {
        "spacing_variance": round(spacing_std, 2),
        "misaligned_icons": alignment,
        "hover_latency_ms": round(hover_latency, 2),
        "css_sample": css_sample,
        "dom_hash": hash(dom) & 0xFFFFFFFF,
        "spacing_values": spacing,
        "dom_length": len(dom),
    }

def test_post_renders_clean_layout(server):
    start = time.time()
    with sync_playwright() as playground:
        browser = playground.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_selector(".task-card")
        metrics = analyze(page)
        SCREENSHOT.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(SCREENSHOT), full_page=True)
        browser.close()
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_FILE.write_text(json.dumps({"metrics": metrics}, indent=2), encoding="utf-8")
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("w", encoding="utf-8") as log:
        log.write(f"Metrics:\n")
        log.write(json.dumps(metrics, indent=2))
    TIME_FILE.write_text(f"{time.time() - start:.2f}\n", encoding="utf-8")
