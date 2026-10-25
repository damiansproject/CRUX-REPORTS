"""Write the CRUX Viewer sidecar for a review paper.

Reads ``<slug>_review.html`` and writes ``<slug>_review.report.json`` beside it,
so CRUX Viewer opens ``<slug>_review.pdf`` with its claim chain highlighted:
``claim_ids`` in first-citation order, and ``claim_anchors`` mapping each id to
the clause the report prints for it (the ``a.claim-link`` text).

Usage: python report_sidecar.py <run>/reports/<slug>_review.html
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

CLAIM_ID_RE = re.compile(r'clm_\S+$')  # slugs keep - and . (clm_fish-oil_0001)


class _Citations(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ''
        self.claim_ids: list[str] = []
        self.anchors: dict[str, str] = {}
        self._clause: list[str] | None = None  # text of the open a.claim-link
        self._clause_ids: list[str] = []
        self._last_clause = ''  # superscripts after a link cite that same clause
        self._h1: list[str] | None = None
        self._in_cite = False  # inside sup.cite

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == 'h1' and not self.title:
            self._h1 = []
        if tag == 'sup' and 'cite' in (a.get('class') or '').split():
            self._in_cite = True
        if tag != 'a':
            return
        match = CLAIM_ID_RE.search(a.get('href') or '')
        if 'claim-link' in (a.get('class') or '').split():
            self._clause, self._clause_ids = [], [match.group(0)] if match else []
        elif match and self._in_cite and self._last_clause:
            self._cite(match.group(0), self._last_clause)

    def handle_endtag(self, tag: str) -> None:
        if tag == 'sup':
            self._in_cite = False
        if tag == 'h1' and self._h1 is not None:
            self.title, self._h1 = ' '.join(''.join(self._h1).split()), None
        if tag == 'a' and self._clause is not None:
            self._last_clause = ' '.join(''.join(self._clause).split())
            for cid in self._clause_ids:
                self._cite(cid, self._last_clause)
            self._clause = None

    def handle_data(self, data: str) -> None:
        if self._clause is not None:
            self._clause.append(data)
        if self._h1 is not None:
            self._h1.append(data)

    def _cite(self, cid: str, clause: str) -> None:
        if cid not in self.anchors:
            self.claim_ids.append(cid)
            self.anchors[cid] = clause


def build_sidecar(html: str) -> dict[str, Any]:
    """Sidecar dict (title, claim_ids, claim_anchors) from review-paper HTML."""
    parser = _Citations()
    parser.feed(html)
    return {'title': parser.title, 'claim_ids': parser.claim_ids, 'claim_anchors': parser.anchors}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    html_path = Path(argv[0])
    sidecar = build_sidecar(html_path.read_text(encoding='utf-8'))
    if not sidecar['claim_ids']:
        print(f'{html_path}: no a.claim-link citations with clm_ ids; nothing to highlight', file=sys.stderr)
        return 1
    out = html_path.with_suffix('.report.json')
    out.write_text(json.dumps(sidecar, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'{out}: {len(sidecar["claim_ids"])} claims')
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
