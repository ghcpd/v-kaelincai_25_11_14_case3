# UI/UX Improvement Evaluation Demo

This repository contains two projects demonstrating Task List UI improvements:
- Project_A_BeforeUI: Baseline with poor spacing and inconsistent components
- Project_B_AfterUI: Improved UI with spacing system, unified components, and interaction feedback

Run the experiments and tests using the provided scripts. They are designed to be runnable locally and produce screenshots and JSON metrics.

Prerequisites:
- Python 3.10+ installed
- Optional: Node.js for Playwright (python installation attempts to install browsers)

Quick start (Unix/macOS):
- Run the combined automation:
  ./run_all.sh

On Windows PowerShell:
- Use the respective .ps1 files, e.g. Project_A_BeforeUI\setup.ps1, then Project_A_BeforeUI\run_tests.ps1

Artifacts produced:
- results/: aggregated JSON results, compare.json
- screenshots/: pre/post screenshots per test case
- compare_report.md: textual summary

Notes:
- The script will run Playwright which will download browsers on first run.
- The tests start local Flask servers on port 3000; port must be available.

Interpretation of metrics:
- spacing_sd: standard deviation of vertical gaps between tasks (<=2 recommended)
- max_btn_height_dev: max difference in button heights (<=2 px)
- icons: array of icon bounding boxes for baseline and checks
- latency_ms: approximate milliseconds for hover event dispatch latency

Known pitfalls and mitigations:
- Global CSS collisions: use component-scoped rules or utility spacing tokens
- Margin collapse: ensure proper containment with padding or border where needed
- DOM mutation race conditions: debounce/microtask stabilization in tests (we wait briefly in E2E)

