# PowerShell version to run both projects
$root = Get-Location
Push-Location Project_A_BeforeUI
if (Test-Path .venv) { Write-Host 'Virtual env exists' } else { python -m venv .venv }
.\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python -m playwright install; pytest -q tests\test_pre_unit.py; pytest -q tests\test_pre_e2e.py
Copy-Item -Path screenshots\* -Destination (Join-Path $root 'results') -Force -ErrorAction SilentlyContinue
Pop-Location

Push-Location Project_B_AfterUI
if (Test-Path .venv) { Write-Host 'Virtual env exists' } else { python -m venv .venv }
.\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python -m playwright install; pytest -q tests\test_post_unit.py; pytest -q tests\test_post_e2e.py
Copy-Item -Path screenshots\* -Destination (Join-Path $root 'results') -Force -ErrorAction SilentlyContinue
Pop-Location

# Simple compare
$pre = Get-Content -Raw -Path (Join-Path $root 'results\results_pre.json') | ConvertFrom-Json
$post = Get-Content -Raw -Path (Join-Path $root 'results\results_post.json') | ConvertFrom-Json
$compare = @{ pre=$pre; post=$post }
$compare | ConvertTo-Json | Out-File -FilePath (Join-Path $root 'results\compare.json')
Write-Host 'All done.'
