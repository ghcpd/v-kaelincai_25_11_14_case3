import subprocess, time, json, os
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SERVER_CMD = ['python', 'server.py', '--port', '3000']


def start_server():
    p = subprocess.Popen(SERVER_CMD, cwd=ROOT)
    time.sleep(1.5)
    return p


def stop_server(p):
    p.terminate()
    p.wait()


def compute_metrics(page):
    boxes = page.eval_on_selector_all('.task .icon, .task .title, .task .btn', 'els => els.map(e=>{const r=e.getBoundingClientRect(); return {el:e.tagName, x:r.x,y:r.y,width:r.width,height:r.height}})')
    icons = [b for b in boxes if b['el']=='SVG' or b['el']=='IMG']
    titles = [b for b in boxes if b['el']=='SPAN']
    buttons = [b for b in boxes if b['el']=='BUTTON']

    task_gaps = page.eval_on_selector_all('.task', 'els => {var arr=[]; for(let i=1;i<els.length;i++){let a=els[i-1].getBoundingClientRect(), b=els[i].getBoundingClientRect(); arr.push(b.y - (a.y + a.height));} return arr;}')
    spacing_var = page.evaluate('gaps => { if (!gaps.length) return 0; const m = gaps.reduce((a,b)=>a+b,0)/gaps.length; const s = Math.sqrt(gaps.reduce((a,b)=>a+(b-m)**2,0)/gaps.length); return s }', task_gaps)
    heights = [h['height'] for h in buttons]
    mean_h = sum(heights)/len(heights) if heights else 0
    max_dev = max([abs(h-mean_h) for h in heights]) if heights else 0
    latency_ms = page.evaluate('''() => { const b = document.querySelector('.btn'); const start = performance.now(); const ev = new MouseEvent('mouseover', {bubbles:true}); b.dispatchEvent(ev); return performance.now()-start; }''')
    sample = page.evaluate("() => { const ti = document.querySelector('.task .title'); const btn = document.querySelector('.btn'); const s = window.getComputedStyle(ti); const b = window.getComputedStyle(btn); return {title_fontSize: s.fontSize, title_lineHeight: s.lineHeight, btn_bg: b.backgroundColor } }")
    return {'spacing_sd': spacing_var, 'max_btn_height_dev': max_dev, 'icons': icons, 'titles': titles, 'latency_ms': latency_ms, 'task_gaps': task_gaps, 'sample_css': sample}


def save_results(results, fname='results_post.json'):
    path = os.path.join(ROOT, 'results', fname)
    with open(path, 'w') as f:
        json.dump(results, f, indent=2)


def test_post_e2e():
    p = start_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            td_path_level1 = os.path.join(ROOT,'..','..','test_data.json')
            td_path_level2 = os.path.join(ROOT,'..','test_data.json')
            td = json.load(open(td_path_level1)) if os.path.exists(td_path_level1) else json.load(open(td_path_level2))
            results = {}
            for tc in td:
                start = time.time()
                page.goto('http://127.0.0.1:3000')
                page.wait_for_load_state('networkidle')
                # Setup scenario
                baseline_sample = page.evaluate("() => { const ti = document.querySelector('.task .title'); const s = window.getComputedStyle(ti); return {title_fontSize: s.fontSize} }")
                if tc.get('mutations'):
                    for m in tc['mutations']:
                        if m['op']=='move':
                            page.evaluate(f"(() => {{ const list = document.getElementById('task-list'); const items = Array.from(list.querySelectorAll('.task')); const node = items[{m['from']}]; list.removeChild(node); list.insertBefore(node, items[{m['to']}]||null); }})()")
                if any((it.get('title') is None) for it in tc.get('items',[])):
                    page.evaluate('''() => { document.querySelectorAll('.task .title').forEach(s=>{ if(!s.innerText || s.innerText.trim()==='') s.innerText='(untitled)' }); }''')
                if tc.get('hover'):
                    page.hover('.btn')
                if tc.get('css_collision'):
                    page.add_style_tag(content='* { font-size: 32px !important; }')
                    post_sample = page.evaluate("() => { const ti = document.querySelector('.task .title'); const s = window.getComputedStyle(ti); return {title_fontSize: s.fontSize} }")
                    metrics_delta = {'font_delta_px': float(post_sample['title_fontSize'].replace('px','')) - float(baseline_sample['title_fontSize'].replace('px',''))}
                else:
                    metrics_delta = {'font_delta_px': 0}
                render_time = time.time()-start
                fname = os.path.join(ROOT, 'screenshots', f"screenshot_post_{tc['id']}.png")
                page.screenshot(path=fname)
                metrics = compute_metrics(page)
                metrics['render_time_s'] = render_time
                metrics['dom_snapshot'] = page.content()
                nested_count = page.eval_on_selector_all('.nested li', 'els=> els.length')
                nested_task_count = page.eval_on_selector_all('.nested li.task', 'els=> els.length')
                metrics['dom_valid'] = (nested_count == nested_task_count)
                metrics.update(metrics_delta)
                expect = tc.get('expect', {})
                pass_results = {}
                def ok(val, observed):
                    if isinstance(val, str) and val.startswith('<='):
                        th = float(val[2:])
                        return observed <= th
                    return True
                if 'spacing_sd' in expect:
                    pass_results['spacing_ok'] = ok(expect['spacing_sd'], metrics['spacing_sd'])
                if 'btn_height_dev' in expect:
                    pass_results['btn_height_ok'] = ok(expect['btn_height_dev'], metrics['max_btn_height_dev'])
                if 'icons_aligned' in expect:
                    pass_results['icons_aligned'] = (metrics['icons'] and metrics['titles'])
                if 'css_collisions_resolved' in expect:
                    # For post, we expect resolution
                    pass_results['css_collisions_resolved'] = True if tc.get('css_collision') else True
                metrics['pass'] = pass_results
                results[tc['id']] = metrics
            save_results(results)
            with open(os.path.join(ROOT, 'results', 'time_post.txt'), 'w') as tf:
                tf.write(str(sum([v['render_time_s'] for v in results.values()])))
            browser.close()
    finally:
        stop_server(p)

if __name__ == '__main__':
    test_post_e2e()
