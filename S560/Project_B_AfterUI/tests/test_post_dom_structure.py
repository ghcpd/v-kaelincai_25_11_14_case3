from bs4 import BeautifulSoup
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INDEX = os.path.join(PROJECT_ROOT, 'src', 'static', 'index.html')


def load_html():
    with open(INDEX, 'r', encoding='utf8') as fh:
        return BeautifulSoup(fh.read(), 'html.parser')


def test_title_does_not_contain_inline_ul():
    soup = load_html()
    titles = soup.select('.title')
    for t in titles:
        assert not t.find('ul'), 'Title element contains a nested UL which is invalid inline placement'
