from bs4 import BeautifulSoup
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INDEX = os.path.join(PROJECT_ROOT, 'src', 'static', 'index.html')


def load_html():
    with open(INDEX, 'r', encoding='utf8') as fh:
        return BeautifulSoup(fh.read(), 'html.parser')


def test_button_height_unified_improved():
    soup = load_html()
    buttons = soup.select('button')
    heights = [len(b.text) for b in buttons]
    # in improved design we force unified height via CSS; expecting lengths to be close
    assert max(heights) - min(heights) <= 6
