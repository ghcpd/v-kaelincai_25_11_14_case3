from typing import List, Dict

# Reuse same helpers but keep separate copy to simulate project-proper unit tests

def spacing_variance(gaps: List[float]) -> float:
    if not gaps:
        return 0.0
    mean = sum(gaps)/len(gaps)
    var = sum((g-mean)**2 for g in gaps)/len(gaps)
    return var**0.5


def check_button_height_consistency(heights: List[float]) -> float:
    if not heights:
        return 0.0
    mean = sum(heights)/len(heights)
    diffs = [abs(h-mean) for h in heights]
    return max(diffs)


def normalize_dom_tree(tree: Dict) -> Dict:
    def walk(node):
        if isinstance(node, dict):
            new = {}
            for k, v in node.items():
                if v is None and k == 'title':
                    new[k] = '(untitled)'
                elif isinstance(v, (dict, list)):
                    new[k] = walk(v)
                else:
                    new[k] = v
            return new
        elif isinstance(node, list):
            return [walk(n) for n in node]
        else:
            return node
    return walk(tree)


def alignment_issues(icon_boxes: List[Dict], texts: List[Dict]) -> int:
    issues = 0
    for ib, tb in zip(icon_boxes, texts):
        if abs((ib['y']+ib['height']/2) - tb['y']) > 2:
            issues += 1
    return issues
