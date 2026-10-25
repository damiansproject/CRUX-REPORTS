from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from report_sidecar import build_sidecar  # noqa: E402

REVIEW = '''<!doctype html><html><head><title>Fish oil and Raynaud</title></head><body>
<h1>Fish oil and Raynaud: a scoping review</h1>
<p>Omega-3 intake <a class="claim-link" href="#q-hyp_001-clm_p_two_0004">lowers
  vasospasm frequency</a><sup class="cite"><a href="#q-hyp_001-clm_p_two_0004">1</a></sup>
  and <a class="claim-link" href="#q-hyp_001-clm_p_one_0001">raises <em>digital</em> blood flow</a><sup
  class="cite"><a href="#q-hyp_001-clm_p_one_0001">2</a></sup><sup class="cite"><a
  href="#q-hyp_001-clm_p_one_0009">3</a></sup>.</p>
<figure class="quote-cite" id="q-hyp_001-clm_p_two_0004"><blockquote>banked quote</blockquote></figure>
<p>Again <a class="claim-link" href="#q-hyp_002-clm_p_two_0004">a later clause</a>.</p>
</body></html>'''


def test_claim_ids_follow_first_citation_order_without_duplicates() -> None:
    assert build_sidecar(REVIEW)['claim_ids'] == ['clm_p_two_0004', 'clm_p_one_0001', 'clm_p_one_0009']


def test_each_claim_anchors_on_its_first_clause_as_printed() -> None:
    anchors = build_sidecar(REVIEW)['claim_anchors']
    # whitespace collapsed, inline markup flattened; the later re-cite does not move the anchor
    assert anchors == {
        'clm_p_two_0004': 'lowers vasospasm frequency',
        'clm_p_one_0001': 'raises digital blood flow',
        'clm_p_one_0009': 'raises digital blood flow',  # adjacent superscript shares the clause
    }


def test_title_comes_from_the_h1() -> None:
    assert build_sidecar(REVIEW)['title'] == 'Fish oil and Raynaud: a scoping review'


def test_cli_writes_sidecar_next_to_the_review(tmp_path: Path) -> None:
    html = tmp_path / 'fishoil_review.html'
    html.write_text(REVIEW, encoding='utf-8')
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'report_sidecar.py'), str(html)], check=True)
    data = json.loads((tmp_path / 'fishoil_review.report.json').read_text(encoding='utf-8'))
    assert data['claim_ids'][0] == 'clm_p_two_0004'


def test_review_without_citations_is_an_error(tmp_path: Path) -> None:
    html = tmp_path / 'empty_review.html'
    html.write_text('<h1>t</h1><p>no cites</p>', encoding='utf-8')
    run = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'report_sidecar.py'), str(html)],
                         capture_output=True, text=True, encoding='utf-8')
    assert run.returncode != 0 and 'claim-link' in run.stderr
    assert not (tmp_path / 'empty_review.report.json').exists()


def test_claim_ids_keep_slug_punctuation() -> None:
    html = '<p><a class="claim-link" href="#q-hyp_001-clm_fish-oil.v2_0001">reduces vasospasm</a></p>'
    assert build_sidecar(html)['claim_anchors'] == {'clm_fish-oil.v2_0001': 'reduces vasospasm'}


def test_only_claim_links_and_cite_superscripts_count() -> None:
    html = ('<nav class="crumb"><a href="02_claims.html#clm_p_one_0001">Source claim</a></nav>'
            '<p>Intake <a class="claim-link" href="#q-hyp_001-clm_p_one_0001">reduces vasospasm</a></p>')
    assert build_sidecar(html)['claim_anchors'] == {'clm_p_one_0001': 'reduces vasospasm'}


def test_superscript_without_a_clause_is_not_a_citation() -> None:
    html = '<p>Text<sup class="cite"><a href="#q-hyp_001-clm_p_one_0001">1</a></sup></p>'
    assert build_sidecar(html)['claim_ids'] == []


def test_viewer_claim_links_give_the_same_ids_and_anchors() -> None:
    crux_local = REVIEW.replace('#q-hyp_001-', 'https://crux.local/claim/').replace('#q-hyp_002-', 'https://crux.local/claim/')
    assert build_sidecar(crux_local)['claim_ids'] == build_sidecar(REVIEW)['claim_ids']
    assert build_sidecar(crux_local)['claim_anchors'] == build_sidecar(REVIEW)['claim_anchors']
