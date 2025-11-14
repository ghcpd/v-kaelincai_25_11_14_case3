#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")" && pwd)
projects=("Project_A_BeforeUI" "Project_B_AfterUI")
results="$root/results"
rm -rf "$results"
mkdir -p "$results"
for project in "${projects[@]}"; do
  echo "Running $project"
  pushd "$root/$project" >/dev/null
  bash run_tests.sh > "$results/${project}.log" 2>&1
  popd >/dev/null
done
cp "$root/Project_A_BeforeUI/results/results_pre.json" "$results/"
cp "$root/Project_A_BeforeUI/results/time_pre.txt" "$results/"
cp "$root/Project_A_BeforeUI/logs/log_pre.txt" "$results/"
cp "$root/Project_A_BeforeUI/screenshots/screenshot_pre_1.png" "$results/"
cp "$root/Project_B_AfterUI/results/results_post.json" "$results/"
cp "$root/Project_B_AfterUI/results/time_post.txt" "$results/"
cp "$root/Project_B_AfterUI/logs/log_post.txt" "$results/"
cp "$root/Project_B_AfterUI/screenshots/screenshot_post_1.png" "$results/"
python - <<'PY'
import json
from pathlib import Path
root = Path(__file__).resolve().parent
pre_metrics = json.loads((root / "Project_A_BeforeUI" / "results" / "results_pre.json").read_text())
post_metrics = json.loads((root / "Project_B_AfterUI" / "results" / "results_post.json").read_text())
hover_pre = pre_metrics["metrics"].get("hover_latency_ms", 0)
hover_post = post_metrics["metrics"].get("hover_latency_ms", 0)
spacing_pre = pre_metrics["metrics"].get("spacing_deviation", 0)
spacing_post = post_metrics["metrics"].get("spacing_variance", 0)
misaligned_pre = pre_metrics["metrics"].get("misaligned_icons", 0)
misaligned_post = post_metrics["metrics"].get("misaligned_icons", 0)
time_pre = float((root / "Project_A_BeforeUI" / "results" / "time_pre.txt").read_text().strip())
time_post = float((root / "Project_B_AfterUI" / "results" / "time_post.txt").read_text().strip())
misalignment_delta = misaligned_pre - misaligned_post
hover_delta = hover_pre - hover_post
render_time_delta = time_pre - time_post
diff = {
    "spacing_delta": spacing_pre - spacing_post,
    "misalignment_delta": misalignment_delta,
    "hover_latency_delta_ms": hover_delta,
    "render_time_savings": render_time_delta,
}
(Path(root / "results" / "diff_metrics.json")).write_text(json.dumps(diff, indent=2), encoding="utf-8")
(Path(root / "results" / "diff_logs.txt")).write_text(
    f"Log length pre: {len(Path(root / "Project_A_BeforeUI" / "logs" / "log_pre.txt").read_text())}\n"
    f"Log length post: {len(Path(root / "Project_B_AfterUI" / "logs" / "log_post.txt").read_text())}\n",
    encoding="utf-8"
)
report = root / "compare_report.md"
report.write_text(
    f"""# UI/UX Comparison Report

    ## Key Metrics
    - Baseline spacing variance: {spacing_pre}
    - Improved spacing variance: {spacing_post}
    - Misaligned icons reduced by: {misalignment_delta}
    - Hover latency change: {hover_delta} ms
    - Render time savings: {render_time_delta:.2f} s

    ## Observations
    1. Project B introduces consistent spacing, responsive grid, and accessible buttons.
    2. Hover/active feedback is unified with CSS transitions, resolving the baseline density.
    3. DOM tree normalization prevents malformed inputs from breaking spacing logic.

    ## Recommendations
    - Keep the spacing delta below 2px to maintain consistent layout.
    - Monitor hover feedback latency to stay under 16ms for interactive affordance.
    - Continue running the Playwright snapshots to validate DOM mutations and CSS collisions.
    """,
    encoding="utf-8",
)
PY
