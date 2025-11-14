import pytest
from layout_utils import spacing_variance, compute_item_spacings, icons_aligned, normalize_dom_text


def test_spacing_variance_basic():
    spacings = [8, 10, 12]
    sdev = spacing_variance(spacings)
    assert sdev < 2.1


def test_item_spacings_sorted_order():
    bboxes = [
        {"x":0, "y":0, "width":200, "height":40},
        {"x":0, "y":48, "width":200, "height":40},
        {"x":0, "y":98, "width":200, "height":40},
    ]
    spacings = compute_item_spacings(bboxes)
    assert len(spacings) == 2
    assert spacings[0] == 8
    assert spacings[1] == 10


def test_icons_alignment():
    icons = [{"x":0, "y":10, "width":20, "height":20}, {"x":0, "y":11, "width":20, "height":20}, {"x":0, "y":8, "width":20, "height":20}]
    assert icons_aligned(icons, tolerance=3)


def test_dom_normalizer():
    s = '  Null  label\n  n/a   extra '
    assert normalize_dom_text(s) == 'label extra'
