Project A — Baseline UI

How to run:
1. Create and activate a Python venv: `python -m venv .venv` and `. .venv/Scripts/activate` (PowerShell: `. .\.venv\Scripts\Activate.ps1`)
2. `pip install -r requirements.txt`
3. `playwright install`
4. Run tests: `.venv\Scripts\activate` then `pytest -q`

Artifacts:
- `screenshots/screenshot_pre_1.png`
- `results/results_pre.json`
- `logs/log_pre.txt`

Note: Baseline intentionally uses inconsistent CSS to test metrics and edge conditions.
