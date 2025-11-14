#!/usr/bin/env bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "from playwright.sync_api import sync_playwright; print('Playwright installing...')"
python -m playwright install
