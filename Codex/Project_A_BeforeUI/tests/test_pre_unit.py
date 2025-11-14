from tests.utils.layout_metrics import (
    LayoutMetrics,
    button_height_range,
    dom_is_valid,
    evaluate_acceptance,
    misaligned_icons,
    spacing_from_boxes,
    summarize_metrics,
)


def test_spacing_variance_detects_inconsistent_gap():
  boxes = [
      {'top': 0, 'bottom': 50, 'buttonHeight': 20},
      {'top': 60, 'bottom': 110, 'buttonHeight': 28},
      {'top': 130, 'bottom': 180, 'buttonHeight': 28},
  ]
  spacings, variance = spacing_from_boxes(boxes)
  assert spacings == [10, 20]
  assert variance > 20


def test_button_height_range_exposes_mismatch():
  boxes = [
      {'buttonHeight': 20},
      {'buttonHeight': 34},
      {'buttonHeight': 34},
  ]
  assert button_height_range(boxes) == 14


def test_alignment_checker_counts_misaligned_icons():
  boxes = [
      {'iconTop': 10, 'textTop': 11},
      {'iconTop': 20, 'textTop': 27},
  ]
  assert misaligned_icons(boxes, tolerance=2) == 1


def test_dom_validator_flags_invalid_items():
  snapshot = {
      'tag': 'UL',
      'children': [
          {'tag': 'DIV', 'children': []},
          {'tag': 'LI', 'children': []},
      ],
  }
  valid, issues = dom_is_valid(snapshot)
  assert not valid
  assert issues


def test_evaluate_acceptance_combines_metrics():
  metrics = LayoutMetrics(
      spacing_values=[4, 4],
      spacing_variance=0.0,
      button_height_range=1.0,
      misaligned_icons=0,
      css_collisions=0,
      hover_latency=10,
      dom_valid=True,
  )
  verdict = evaluate_acceptance(metrics)
  assert verdict['overall']


def test_summary_pipeline_from_boxes():
  boxes = [
      {'top': 0, 'bottom': 40, 'buttonHeight': 36, 'iconTop': 10, 'textTop': 12},
      {'top': 60, 'bottom': 100, 'buttonHeight': 36, 'iconTop': 70, 'textTop': 71},
  ]
  metrics = summarize_metrics(boxes, css_collisions=2, hover_latency=30, dom_snapshot={'tag': 'DIV', 'children': []})
  assert metrics.spacing_variance == 100.0
  assert metrics.css_collisions == 2
