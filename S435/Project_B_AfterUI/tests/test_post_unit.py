import pytest
from ui_metrics import spacing_variance, check_button_height_consistency, normalize_dom_tree, alignment_issues


def test_spacing_variance_small():
    gaps = [10, 11, 10, 11]
    s = spacing_variance(gaps)
    assert s <= 2


def test_button_height_consistency_post():
    heights = [36, 36, 36, 36]
    diff = check_button_height_consistency(heights)
    assert diff <= 1


def test_dom_normalizer_handles_nulls_post():
    raw = {'page':'task_list','items':[{'title':None}, {'title':'OK'}]}
    norm = normalize_dom_tree(raw)
    assert norm['items'][0]['title'] == '(untitled)'


def test_alignment_issues_post():
    icons = [{'x':10,'y':16,'width':20,'height':20}, {'x':10,'y':16,'width':20,'height':20}]
    texts = [{'x':40,'y':16,'width':200,'height':20}, {'x':40,'y':16,'width':200,'height':20}]
    issues = alignment_issues(icons, texts)
    assert issues == 0


def test_dom_mutation_normalize_post():
    raw = {'page':'task_list','items':[{'title':'A'},{'title':'B'},{'title':'C'}]}
    raw['items'].insert(0, raw['items'].pop(2))
    norm = normalize_dom_tree(raw)
    assert norm['items'][0]['title'] == 'C'


def test_non_string_title_post():
    raw = {'page':'task_list','items':[{'title':123}, {'title':None}]}
    norm = normalize_dom_tree(raw)
    assert isinstance(norm['items'][0]['title'], int)
    assert norm['items'][1]['title'] == '(untitled)'
