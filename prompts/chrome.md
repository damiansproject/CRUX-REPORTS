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
- **Verifier, not theatre.** Every claim must be checkable in one click:
  click the statement → the source quote. “Forty studies report that…”
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
3. **In-text citations (click-to-quote).** Cites live **inside the argument
   prose** — statement, mechanism, and plan — on the clause they support.
   Wrap that clause in `<a class="claim-link" href="#q-…">…</a>` plus
   `<sup class="cite"><a href="#q-…">n</a></sup>`. Two (or more) sources on
   **one sentence** is allowed: keep one `claim-link` on the clause, then
   adjacent superscripts (`<sup class="cite">1</sup><sup class="cite">2</sup>`),
   each `href` a different figure. After **that same paragraph**, put one
   `<figure class="quote-cite" id="q-…">` per cited claim (sibling, not
   inside `<p>`). Figure ids must be unique on the page (`q-<hyp_or_prp>-<claim_id>`).
   Figcaption starts with `<a class="quote-close" href="#!" aria-label="Close">×</a>`
   then `<span class="quote-title">Supporting quotes</span>` (or Mentioning /
   Contradicting quotes), then `<span class="stance supporting">supporting</span>`
   + claim id + paper. `<blockquote>` uses `<mark>` on the clause that supports
   the sentence. Screen CSS shows the figure as a popover on click (`:target`);
   print shows every card. Use the claim’s stored `quotes` — do not invent text.
   If a sentence has no quote, do not write it as load-bearing. Include
   `template.html`’s click-outside script (chrome).
   **Not citations:** wrapping the whole statement as one link; putting every
   cite only in a `<details>` list; a bibliography after an uncited mechanism.
4. **Type** — argument body stays Georgia; tallies, badges, captions, crumbs,
   and ids use the sans stack in `paper.css`.
