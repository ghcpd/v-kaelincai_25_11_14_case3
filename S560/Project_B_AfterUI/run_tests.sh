#!/usr/bin/env bash
set -e
. .venv/Scripts/activate
python -m pytest -q
