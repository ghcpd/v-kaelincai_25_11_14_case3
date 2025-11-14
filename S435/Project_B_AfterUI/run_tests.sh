#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
# Run unit tests
pytest -q tests/test_post_unit.py | tee logs/log_post_unit.txt
# Run e2e tests (these will start the local server)
pytest -q tests/test_post_e2e.py | tee logs/log_post_e2e.txt
# Consolidate logs
cat logs/log_post_unit.txt logs/log_post_e2e.txt > logs/log_post.txt || true
