# UI/UX Improvement Evaluation

This repository contains two runnable task-list demos: `Project_A_BeforeUI` (baseline) and `Project_B_AfterUI` (improved). Each project ships its own Flask server, CSS/JS front-end, automated unit + Playwright-based E2E suites, and artifacts that document layout metrics, logs, and screenshots.

## Running the demos

1. **Environment bootstrap (Linux/macOS/WSL)** 每 run `./Project_A_BeforeUI/setup.sh` then `./Project_B_AfterUI/setup.sh` to install shared dependencies and the Chromium driver. On Windows, execute the same commands from PowerShell using `bash` or adapt to `python -m pip install -r requirements.txt` + `python -m playwright install chromium`.
2. **Project-specific tests** 每 from each project folder run `bash run_tests.sh`. Each script installs dependencies (if needed), starts the Flask server on port 3000, launches Playwright, captures spacing metrics, saves screenshots, and writes `results_*`, `log_*`, and `time_*` files.
3. **Full evaluation** 每 `./run_all.sh` executes Project A then Project B, copies the generated artifacts into the root-level `/results` folder, and emits `diff_metrics.json`, `diff_logs.txt`, and `compare_report.md`. (When `bash`/WSL is unavailable, replicate the script steps using PowerShell or Bash on Git for Windows.)

## Testing and coverage

- Unit tests (`tests/test_pre_unit.py`, `tests/test_post_unit.py`) validate spacing variance, alignment checks, DOM normalization, malformed handling, and depth detection logic in `src/metrics.py`.
- E2E tests (`tests/test_pre_e2e.py`, `tests/test_post_e2e.py`) start the Flask demo, drive Playwright flows (click/hover), capture DOM/CSS snapshots, compute layout metrics (spacing deviation, icon alignment, hover latency), and save screenshots (`screenshots/screenshot_pre_1.png`, `screenshots/screenshot_post_1.png`). Test artifacts include `results_pre.json`, `results_post.json`, timing logs, and DOM snapshots.
- Additional `test_data.json` describes five structured scenarios (normal, dense, malformed, CSS collision, DOM mutation) with expected layout/CSS rules plus pass/fail signals.

## Metrics interpretation

- **Spacing deviation** 每 represents the standard deviation of vertical gutters; values ≒ 2px indicate controlled spacing. Lower values in Project B imply the new whitespace system is more predictable.
- **Icon alignment** 每 counts how many task icons fall outside a 3px horizontal band; zero misalignments mean the improved layout respects inline baselines.
- **Hover latency** 每 Playwright measures how quickly hover interactions register (target < 16ms). Project B also adds visual transitions on buttons for clearer feedback.
- **Render time** 每 `time_pre.txt`/`time_post.txt` capture end-to-end rendering durations, showing whether layout updates add perceptible delay.
- **Diff artifacts** 每 `results/diff_metrics.json` and `results/diff_logs.txt` summarize year-over-year improvements and log length differences for easy comparison.

## Known pitfalls & mitigations

1. **Global CSS side effects** 每 resets such as `body * { margin: 0 }` can collide with component-level spacing. Scope selectors to `.task-card` and use utility variables to avoid overrides.
2. **Inconsistent margin collapse** 每 inconsistent wrappers can collapse margins unexpectedly. Standardize container padding/gutters with explicit gaps or flexbox spacing instead of relying on default margins.
3. **DOM mutation race conditions** 每 dynamic reorders or nested lists can expose malformed nodes. Normalize the DOM tree (see `src/metrics.py`) and guard asynchronous rendering with defensive checks before measuring spacing.

## Additional notes

- All artifacts (screenshots, logs, JSON results) live under each project (`screenshots/`, `logs/`, `results/`) and are aggregated to `/results` for summary.
- The `run_all.sh` script assumes Bash/WSL but the same steps can be run manually on other platforms; it orchestrates both test suites and writes `compare_report.md` with quantitative insights.
- Use `test_data.json` to synthesize synthetic DOM states in future experiments or to drive additional Playwright scenarios.
