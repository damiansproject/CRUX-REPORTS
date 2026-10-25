"""The journal issue prints as an opening page, then one article per hypothesis from a new page."""
from __future__ import annotations

import io
from pathlib import Path

import pytest

sync_api = pytest.importorskip('playwright.sync_api')
pypdf = pytest.importorskip('pypdf')

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
BODY = '''<header class="masthead"><span>CRUX Hypotheses</span><span>Raynaud's phenomenon</span></header>
<h1 class="title">Fish oil and Raynaud's attacks</h1>
<ol class="contents">
  <li><span class="rank">1</span><a href="#art-1"><span class="entry-title">Viscosity title</span>
    <span class="score">86</span><span class="why">Why it ranked first.</span></a></li>
  <li><span class="rank">2</span><a href="#art-2"><span class="entry-title">Serotonin title</span>
    <span class="score">80</span><span class="why">Why it ranked second.</span></a></li>
</ol>
<article class="hyp" id="art-1"><p class="running-head">CRUX Hypotheses</p>
  <h2 class="title">Viscosity title</h2><p>Viscosity body.</p></article>
<article class="hyp" id="art-2"><p class="running-head">CRUX Hypotheses</p>
  <h2 class="title">Serotonin title</h2><p>Serotonin body.</p></article>'''


@pytest.fixture(scope='module')
def issue(tmp_path_factory):
    return print_issue(tmp_path_factory.mktemp('issue'))


def print_issue(folder: Path, body: str = BODY, css: str = '') -> 'pypdf.PdfReader':
    """Print the issue through template.html + paper.css (plus `css`) to a PDF reader."""
    html = (SCRIPTS / 'template.html').read_text(encoding='utf-8')
    for key, value in {'css': (SCRIPTS / 'paper.css').read_text(encoding='utf-8') + css,
                       'title': 'Test', 'nav': '', 'body': body}.items():
        html = html.replace('{{' + key + '}}', value)
    report = folder / 'issue.html'
    report.write_text(html, encoding='utf-8')
    with sync_api.sync_playwright() as p:
        browser = p.chromium.launch()
        tab = browser.new_page()
        tab.goto(report.as_uri())
        pdf = tab.pdf(prefer_css_page_size=True)
        browser.close()
    return pypdf.PdfReader(io.BytesIO(pdf))


def test_each_article_starts_on_a_new_page(issue) -> None:
    texts = [page.extract_text() for page in issue.pages]
    assert len(texts) == 3
    assert 'Viscosity body' in texts[1] and 'Serotonin body' not in texts[1]
    assert 'Serotonin body' in texts[2]


def footer(page) -> list[str]:
    """Text printed below the 20 mm bottom page margin (57 pt), where the page number goes."""
    found = []
    page.extract_text(visitor_text=lambda text, cm, tm, *_: text.strip() and
                      cm[1] * tm[4] + cm[3] * tm[5] + cm[5] < 57 and found.append(text.strip()))
    return found


def test_every_page_prints_its_number(issue) -> None:
    assert [footer(page) for page in issue.pages] == [['1'], ['2'], ['3']]


def test_contents_entries_jump_to_their_articles(issue) -> None:
    links = [annot.get_object() for annot in issue.pages[0].get('/Annots', [])]
    targets = {str(link['/Dest']).lstrip('/') for link in links if '/Dest' in link}
    assert targets == {'art-1', 'art-2'}
    for name, body in (('art-1', 'Viscosity body'), ('art-2', 'Serotonin body')):
        page = issue.get_destination_page_number(issue.named_destinations['/' + name])
        assert body in issue.pages[page].extract_text()
