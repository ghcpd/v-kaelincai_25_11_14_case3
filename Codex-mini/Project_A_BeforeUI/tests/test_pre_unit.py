import pytest
from src.metrics import calc_spacing_variance, check_alignment, normalize_dom_tree, handle_malformed_task


def test_calc_spacing_variance_returns_zero_for_empty():
    assert calc_spacing_variance([]) == 0.0


def test_calc_spacing_variance_margin():
    values = [10, 14, 13]
    assert round(calc_spacing_variance(values), 2) == round(((2**2 + 2**2 + 1**2) / 3) ** 0.5, 2)


def test_check_alignment_counts_misaligned():
    coords = [{"top": 10}, {"top": 12}, {"top": 20}]
    assert check_alignment(coords, threshold=3) == 1


def test_normalize_dom_tree_preserves_structure():
    node = {"tag": "ul", "children": [{"tag": "li", "children": []}]}
    normalized = normalize_dom_tree(node)
    assert normalized == {"tag": "ul", "children": [{"tag": "li", "children": []}]}


def test_handle_malformed_task_defaults():
    task = {"title": None, "status": "unknown"}
    normalized = handle_malformed_task(task)
    assert normalized == {"title": "Untitled Task", "status": "pending"}

@pytest.mark.parametrize("input_status,expected", [
    ("pending", "pending"),
    ("in-progress", "in-progress"),
    ("blocked", "blocked"),
    ("", "pending"),
])
def test_handle_malformed_task_status(input_status, expected):
    assert handle_malformed_task({"title": "hi", "status": input_status})["status"] == expected
