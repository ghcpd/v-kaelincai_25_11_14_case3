#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python -m pip install --user -r requirements.txt
python -m playwright install chromium
pytest tests/test_post_unit.py tests/test_post_e2e.py
