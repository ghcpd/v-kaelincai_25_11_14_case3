from src.metrics import calc_spacing_variance, check_alignment, normalize_dom_tree, handle_malformed_task, depth_of_dom


def test_spacing_variance_improved():
    values = [16, 16, 15, 16]
    assert calc_spacing_variance(values) < 1


def test_alignment_checker():
    coords = [{"y": 10}, {"y": 11}, {"y": 20}]
    assert check_alignment(coords, threshold=2) == 1


def test_dom_normalizer_prefers_structure():
    tree = {"tag": "div", "children": [{"tag": "span", "children": []}]}
    assert normalize_dom_tree(tree) == tree


def test_handle_malformed_defaults_to_pending():
    task = {"title": "", "status": None}
    normalized = handle_malformed_task(task)
    assert normalized["title"] == "Untitled Task"
    assert normalized["status"] == "pending"


def test_dom_depth():
    tree = {"tag": "root", "children": [{"tag": "child", "children": []}]}
    assert depth_of_dom(tree) == 2
