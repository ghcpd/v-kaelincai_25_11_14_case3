@REM Master script to run all tests - Windows
@echo off
setlocal enabledelayedexpansion

for /f %%A in ('cd') do set REPO_ROOT=%%A
set RESULTS_DIR=%REPO_ROOT%\results
set PROJECT_A_DIR=%REPO_ROOT%\Project_A_BeforeUI
set PROJECT_B_DIR=%REPO_ROOT%\Project_B_AfterUI

REM Create results directory
if not exist "%RESULTS_DIR%" mkdir "%RESULTS_DIR%"

echo =========================================
echo UI/UX Improvement Evaluation
echo =========================================
echo.

REM Run Project A tests
echo Running Project A (Before) tests...
cd /d "%PROJECT_A_DIR%"
call run_tests.bat
cd /d "%REPO_ROOT%"

echo.
echo Project A tests completed!
echo.

REM Run Project B tests
echo Running Project B (After) tests...
cd /d "%PROJECT_B_DIR%"
call run_tests.bat
cd /d "%REPO_ROOT%"

echo.
echo Project B tests completed!
echo.

REM Copy results to aggregated results folder
echo Aggregating results...
if exist "%PROJECT_A_DIR%\results\results_pre.json" (
    copy "%PROJECT_A_DIR%\results\results_pre.json" "%RESULTS_DIR%\" >nul
) else (
    echo Note: results_pre.json not found
)

if exist "%PROJECT_A_DIR%\results\time_pre.txt" (
    copy "%PROJECT_A_DIR%\results\time_pre.txt" "%RESULTS_DIR%\" >nul
) else (
    echo Note: time_pre.txt not found
)

if exist "%PROJECT_A_DIR%\logs\log_pre.txt" (
    copy "%PROJECT_A_DIR%\logs\log_pre.txt" "%RESULTS_DIR%\" >nul
) else (
    echo Note: log_pre.txt not found
)

if exist "%PROJECT_B_DIR%\results\results_post.json" (
    copy "%PROJECT_B_DIR%\results\results_post.json" "%RESULTS_DIR%\" >nul
) else (
    echo Note: results_post.json not found
)

if exist "%PROJECT_B_DIR%\results\time_post.txt" (
    copy "%PROJECT_B_DIR%\results\time_post.txt" "%RESULTS_DIR%\" >nul
) else (
    echo Note: time_post.txt not found
)

if exist "%PROJECT_B_DIR%\logs\log_post.txt" (
    copy "%PROJECT_B_DIR%\logs\log_post.txt" "%RESULTS_DIR%\" >nul
) else (
    echo Note: log_post.txt not found
)

REM Generate comparison report
echo.
echo Generating comparison report...
python "%REPO_ROOT%\generate_comparison_report.py"

echo.
echo =========================================
echo Evaluation Complete!
echo =========================================
echo.
echo Generated artifacts:
echo   - results\results_pre.json (Before)
echo   - results\results_post.json (After)
echo   - results\time_pre.txt
echo   - results\time_post.txt
echo   - results\log_pre.txt
echo   - results\log_post.txt
echo   - compare_report.md (Comparison)
echo.
echo Screenshots:
echo   - Project_A_BeforeUI\screenshots\
echo   - Project_B_AfterUI\screenshots\
echo.
