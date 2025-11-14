"""Utility functions for layout measurements and validation."""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class LayoutMetrics:
    """Container for layout measurement data."""
    spacing_variance: float
    button_heights: List[int]
    item_paddings: List[int]
    gaps: List[float]
    alignment_errors: List[str]
    css_rules: Dict[str, str]

def extract_css_value(css_string: str, property_name: str) -> Optional[str]:
    """Extract a single CSS property value from a CSS string."""
    pattern = rf'{property_name}\s*:\s*([^;]+);'
    match = re.search(pattern, css_string)
    return match.group(1).strip() if match else None

def parse_spacing_value(value: str) -> float:
    """Convert CSS spacing value to pixels."""
    value = value.strip()
    if 'px' in value:
        return float(value.replace('px', ''))
    elif 'rem' in value:
        return float(value.replace('rem', '')) * 16  # Assuming base font-size of 16px
    elif 'em' in value:
        return float(value.replace('em', '')) * 16
    return 0.0

def calculate_spacing_variance(spacings: List[float]) -> float:
    """Calculate variance in spacing values."""
    if len(spacings) < 2:
        return 0.0
    mean = sum(spacings) / len(spacings)
    variance = sum((x - mean) ** 2 for x in spacings) / len(spacings)
    return variance ** 0.5

def validate_button_consistency(buttons: List[Dict]) -> Tuple[bool, List[str]]:
    """Validate that all buttons have consistent height, width, and styling."""
    errors = []
    
    if not buttons:
        return True, errors
    
    heights = [b.get('height') for b in buttons]
    widths = [b.get('width') for b in buttons]
    padding = [b.get('padding') for b in buttons]
    
    # Check height consistency
    if len(set(heights)) > 1:
        errors.append(f"Inconsistent button heights: {set(heights)}")
    
    # Check width consistency (for same-type buttons)
    if len(set(widths)) > 1:
        errors.append(f"Inconsistent button widths: {set(widths)}")
    
    return len(errors) == 0, errors

def validate_icon_alignment(elements: List[Dict]) -> Tuple[bool, List[str]]:
    """Validate that icons are properly aligned within their containers."""
    errors = []
    
    for elem in elements:
        if elem.get('type') == 'icon':
            display = elem.get('display')
            align_items = elem.get('align_items')
            justify_content = elem.get('justify_content')
            
            if display not in ['flex', 'inline-flex']:
                errors.append(f"Icon not using flex layout: {display}")
            if align_items != 'center':
                errors.append(f"Icon alignment-items not centered: {align_items}")
    
    return len(errors) == 0, errors

def validate_dom_structure(dom_tree: Dict) -> Tuple[bool, List[str]]:
    """Validate DOM structure for proper nesting and semantics."""
    errors = []
    
    def check_element(elem, depth=0):
        if not elem:
            return
        
        tag = elem.get('tag', '')
        children = elem.get('children', [])
        
        # Check for orphaned elements
        if depth > 10:
            errors.append(f"Deep nesting detected (depth > 10): {tag}")
        
        # Check semantic correctness
        if tag == 'li' and elem.get('parent') not in ['ul', 'ol']:
            errors.append("List item <li> not inside <ul> or <ol>")
        
        # Recursively check children
        for child in children:
            check_element(child, depth + 1)
    
    check_element(dom_tree)
    return len(errors) == 0, errors

def validate_spacing_consistency(items: List[Dict], tolerance_px: float = 2.0) -> Tuple[bool, List[str]]:
    """Validate that spacing between items is consistent."""
    errors = []
    
    spacings = []
    for item in items:
        padding = parse_spacing_value(item.get('padding', '0'))
        margin = parse_spacing_value(item.get('margin', '0'))
        spacings.append(padding + margin)
    
    if len(spacings) >= 2:
        variance = calculate_spacing_variance(spacings)
        if variance > tolerance_px:
            errors.append(f"Spacing variance ({variance:.2f}px) exceeds tolerance ({tolerance_px}px)")
    
    return len(errors) == 0, errors

def measure_hover_feedback_latency(browser_perf_data: Dict) -> float:
    """Measure the time between hover event and visual feedback appearance."""
    # This would typically involve analyzing browser performance data
    # For now, return a placeholder
    if 'entries' in browser_perf_data:
        entries = browser_perf_data['entries']
        if entries:
            return entries[0].get('duration', 0)
    return 0.0

def validate_malformed_input_handling(input_data: Dict) -> Tuple[bool, List[str]]:
    """Validate that malformed inputs are handled gracefully."""
    errors = []
    
    if input_data.get('title') == '' and input_data.get('id') is None:
        if not input_data.get('fallback_applied'):
            errors.append("No fallback applied for missing title and id")
    
    return len(errors) == 0, errors

def generate_layout_report(metrics: LayoutMetrics) -> Dict:
    """Generate a comprehensive layout validation report."""
    return {
        'spacing_variance': metrics.spacing_variance,
        'button_heights': metrics.button_heights,
        'item_paddings': metrics.item_paddings,
        'gaps': metrics.gaps,
        'alignment_errors': metrics.alignment_errors,
        'css_rules': metrics.css_rules,
        'passed': len(metrics.alignment_errors) == 0
    }
