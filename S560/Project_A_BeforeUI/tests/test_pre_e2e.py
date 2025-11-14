import subprocess
import time
import os
import signal
import json
import requests
from playwright.sync_api import sync_playwright
from layout_utils import compute_item_spacings, spacing_variance, icons_aligned, normalize_dom_text

ROOT = os.path.dirname(__file__)  # tests dir
PROJECT_ROOT = os.path.abspath(os.path.join(ROOT, '..'))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'src', 'static')

SERVER_CMD = ['python', os.path.join(PROJECT_ROOT, 'src', 'app.py')]


def wait_for_server(url='http://127.0.0.1:3000', timeout=10.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


def save_results(results, path):
    with open(path, 'w', encoding='utf8') as fh:
        json.dump(results, fh, indent=2)


def test_e2e_baseline_and_metrics(tmp_path):
    # Start server
    proc = subprocess.Popen(SERVER_CMD, cwd=PROJECT_ROOT)
    try:
        assert wait_for_server(), 'server did not start'
        start_time = time.time()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width":1280, "height":768})
            page.goto('http://127.0.0.1:3000')
            # interactions: hover first item
            items = page.query_selector_all('.task-item')
            assert len(items) >= 1
            first = items[0]
            start_hover = time.time()
            first.hover()
            # exercise dynamic mutation by using Add button if present
            add_btn = page.query_selector('.add-btn')
            if add_btn:
                add_btn.click()
                page.wait_for_timeout(250)
                items = page.query_selector_all('.task-item')
            hover_timeout = 0.1
            changed = False
            elapsed = 0
            while elapsed < hover_timeout:
                style = page.evaluate("(el)=>getComputedStyle(el).transform", first)
                if style and style != 'none':
                    changed = True
                    break
                time.sleep(0.005)
                elapsed = time.time() - start_hover
            hover_latency = elapsed if changed else None
            # collect bounding boxes
            bboxes = []
            icon_boxes = []
            for x in items:
                bb = x.bounding_box()
                if bb:
                    bboxes.append({k: float(v) for k,v in bb.items()})
                icon = x.query_selector('.icon')
                if icon:
                    ib = icon.bounding_box()
                    if ib:
                        icon_boxes.append({k: float(v) for k,v in ib.items()})
            spacings = compute_item_spacings(bboxes)
            sdev = spacing_variance(spacings)
            icons_ok = icons_aligned(icon_boxes, tolerance=6.0)
            normalized_titles = []
            for item in items:
                t = item.query_selector('.title')
                if t:
                    text = t.inner_text()
                else:
                    text = ''
                normalized_titles.append(normalize_dom_text(text))
            stop_time = time.time()
            # capture screenshot
            screenshot_path = os.path.join(PROJECT_ROOT, 'screenshots', 'screenshot_pre_1.png')
            page.screenshot(path=screenshot_path, full_page=True)
            results = {
                'timing': stop_time - start_time,
                'spacing_stddev': sdev,
                'spacing_samples': spacings,
                'icons_ok': icons_ok,
                'title_count': len(normalized_titles),
                'titles': normalized_titles,
            }
            save_results(results, os.path.join(PROJECT_ROOT, 'results', 'results_pre.json'))
            # Save additional logs
            with open(os.path.join(PROJECT_ROOT, 'logs', 'log_pre.txt'), 'w', encoding='utf8') as lh:
                lh.write('E2E test results:\n')
                lh.write(str(results))
            browser.close()
            # Baseline should NOT satisfy improvement criteria — we assert that baseline demonstrates the problem
            assert sdev >= 2.0, 'Baseline is too consistent — may be not a true baseline'
            assert icons_ok is False or icons_ok is None, 'Baseline unexpectedly has aligned icons'
            assert hover_latency is None, 'Baseline should not show hover feedback within 16ms, but it appears to' 
    finally:
        proc.terminate()
        proc.wait(timeout=5)
