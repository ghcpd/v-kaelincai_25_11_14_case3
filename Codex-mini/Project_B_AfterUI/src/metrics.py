from typing import Any, Dict, List


def calc_spacing_variance(spacings: List[float], target: float = 16.0) -> float:
    if not spacings:
        return 0.0
    deviations = [(spacing - target) for spacing in spacings]
    squared = [d * d for d in deviations]
    variance = sum(squared) / len(squared)
    return variance ** 0.5


def check_alignment(coordinates: List[Dict[str, float]], threshold: float = 2.0) -> int:
    if not coordinates:
        return 0
    baseline = coordinates[0].get("y", 0)
    return sum(1 for coord in coordinates if abs(coord.get("y", 0) - baseline) > threshold)


def normalize_dom_tree(node: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {"tag": node.get("tag"), "children": []}
    for child in node.get("children", []):
        normalized["children"].append(normalize_dom_tree(child))
    return normalized


def handle_malformed_task(task: Dict[str, Any]) -> Dict[str, str]:
    title = task.get("title")
    if not isinstance(title, str) or not title.strip():
        title = "Untitled Task"
    status = task.get("status")
    if status not in {"pending", "in-progress", "blocked"}:
        status = "pending"
    return {"title": title, "status": status}


def depth_of_dom(node: Dict[str, Any]) -> int:
    if not node.get("children"):
        return 1
    return 1 + max(depth_of_dom(child) for child in node.get("children", []))
