from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Dict, List, Tuple


@dataclass
class LayoutMetrics:
  spacing_values: List[float]
  spacing_variance: float
  button_height_range: float
  misaligned_icons: int
  css_collisions: int
  hover_latency: float
  dom_valid: bool


def _variance(values: List[float]) -> float:
  if not values:
    return 0.0
  avg = mean(values)
  return sum((v - avg) ** 2 for v in values) / len(values)


def spacing_from_boxes(boxes: List[Dict[str, float]]) -> Tuple[List[float], float]:
  spacings: List[float] = []
  for prev, curr in zip(boxes, boxes[1:]):
    top_gap = curr.get('top', 0) - prev.get('bottom', 0)
    spacings.append(round(top_gap, 2))
  return spacings, _variance(spacings)


def button_height_range(boxes: List[Dict[str, float]]) -> float:
  heights: List[float] = []
  for box in boxes:
    if box.get('buttonHeights'):
      heights.extend([value for value in box['buttonHeights'] if value])
    elif box.get('buttonHeight'):
      heights.append(box['buttonHeight'])
  if not heights:
    return 0.0
  return max(heights) - min(heights)


def misaligned_icons(boxes: List[Dict[str, float]], tolerance: float = 2.0) -> int:
  misaligned = 0
  for box in boxes:
    icon_top = box.get('iconTop')
    text_top = box.get('textTop')
    if icon_top is None or text_top is None:
      continue
    if abs(icon_top - text_top) > tolerance:
      misaligned += 1
  return misaligned


def dom_is_valid(snapshot: Dict) -> Tuple[bool, List[str]]:
  issues: List[str] = []

  if not snapshot:
    return False, ['Snapshot was empty']

  if snapshot.get('tag') != 'UL':
    issues.append('Root node must be UL')

  def walk(node: Dict, parent: str | None) -> None:
    if not node:
      return
    tag = node.get('tag')
    children = node.get('children', [])
    if parent == 'UL' and tag != 'LI':
      issues.append(f"UL child must be LI but found {tag}")
    for child in children:
      walk(child, tag)

  walk(snapshot, None)
  return (len(issues) == 0, issues)


def summarize_metrics(boxes: List[Dict[str, float]], css_collisions: int, hover_latency: float, dom_snapshot: Dict | None) -> LayoutMetrics:
  spacing_values, variance = spacing_from_boxes(boxes)
  dom_valid, _ = dom_is_valid(dom_snapshot or {})
  return LayoutMetrics(
    spacing_values=spacing_values,
    spacing_variance=variance,
    button_height_range=button_height_range(boxes),
    misaligned_icons=misaligned_icons(boxes),
    css_collisions=css_collisions,
    hover_latency=hover_latency,
    dom_valid=dom_valid,
  )


def evaluate_acceptance(metrics: LayoutMetrics) -> Dict[str, bool]:
  verdict = {
    'spacing': metrics.spacing_variance <= 2,
    'buttons': metrics.button_height_range <= 2,
    'icons': metrics.misaligned_icons == 0,
    'hover': metrics.hover_latency <= 16,
    'dom': metrics.dom_valid,
    'css': metrics.css_collisions <= 1,
  }
  verdict['overall'] = all(verdict.values())
  return verdict
