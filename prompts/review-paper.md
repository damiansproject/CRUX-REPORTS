# Review paper (optional tool)

Only when the user asks for a review / scoping paper / printable PDF. Not a core
CRUX stage.

The look is `scripts/paper.css`. Author the HTML yourself (`scripts/template.html`
is the chrome). Do not invent a `<style>` block — copy `paper.css` into it.

## Flow

1. Author `<run>/reports/<slug>_review.html` from the run’s claims /
   hypotheses / goal. Same **voice + chrome** as [chrome.md](chrome.md): quantified
   `lead-claim`, stance `tally`, click-to-quote (`a.claim-link` +
   `figure.quote-cite` with `<mark>` on the supporting clause). Argue for a
   research program. Say once that it is
   an **AI-assisted scoping synthesis**, not a PRISMA systematic review — then
   make the case. Do not invent sources or numbers. Put limits in a short
   Limitations stretch (not in the lead).
2. Print from the browser (or Edge/Chrome `--print-to-pdf`); `@media print` in
   `paper.css` is the PDF page. Save it as `<run>/reports/<slug>_review.pdf`.
3. Write the CRUX Viewer sidecar:
   `python <skill_root>/scripts/report_sidecar.py <run>/reports/<slug>_review.html`.
   It writes `<slug>_review.report.json` (`claim_ids` in citation order,
   `claim_anchors` = each claim's `claim-link` clause), so CRUX Viewer opens the
   PDF with its claim chain highlighted and each clause linked to its source
   quote. A nonzero exit means the HTML has no `claim-link` cites: fix the HTML.
   Re-run it after any edit to the HTML.
4. Link from `reports/index.html`.

Suggested authoring: `opus` / `high`.
