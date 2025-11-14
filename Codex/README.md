# Task List UI/UX Improvement Evaluation

This workspace hosts two reproducible mini-projects that simulate a before/after UI modernization effort for a task-list surface. Each project ships a Flask web demo, Playwright E2E coverage, PyTest unit tests, layout-metric collectors, screenshot capture, logs, machine-readable outputs, and orchestration scripts.

## Scenario & Acceptance Criteria

**Tested interaction:** task list browsing with hover states, nested subtasks, density changes, malformed payloads, and CSS collisions.

**Structured payload:** test cases (see `test_data.json`) follow:

```json
{
  "page": "task_list",
  "items": [
    {"id": "t1", "title": "Task 1", "label": "Ops", "priority": "high", "icon": "?"}
  ],
  "hover": true,
  "mutation": "reorder_on_priority",
  "global_styles": "body button { padding: 4px; }"
}
```

**Expected "after" output:** normalized spacing, 40px pill buttons, baseline-aligned icons, responsive subtasks, hover feedback in <=16 ms, resilient DOM tree.

**Acceptance criteria enforced inside automated tests:**

- spacing variance <= 2px across consecutive cards
- button height range <= 2px
- icon/text baselines within 2px
- hover feedback latency <= 16 ms
- CSS collision count <= 1 after scoping
- DOM normalizer reports no invalid child nodes inside lists

## Test Data & Coverage Matrix

`test_data.json` encodes five required scenarios:

1. `normal_density` - baseline control
2. `dense_text` - long labels + hover stress
3. `missing_fields` - null labels/icons
4. `css_collision` - hostile global selectors
5. `dom_mutation` - nested subtasks + dynamic reorder

Each entry includes: `initial_dom`, `expected_layout_snapshot`, `css_rules_to_validate`, `screenshots_required`, and `expected` results (`pre` vs `post`). Playwright loops through the matrix, captures PNGs, and asserts the per-variant status matches expectations.

## Repository Layout

```
Project_A_BeforeUI/
  src/               # Flask app + dense baseline UI
  tests/             # unit + Playwright E2E (writes results_pre.json, log_pre.txt, time_pre.txt)
  screenshots/       # screenshot_pre_<case>.png artifacts
  logs/, results/    # metrics, JSON outputs
  requirements.txt, setup.sh, run_tests.sh
Project_B_AfterUI/
  ... (mirrors structure, produces *_post artifacts)
results/
  summary.json       # aggregated deltas (written by run_all.sh)
run_all.sh           # one-command orchestrator
compare_report.md    # auto-generated summary after run_all
README.md            # (this file)
```

## Environment Setup & Execution

1. **Before UI project**
   ```bash
   cd Project_A_BeforeUI
   bash setup.sh        # creates .venv, installs deps, installs Playwright browser
   bash run_tests.sh    # runs pytest (unit + E2E), produces screenshots/logs/results
   ```

2. **After UI project** - repeat in `Project_B_AfterUI` (scripts are analogous but export `UI_VARIANT=post`).

3. **Full evaluation**
   ```bash
   bash run_all.sh
   ```
   - Ensures both projects are set up/run in sequence.
   - Copies individual result files into the repo-level `results/` folder.
   - Generates `results/summary.json` (spacing/hover/CSS deltas) and rewrites `compare_report.md` with human-readable findings.

## Automated Tests

- **Unit tests (`test_pre_unit.py`, `test_post_unit.py`)** exercise spacing variance math, alignment counters, DOM validators, malformed input fallbacks, and acceptance evaluation logic.
- **E2E tests (`test_pre_e2e.py`, `test_post_e2e.py`)** spin up the local Flask server, drive Chromium via Playwright, trigger hover/responsive flows, record DOM/CSS snapshots, compute layout metrics, and persist:
  - `screenshots/screenshot_<variant>_<case>.png`
  - `logs/log_<variant>.txt` (includes DOM diff + CSS collision info)
  - `results/results_<variant>.json` (per-case metrics + verdicts)
  - `results/time_<variant>.txt` (run duration)

Each run also writes `results_pre.json` / `results_post.json` to the repo-level `results/` directory for quick diffing.

## Layout Metrics & Calculation Details

- Bounding boxes are captured via in-browser helpers (`window.__captureLayout`).
- Python-side utilities (`tests/utils/layout_metrics.py`) compute spacing vectors, variance, button-height range, icon baseline drift, CSS collision counts, hover latency, and DOM validity.
- Acceptance gates convert those measurements into verdicts; failures are expected for `pre` in several scenarios and flip to pass for `post`.

## Screenshots & Evidence

PNG artifacts live under each project's `screenshots/` folder using the `screenshot_<variant>_<case>.png` naming contract. Test logs enumerate the associated metrics so each screenshot can be traced back to spacing + CSS numbers.

## Pitfalls & Mitigations

- **Global CSS side effects:** hostile selectors from the test data are injected into both projects. Project B scopes button styles and reapplies component tokens so Playwright verifies collision counts drop to <=1.
- **Margin collapse / spacing drift:** Project A intentionally mixes negative/positive margins; Project B relies on CSS custom props + flex column gaps to maintain <=2 px variance.
- **DOM mutation race conditions:** Before UI performs naive `appendChild` operations; the improved UI sorts by semantic priority within a stable requestAnimationFrame cycle, which the DOM normalizer validates.
- **Malformed inputs:** Project B hydrates placeholders for null labels/titles, ensuring DOM stability and consistent layout metrics.

## Artifact Expectations

After running `run_all.sh`, you should have:

- `Project_A_BeforeUI/{screenshots,logs,results}` populated with `_pre_` artifacts.
- `Project_B_AfterUI/{screenshots,logs,results}` populated with `_post_` artifacts.
- Root-level `results/summary.json`, `results/results_pre.json`, `results/results_post.json`.
- `compare_report.md` summarizing spacing, hover, CSS, and verdict deltas.

All tooling stays offline-friendly and runnable via bash + Python on port 3000.
