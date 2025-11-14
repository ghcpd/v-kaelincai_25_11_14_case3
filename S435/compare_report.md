# Compare Report

This report summarizes the UI/UX improvement measurement between Project_A_BeforeUI (pre) and Project_B_AfterUI (post). Run `./run_all.sh` to generate `results/` and the JSON and PNG artifacts.

## Summary of improvements
- Improved spacing and spacing system (CSS variables)
- Unified and consistent button styles and baseline alignment
- Hover/active feedback and keyboard accessibility
- More robust DOM handling for malformed input

## Metrics collected
- spacing_sd: standard deviation of vertical gaps between tasks
- max_btn_height_dev: maximum difference in button heights (px)
- dom_valid: whether nested lists have valid li.task entries
- font_delta_px: change in font size after global css collision injection
- latency_ms: event dispatch/hover latency (ms)

## Risks and observations
- CSS global collisions using `!important` may still override local definitions — mitigate with more specific selectors or component scoping.
- Margin collapse and whitespace can still vary across browsers; use containment and consistent spacing rules.
- DOM mutation race conditions are addressed by tests using demo stabilizing waits; in production, prefer guarded state updates.

## Next steps
- Add visual regression snapshot diffs (pixel-comparison)
- Expand acceptance thresholds per device/viewport
- Add CI integration with headless browsers

See the `results/` folder for detailed logs and per-test artifacts.
