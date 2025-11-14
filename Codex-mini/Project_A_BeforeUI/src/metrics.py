from typing import List, Dict, Any


def calc_spacing_variance(spacings: List[float], target: float = 12.0) -> float:
    if not spacings:
        return 0.0
    deviations = [(s - target) for s in spacings]
    squared = [d * d for d in deviations]
    variance = sum(squared) / len(squared)
    return variance ** 0.5


def check_alignment(coordinates: List[Dict[str, float]], threshold: float = 3.0) -> int:
    if not coordinates:
        return 0
    reference = coordinates[0].get("top", 0)
    misaligned = 0
    for coord in coordinates:
        if abs(coord.get("top", 0) - reference) > threshold:
            misaligned += 1
    return misaligned


def normalize_dom_tree(node: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {"tag": node.get("tag"), "children": []}
    for child in node.get("children", []):
        normalized["children"].append(normalize_dom_tree(child))
    return normalized


def handle_malformed_task(task: Dict[str, Any]) -> Dict[str, str]:
    title = task.get("title") if isinstance(task.get("title"), str) and task.get("title").strip() else "Untitled Task"
    status = task.get("status") if task.get("status") in {"pending", "in-progress", "blocked"} else "pending"
    return {"title": title, "status": status}
