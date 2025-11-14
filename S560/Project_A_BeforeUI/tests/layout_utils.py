from typing import List, Dict
import math

# Bounding box structure: {"x":float,"y":float,"width":float,"height":float}

def spacing_variance(spacings: List[float]) -> float:
    if not spacings:
        return 0.0
    mean = sum(spacings) / len(spacings)
    var = sum((s - mean) ** 2 for s in spacings) / len(spacings)
    return math.sqrt(var)  # standard deviation


def compute_item_spacings(bboxes: List[Dict[str, float]]) -> List[float]:
    # Compute vertical spacing between adjacent items using their bounding boxes
    if not bboxes or len(bboxes) < 2:
        return []
    spacings = []
    # items assumed sorted by y
    bboxes_sorted = sorted(bboxes, key=lambda b: b['y'])
    for a, b in zip(bboxes_sorted, bboxes_sorted[1:]):
        gap = max(0.0, b['y'] - (a['y'] + a['height']))
        spacings.append(gap)
    return spacings


def icons_aligned(bboxes_icons: List[Dict[str, float]], tolerance: float = 2.0) -> bool:
    # check if icons have similar y coordinates within tolerance
    if not bboxes_icons:
        return True
    tops = [bbox['y'] for bbox in bboxes_icons]
    mean = sum(tops)/len(tops)
    return max(abs(t - mean) for t in tops) <= tolerance


def normalize_dom_text(text: str) -> str:
    # Simplified DOM label normalization; replace multiple whitespace and null-like tokens
    import re
    text = (text or '')
    text = text.replace('\u00a0',' ')
    text = re.sub(r'\bnull\b|\bn/a\b', '', text, flags=re.I)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
