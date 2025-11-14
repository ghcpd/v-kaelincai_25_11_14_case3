$root = (Get-Location).Path
Write-Host "Running Project A (Before)"
Set-Location "$root/Project_A_BeforeUI"
if (-not (Test-Path .venv)) { python -m venv .venv }
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install
pytest -q
Copy-Item results\results_pre.json -Destination "$root/results/" -Force
Copy-Item screenshots\screenshot_pre_1.png -Destination "$root/results/" -Force

Write-Host "Running Project B (After)"
Set-Location "$root/Project_B_AfterUI"
if (-not (Test-Path .venv)) { python -m venv .venv }
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install
pytest -q
Copy-Item results\results_post.json -Destination "$root/results/" -Force
Copy-Item screenshots\screenshot_post_1.png -Destination "$root/results/" -Force

Write-Host "Comparing results..."
python "$root/compare_results.py" "$root/results/results_pre.json" "$root/results/results_post.json" "$root/compare_report.md"
Write-Host "Done: outputs in $root/results\ and compare_report.md"
