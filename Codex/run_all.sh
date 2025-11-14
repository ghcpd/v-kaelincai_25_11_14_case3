#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR=$(cd "$(dirname "$0")" && pwd)

run_project() {
  local project_dir="$1"
  pushd "$project_dir" >/dev/null
  if [ ! -d .venv ]; then
    echo "[setup] creating venv for $project_dir"
    bash setup.sh
  fi
  bash run_tests.sh
  popd >/dev/null
}

run_project "Project_A_BeforeUI"
run_project "Project_B_AfterUI"

python <<'PY'
import json
from pathlib import Path

root = Path('.').resolve()
results_dir = root / 'results'
results_dir.mkdir(exist_ok=True)
pre_path = root / 'Project_A_BeforeUI' / 'results' / 'results_pre.json'
post_path = root / 'Project_B_AfterUI' / 'results' / 'results_post.json'
pre = json.loads(pre_path.read_text())
post = json.loads(post_path.read_text())

index_post = {case['id']: case for case in post['cases']}
comparisons = []
for case in pre['cases']:
    post_case = index_post.get(case['id'], {})
    comparisons.append({
        'id': case['id'],
        'spacing_delta': case['metrics']['spacing_variance'] - post_case.get('metrics', {}).get('spacing_variance', 0),
        'hover_delta': case['metrics']['hover_latency'] - post_case.get('metrics', {}).get('hover_latency', 0),
        'css_delta': case['metrics']['css_collisions'] - post_case.get('metrics', {}).get('css_collisions', 0),
        'status_transition': f"{case['status']}->{post_case.get('status', 'unknown')}",
    })

summary = {
    'pre_summary': pre['summary'],
    'post_summary': post['summary'],
    'comparisons': comparisons,
}

(results_dir / 'summary.json').write_text(json.dumps(summary, indent=2))
(results_dir / 'results_pre.json').write_text(pre_path.read_text())
(results_dir / 'results_post.json').write_text(post_path.read_text())

lines = [
    '# UI/UX Improvement Comparison',
    '',
    f"Average spacing variance improved from {pre['summary']['avg_spacing_variance']:.2f} to {post['summary']['avg_spacing_variance']:.2f}.",
    f"Hover latency average improved from {pre['summary']['avg_hover_latency']:.2f}ms to {post['summary']['avg_hover_latency']:.2f}ms.",
    '',
    '## Case Results',
]
for comp in comparisons:
    lines.append(
        f"- {comp['id']}: spacing delta {comp['spacing_delta']:.2f}, hover delta {comp['hover_delta']:.2f}ms, css delta {comp['css_delta']}, status {comp['status_transition']}"
    )

(root / 'compare_report.md').write_text('\n'.join(lines))
PY
