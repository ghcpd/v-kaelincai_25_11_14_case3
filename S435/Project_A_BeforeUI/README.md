Project A - Baseline UI

How to run:
- Optionally create venv: python -m venv .venv; source .venv/bin/activate
- Install: pip install -r requirements.txt
- Install Playwright browsers: python -m playwright install
- Run unit tests: pytest -q tests/test_pre_unit.py
- Run e2e: pytest -q tests/test_pre_e2e.py

Artifacts:
- screenshots/: screenshot_pre_<id>.png per test case
- results/: results_pre.json, time_pre.txt
- logs/: log_pre.txt
