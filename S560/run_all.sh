#!/usr/bin/env bash
set -e
ROOT=$(pwd)

# Setup and run Project A
cd "$ROOT/Project_A_BeforeUI"
if [ ! -d .venv ]; then
  python -m venv .venv
fi
. .venv/Scripts/activate
pip install -r requirements.txt
playwright install
pytest -q

# Copy results
mkdir -p "$ROOT/results"
cp results/results_pre.json "$ROOT/results/"
cp screenshots/screenshot_pre_1.png "$ROOT/results/"

# Setup and run Project B
cd "$ROOT/Project_B_AfterUI"
if [ ! -d .venv ]; then
  python -m venv .venv
fi
. .venv/Scripts/activate
pip install -r requirements.txt
playwright install
pytest -q

cp results/results_post.json "$ROOT/results/"
cp screenshots/screenshot_post_1.png "$ROOT/results/"

# Compare results
python "$ROOT/compare_results.py" "$ROOT/results/results_pre.json" "$ROOT/results/results_post.json" "$ROOT/compare_report.md"

echo "Done: outputs in $ROOT/results/ and compare_report.md"
