@REM Setup script for Project B (After UI Improvement) - Windows
@echo off
setlocal enabledelayedexpansion

echo Setting up Project B (After UI)...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Install Playwright browsers
echo Installing Playwright browsers...
playwright install chromium

echo Setup complete! Project B is ready.
echo.
echo To run tests:
echo   run_tests.bat
