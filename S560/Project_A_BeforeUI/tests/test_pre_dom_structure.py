from bs4 import BeautifulSoup
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INDEX = os.path.join(PROJECT_ROOT, 'src', 'static', 'index.html')


def load_html():
    with open(INDEX, 'r', encoding='utf8') as fh:
        return BeautifulSoup(fh.read(), 'html.parser')


def test_title_contains_inline_ul():
    soup = load_html()
    titles = soup.select('.title')
    found = False
    for t in titles:
        if t.find('ul'):
            found = True
    assert found, 'Baseline expected to contain a malformed inline UL inside title'
