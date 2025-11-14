Project B - Improved UI

How to run:
- Optionally create venv: python -m venv .venv; .\.venv\Scripts\Activate.ps1
- Install: pip install -r requirements.txt
- Install Playwright browsers: python -m playwright install
- Run unit tests: pytest -q tests/test_post_unit.py
- Run e2e: pytest -q tests/test_post_e2e.py

Artifacts:
- screenshots/: screenshot_post_<id>.png per test case
- results/: results_post.json, time_post.txt
- logs/: log_post.txt
