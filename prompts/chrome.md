# CRUX report chrome

Author skim-friendly HTML under `<run>/reports/`. No report script — you
author the HTML. Copy `scripts/paper.css` into `<style>` (`scripts/template.html`
is the chrome). Do not invent a `<style>` block.

## Voice

Reports are a **verifier + advocate**, not a helper persona.

- **Third person, corpus-attributed.** “Twelve claims from four papers support
  …”. Never “I”, “we found”, “let’s”, “exciting”, or “as an AI”.
- **Lead is a bet with counts:** first sentence states what
  to do next *and* the evidence size. Do not hedge that sentence with
  may / might / could / potentially. Residual doubt goes in a short Limitations
  stretch after the case.
- **Verifier, not theatre.** Every claim must be checkable at a glance:
  hover the statement in CRUX Viewer → the source quote. “Forty studies report that…”
  — name the count; do not narrate “searching…” / “synthesizing…”.
- **Stance words:** **supporting** / **mentioning** / **contradicting**. Do
  not invent a Yes/No meter.
- Presentation mode still applies to jargon (`run.json` `presentation`).

## Required chrome (classes already in `paper.css`)

1. **Quantified lead** — `<p class="lead-claim">` immediately under the title.
   Example shape: “Among 9 revised hypotheses (4 papers, 18 claims), rank 1 is
   … because …”.
2. **Tally** — `<p class="tally" aria-label="…">` with
   `<span class="tally-item supporting|mentioning|contradicting"><i></i> N …</span>`
   plus optional `<span class="tally-meta">N papers · M claims</span>`.
   Count from this run’s artifacts only:
   - **supporting** — claim ids used in a hypothesis `claim_chain` /
     `dependency_claim_ids`
   - **mentioning** — other banked claims not used in a chain
   - **contradicting** — critique `issues` + `unsupported_hops` (and revise
     `needs_claims` gaps if still open)
3. **In-text citations (hover-to-quote in CRUX Viewer).** Cites live **inside the
   argument prose** — statement, mechanism, and evidence — on the clause they support.
   Wrap that clause in `<a class="claim-link" href="https://crux.local/claim/<claim_id>">…</a>`
   plus `<sup class="cite"><a href="https://crux.local/claim/<claim_id>">n</a></sup>`.
   CRUX Viewer reads these links from the PDF: hovering the clause shows that
   claim's stored quote, and its sidebar lists every claim. The report itself
   carries no quote boxes or popovers. Two (or more) sources on **one sentence**
   is allowed: keep one `claim-link` on the clause, then adjacent superscripts
   (`<sup class="cite">1</sup><sup class="cite">2</sup>`), each `href` a
   different claim. Cite only claims banked in this run — their stored `quotes`
   are what the viewer shows; do not invent text. If a sentence has no quote,
   do not write it as load-bearing.
   **Not citations:** wrapping the whole statement as one link; putting every
   cite only in a `<details>` list; a bibliography after an uncited mechanism.
4. **Type** — argument body stays Georgia; tallies, badges, captions, crumbs,
   and ids use the sans stack in `paper.css`.
