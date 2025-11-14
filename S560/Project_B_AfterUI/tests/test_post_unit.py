import pytest
from layout_utils import spacing_variance, compute_item_spacings, icons_aligned, normalize_dom_text


def test_spacing_variance_target():
    spacings = [14, 14, 16, 16]
    sdev = spacing_variance(spacings)
    assert sdev <= 1.0


def test_item_spacings_basic():
    bboxes = [
        {"x":0, "y":0, "width":200, "height":40},
        {"x":0, "y":54, "width":200, "height":40},
        {"x":0, "y":108, "width":200, "height":40},
    ]
    spacings = compute_item_spacings(bboxes)
    assert len(spacings) == 2
    assert spacings[0] == 14
    assert spacings[1] == 14


def test_icons_alignment_improved():
    icons = [{"x":0, "y":10.3, "width":24, "height":24}, {"x":0, "y":10.1, "width":24, "height":24}, {"x":0, "y":9.9, "width":24, "height":24}]
    assert icons_aligned(icons, tolerance=2)


def test_dom_normalizer_handles_empty():
    assert normalize_dom_text(None) == ''
    assert normalize_dom_text('   ') == ''
