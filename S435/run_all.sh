#!/usr/bin/env bash
set -e
ROOT=$(pwd)
# Run Project A tests
cd Project_A_BeforeUI
./setup.sh || true
./run_tests.sh
mkdir -p "$ROOT/results/pre"
cp -r results/* "$ROOT/results/pre/"
cp -r screenshots/* "$ROOT/results/pre/"
cp logs/log_pre.txt "$ROOT/results/pre/log_pre.txt" || true
cd "$ROOT"
# Run Project B tests
cd Project_B_AfterUI
./setup.sh || true
./run_tests.sh
mkdir -p "$ROOT/results/post"
cp -r results/* "$ROOT/results/post/"
cp -r screenshots/* "$ROOT/results/post/"
cp logs/log_post.txt "$ROOT/results/post/log_post.txt" || true
cd "$ROOT"
# Generate diff using results files
python - << 'PY'
import json,os
root='.'
results_dir=os.path.join(root,'results')
pre=os.path.join(results_dir,'results_pre.json')
post=os.path.join(results_dir,'results_post.json')
pre_d={}
post_d={}
if os.path.exists(pre): pre_d=json.load(open(pre))
if os.path.exists(post): post_d=json.load(open(post))
diff={'pre':pre_d,'post':post_d}
open(os.path.join(results_dir,'compare.json'),'w').write(json.dumps(diff,indent=2))
print('Compare written to results/compare.json')
PY

# Create detailed compare report
python - << 'PY'
import json,os
r='results'
pr=os.path.join(r,'pre','results_pre.json')
po=os.path.join(r,'post','results_post.json')
pre=json.load(open(pr)) if os.path.exists(pr) else {}
post=json.load(open(po)) if os.path.exists(po) else {}
rep='compare_report.md'
lines=[]
lines.append('# Compare Report\n')
lines.append('This report summarizes metrics and pass/fail per test case.\n')
ids = sorted(set(list(pre.keys()) + list(post.keys())), key=lambda x: int(x))
for tid in ids:
    p = pre.get(tid, {})
    q = post.get(tid, {})
    lines.append(f'## Test {tid}\n')
    lines.append('- Pre:')
    lines.append('```json')
    lines.append(json.dumps(p, indent=2))
    lines.append('```\n')
    lines.append('- Post:')
    lines.append('```json')
    lines.append(json.dumps(q, indent=2))
    lines.append('```\n')
    # quick diff
    if 'spacing_sd' in p and 'spacing_sd' in q:
        lines.append(f"- Spacing SD delta: {p['spacing_sd'] - q['spacing_sd']:.2f}\n")
    if 'max_btn_height_dev' in p and 'max_btn_height_dev' in q:
        lines.append(f"- Max button height dev delta: {p['max_btn_height_dev'] - q['max_btn_height_dev']:.2f}\n")
    # pass/fail
    pass_pre = p.get('pass',{})
    pass_post = q.get('pass',{})
    lines.append('- Pass summary: Pre: '+json.dumps(pass_pre)+' Post: '+json.dumps(pass_post)+'\n')

open(rep,'w').write('\n'.join(lines))
print('Compare written to', rep)
PY

echo "All done. Results in results/ and compare_report.md"
