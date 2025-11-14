from tests.utils.layout_metrics import (
    LayoutMetrics,
    button_height_range,
    dom_is_valid,
    evaluate_acceptance,
    misaligned_icons,
    spacing_from_boxes,
    summarize_metrics,
)


def test_spacing_variance_stays_within_threshold():
  boxes = [
      {'top': 0, 'bottom': 60, 'buttonHeight': 40},
      {'top': 66, 'bottom': 126, 'buttonHeight': 40},
      {'top': 132, 'bottom': 192, 'buttonHeight': 40},
  ]
  _, variance = spacing_from_boxes(boxes)
  assert variance <= 2


def test_button_height_range_is_zero():
  boxes = [
      {'buttonHeight': 40},
      {'buttonHeight': 40},
  ]
  assert button_height_range(boxes) == 0


def test_alignment_checker_accepts_baseline_icons():
  boxes = [
      {'iconTop': 10, 'textTop': 10},
      {'iconTop': 20, 'textTop': 21},
  ]
  assert misaligned_icons(boxes) == 0


def test_dom_validator_accepts_nested_lists():
  snapshot = {
      'tag': 'UL',
      'children': [
          {'tag': 'LI', 'children': [{'tag': 'UL', 'children': [{'tag': 'LI', 'children': []}]}]},
      ],
  }
  valid, _ = dom_is_valid(snapshot)
  assert valid


def test_acceptance_enforces_css_and_hover():
  metrics = LayoutMetrics(
      spacing_values=[6, 6],
      spacing_variance=0.0,
      button_height_range=0.0,
      misaligned_icons=0,
      css_collisions=0,
      hover_latency=9.0,
      dom_valid=True,
  )
  verdict = evaluate_acceptance(metrics)
  assert verdict['overall']


def test_summary_metrics_round_trip():
  boxes = [
      {'top': 0, 'bottom': 50, 'buttonHeight': 40, 'iconTop': 10, 'textTop': 10},
      {'top': 60, 'bottom': 110, 'buttonHeight': 40, 'iconTop': 70, 'textTop': 70},
  ]
  metrics = summarize_metrics(boxes, css_collisions=0, hover_latency=8, dom_snapshot={'tag': 'UL', 'children': []})
  verdict = evaluate_acceptance(metrics)
  assert verdict['overall']
