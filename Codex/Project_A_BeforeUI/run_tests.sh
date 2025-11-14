#!/usr/bin/env bash
set -euo pipefail
if [ ! -d .venv ]; then
  echo "Virtual environment not found. Run setup.sh first." >&2
  exit 1
fi
source .venv/bin/activate
export PYTHONPATH=$PWD/src
export UI_VARIANT=pre
pytest tests -s --maxfail=1 --disable-warnings
