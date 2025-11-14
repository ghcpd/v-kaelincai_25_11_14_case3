#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
# Run unit tests
pytest -q tests/test_pre_unit.py | tee logs/log_pre_unit.txt
# Run e2e tests (these will start the local server)
pytest -q tests/test_pre_e2e.py | tee logs/log_pre_e2e.txt
# Consolidate logs
cat logs/log_pre_unit.txt logs/log_pre_e2e.txt > logs/log_pre.txt || true
