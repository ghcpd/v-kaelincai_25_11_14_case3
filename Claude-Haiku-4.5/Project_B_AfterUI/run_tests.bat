@REM Run tests for Project B (After UI Improvement) - Windows
@echo off
setlocal enabledelayedexpansion

for /f %%A in ('cd') do set PROJECT_DIR=%%A

echo =========================================
echo Project B - After UI Improvement
echo =========================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Start the web server in background
echo Starting web server on http://localhost:3000...
start "" python src\server.py

REM Give server time to start
timeout /t 2 /nobreak

REM Run unit tests
echo.
echo Running unit tests...
cd tests
python -m pytest test_post_unit.py -v --tb=short
cd ..

REM Run E2E tests
echo.
echo Running E2E tests...
cd tests
python test_post_e2e.py
cd ..

REM Kill the server
taskkill /f /im python.exe 2>nul

echo.
echo =========================================
echo Tests completed!
echo Results saved to:
echo   - results\results_post.json
echo   - logs\log_post.txt
echo   - results\time_post.txt
echo Screenshots saved to:
echo   - screenshots\
echo =========================================
