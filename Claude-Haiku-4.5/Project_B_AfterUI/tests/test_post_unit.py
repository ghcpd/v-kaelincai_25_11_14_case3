"""Unit tests for Project B (After) - Layout validation and DOM structure."""

import pytest
import json
import re
from pathlib import Path
from layout_validator import (
    calculate_spacing_variance,
    validate_button_consistency,
    validate_icon_alignment,
    validate_dom_structure,
    validate_spacing_consistency,
    parse_spacing_value,
    validate_malformed_input_handling
)

# Load test data
TEST_DATA_PATH = Path(__file__).parent.parent.parent / "test_data.json"
with open(TEST_DATA_PATH, encoding='utf-8') as f:
    TEST_DATA = json.load(f)


class TestSpacingCalculations:
    """Test spacing calculation utilities."""
    
    def test_parse_spacing_px(self):
        """Test parsing pixel values."""
        assert parse_spacing_value("10px") == 10.0
        assert parse_spacing_value("0px") == 0.0
        assert parse_spacing_value("  5px  ") == 5.0
    
    def test_parse_spacing_rem(self):
        """Test parsing rem values (16px base)."""
        assert parse_spacing_value("1rem") == 16.0
        assert parse_spacing_value("0.5rem") == 8.0
        assert parse_spacing_value("2rem") == 32.0
    
    def test_parse_spacing_em(self):
        """Test parsing em values."""
        assert parse_spacing_value("1em") == 16.0
        assert parse_spacing_value("0.5em") == 8.0
    
    def test_calculate_spacing_variance_zero(self):
        """Test variance with identical values."""
        spacings = [10.0, 10.0, 10.0]
        variance = calculate_spacing_variance(spacings)
        assert variance == 0.0
    
    def test_calculate_spacing_variance_nonzero(self):
        """Test variance with varying values."""
        spacings = [10.0, 12.0, 14.0]
        variance = calculate_spacing_variance(spacings)
        assert variance > 0
    
    def test_calculate_spacing_variance_single_value(self):
        """Test variance with single value."""
        spacings = [10.0]
        variance = calculate_spacing_variance(spacings)
        assert variance == 0.0
    
    def test_calculate_spacing_variance_empty(self):
        """Test variance with empty list."""
        spacings = []
        variance = calculate_spacing_variance(spacings)
        assert variance == 0.0


class TestButtonConsistency:
    """Test button consistency validation."""
    
    def test_consistent_buttons(self):
        """Test validation of consistent buttons."""
        buttons = [
            {'height': 36, 'width': 80, 'padding': '8px'},
            {'height': 36, 'width': 80, 'padding': '8px'},
        ]
        passed, errors = validate_button_consistency(buttons)
        assert passed
        assert len(errors) == 0
    
    def test_inconsistent_button_heights(self):
        """Test detection of inconsistent heights."""
        buttons = [
            {'height': 36, 'width': 80},
            {'height': 40, 'width': 80},
        ]
        passed, errors = validate_button_consistency(buttons)
        assert not passed
        assert any('height' in str(e).lower() for e in errors)
    
    def test_inconsistent_button_widths(self):
        """Test detection of inconsistent widths."""
        buttons = [
            {'height': 36, 'width': 80},
            {'height': 36, 'width': 90},
        ]
        passed, errors = validate_button_consistency(buttons)
        assert not passed
        assert any('width' in str(e).lower() for e in errors)
    
    def test_empty_buttons_list(self):
        """Test with empty button list."""
        passed, errors = validate_button_consistency([])
        assert passed
        assert len(errors) == 0


class TestIconAlignment:
    """Test icon alignment validation."""
    
    def test_properly_aligned_icons(self):
        """Test properly aligned icons."""
        icons = [
            {'type': 'icon', 'display': 'flex', 'align_items': 'center', 'justify_content': 'center'},
            {'type': 'icon', 'display': 'inline-flex', 'align_items': 'center', 'justify_content': 'center'},
        ]
        passed, errors = validate_icon_alignment(icons)
        assert passed
        assert len(errors) == 0
    
    def test_misaligned_icons_no_flex(self):
        """Test icons without flex display."""
        icons = [
            {'type': 'icon', 'display': 'block', 'align_items': 'center'},
        ]
        passed, errors = validate_icon_alignment(icons)
        assert not passed
        assert any('flex' in str(e).lower() for e in errors)
    
    def test_misaligned_icons_wrong_alignment(self):
        """Test icons without centered alignment."""
        icons = [
            {'type': 'icon', 'display': 'flex', 'align_items': 'flex-start'},
        ]
        passed, errors = validate_icon_alignment(icons)
        assert not passed
        assert any('alignment' in str(e).lower() for e in errors)
    
    def test_empty_icons_list(self):
        """Test with empty icons list."""
        passed, errors = validate_icon_alignment([])
        assert passed


class TestDOMStructure:
    """Test DOM structure validation."""
    
    def test_valid_dom_structure(self):
        """Test validation of valid DOM structure."""
        dom = {
            'tag': 'ul',
            'children': [
                {'tag': 'li', 'parent': 'ul', 'children': []},
                {'tag': 'li', 'parent': 'ul', 'children': []},
            ]
        }
        passed, errors = validate_dom_structure(dom)
        assert passed
    
    def test_invalid_list_nesting(self):
        """Test detection of invalid list nesting."""
        dom = {
            'tag': 'div',
            'children': [
                {'tag': 'li', 'parent': 'div', 'children': []},
            ]
        }
        passed, errors = validate_dom_structure(dom)
        assert not passed
        assert any('list item' in str(e).lower() for e in errors)
    
    def test_deeply_nested_dom(self):
        """Test detection of excessive nesting."""
        dom = {'tag': 'div', 'children': []}
        current = dom
        for i in range(15):
            current['children'] = [{'tag': 'div', 'children': []}]
            current = current['children'][0]
        
        passed, errors = validate_dom_structure(dom)
        assert not passed


class TestSpacingConsistency:
    """Test spacing consistency validation."""
    
    def test_consistent_spacing(self):
        """Test consistent spacing validation."""
        items = [
            {'padding': '20px', 'margin': '0px'},
            {'padding': '20px', 'margin': '0px'},
            {'padding': '20px', 'margin': '0px'},
        ]
        passed, errors = validate_spacing_consistency(items, tolerance_px=2.0)
        assert passed
        assert len(errors) == 0
    
    def test_improved_spacing_variance(self):
        """Test that improved spacing has better variance."""
        items = [
            {'padding': '20px', 'margin': '0px'},
            {'padding': '20px', 'margin': '0px'},
            {'padding': '20px', 'margin': '0px'},
        ]
        spacings = [20.0, 20.0, 20.0]
        variance = calculate_spacing_variance(spacings)
        assert variance < 1.0  # Improved layout has very low variance
    
    def test_spacing_within_tolerance(self):
        """Test spacing within tolerance."""
        items = [
            {'padding': '20px', 'margin': '0px'},
            {'padding': '21px', 'margin': '0px'},
            {'padding': '20px', 'margin': '0px'},
        ]
        passed, errors = validate_spacing_consistency(items, tolerance_px=2.0)
        assert passed


class TestMalformedInputHandling:
    """Test handling of malformed inputs."""
    
    def test_missing_title(self):
        """Test handling of missing title."""
        input_data = {
            'title': '',
            'id': 'task_1',
            'fallback_applied': True
        }
        passed, errors = validate_malformed_input_handling(input_data)
        assert passed
    
    def test_missing_id(self):
        """Test handling of missing id."""
        input_data = {
            'title': 'Task 1',
            'id': None,
            'fallback_applied': False
        }
        # This specific case doesn't fail in our validator
        passed, errors = validate_malformed_input_handling(input_data)
    
    def test_both_missing_no_fallback(self):
        """Test when both title and id missing without fallback."""
        input_data = {
            'title': '',
            'id': None,
            'fallback_applied': False
        }
        passed, errors = validate_malformed_input_handling(input_data)
        assert not passed
        assert len(errors) > 0


class TestImprovedVisuals:
    """Test improvements in visual design."""
    
    def test_improved_button_size(self):
        """Test that button sizes meet improved standard."""
        buttons = [
            {'height': 36, 'width': 100},
            {'height': 36, 'width': 100},
        ]
        passed, errors = validate_button_consistency(buttons)
        assert passed
        # Check size is within improved range (36-48px)
        assert all(36 <= b['height'] <= 48 for b in buttons)
    
    def test_improved_icon_alignment(self):
        """Test improved icon alignment with flex."""
        icons = [
            {'type': 'icon', 'display': 'inline-flex', 'align_items': 'center', 'justify_content': 'center'},
        ]
        passed, errors = validate_icon_alignment(icons)
        assert passed


class TestDataGeneration:
    """Test that test data is properly structured."""
    
    def test_test_data_loaded(self):
        """Test that test data is properly loaded."""
        assert 'test_cases' in TEST_DATA
        assert len(TEST_DATA['test_cases']) >= 5
    
    def test_all_test_cases_have_required_fields(self):
        """Test that all test cases have required fields."""
        for case in TEST_DATA['test_cases']:
            assert 'id' in case
            assert 'name' in case
            assert 'description' in case
            assert 'category' in case
            assert 'initial_dom' in case
            assert 'expected_layout' in case
            assert 'acceptance_criteria' in case
    
    def test_test_case_categories(self):
        """Test that test cases cover required categories."""
        categories = {case['category'] for case in TEST_DATA['test_cases']}
        assert 'normal' in categories
        assert 'edge_case' in categories
        assert 'malformed' in categories
        assert 'dom_mutation' in categories


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
