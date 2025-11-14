python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python -m playwright install; pytest -q tests\test_pre_unit.py; pytest -q tests\test_pre_e2e.py
