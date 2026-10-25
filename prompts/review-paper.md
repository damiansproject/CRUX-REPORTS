# Review paper: a journal issue (optional tool)

Only when the user asks for a review / scoping paper / printable PDF. Not a core
CRUX stage.

The paper is laid out as a **journal issue**: an opening page that summarises
the issue, then one short article per final hypothesis, in rank order. What a
researcher wants from each article is the idea: which findings the hypothesis
combines, and why that combination answers the question. Each article leads
with that, then backs it up and says why it ranked where it did. Articles
follow the shape of a Frontiers "Hypothesis and Theory" article: the
hypothesis is argued from existing evidence, not from new experiments.

The look is `scripts/paper.css`. Author the HTML yourself (`scripts/template.html`
is the chrome; fill `{{title}}`, `{{css}}`, `{{nav}}` and `{{body}}` by hand).
Do not invent a `<style>` block — copy `paper.css` into it. Where this file and
[chrome.md](chrome.md) differ, this file wins for the journal issue: it has no
stance tally, and its lead names the top-ranked hypothesis, not a next step.

## Inputs (this run's artifacts only)

| What | Where |
| --- | --- |
| Research question | `run.json` `research_goal` |
| Hypotheses | `hypotheses.jsonl`: `statement`, `mechanism`, `claim_chain`, `dependency_claim_ids`, `critique_id` |
| Rank, score, judge's reasons | the latest `tournament/ranking_round_<n>.json`: `ranked_ids`, `scores`, `rationale` |
| Weak links | `critiques.jsonl` row whose `id` is the hypothesis's `critique_id`: `verdict`, `issues`, `unsupported_hops` |
| Quotes | `claims.jsonl`: each claim's `statement` and stored `quotes` |
| Paper titles | `cleaned_jsons/index.json` (`paper_id` → `title`) |

A `claim_chain` link is either `kind: "extracted"` — a banked claim
(`claim_id`, plus a `note` on its role) — or `kind: "conjecture"` — the new
connection the hypothesis proposes (`statement`, `note`, joining
`from_claim_id` to `to_claim_id`). The conjecture is not a banked claim: present
it as the hypothesis's own unproven step, say so, and cite the two claims it
joins, each on the phrase that names it (never one cite on the whole
conjecture, which would show a quote as proof of the unproven step).

**No study design anywhere.** Never use `experimental_plan` or a conjecture's
`kill_experiment`, and leave out any design detail inside `mechanism` (pilots,
arms, sample sizes, schedules, endpoints to measure, "for this experiment").
The issue contains no protocol and no "next experiment". Where feasibility
matters, argue it from what the cited papers already show (a dose that has
been given, a target that has been measured).

## Rules for every article

- **Each article stands alone.** It never names, compares with or points to
  another hypothesis or article ("like article 2", "a broader variant"). It
  reads as a complete paper on its own.
- **Why it ranked** restates the judge's reasons that concern this hypothesis
  itself — its evidence, its fit to the question, how specific it is — in its
  own terms. Drop the judge's comments on its plan without mentioning them,
  and never rank it against the others in words; the rank and score say that.
  If little is left once the plan comments are gone, keep the section short
  rather than pad it.
- Cite inside the prose with hover-to-quote links ([chrome.md](chrome.md) item
  3); every load-bearing sentence carries a cite to a claim banked in this run.
  A superscript's number is the cited paper's number in that article's
  References; when two claims from one paper support a clause, cite the
  stronger one.
- Do not invent sources, quotes, numbers or titles. Reference entries give
  what the run holds: the paper's title, then whichever of venue, PMID and URL
  its claims' `source` has, numbered in order of first cite. Authors and years
  only if the run has them.
- **Concise.** About 900–1,400 words per article, references excluded.
  Paragraphs of at most four sentences; say each thing once.

## Structure

`<slug>` is a short snake_case name for the research topic, e.g.
`fish_oil_raynaud`. Write `<run>/reports/<slug>_review.html`.

**Opening page** (one printed page)

1. `<header class="masthead">` — `<span>CRUX Hypotheses</span><span>{topic} · {month year}</span>`.
2. `<h1 class="title">` — the issue's title.
3. The research question, quoted from `run.json`, in a `<blockquote>`.
4. **Editor's summary** — `<p class="lead-claim">`: what the issue holds and
   how much evidence (hypotheses, papers, claims), the top-ranked hypothesis in
   one clause, and the overall shape of the answer. This is the one place the
   issue is described as a whole. Say here, once, that this is an
   **AI-assisted hypothesis synthesis**, not a systematic review. The opening
   page carries no cites and no stance tally; the articles carry the evidence.
5. **In this issue** — `<ol class="contents">`, one `<li>` per hypothesis in
   rank order: `<span class="rank">N</span><a href="#art-N"><span class="entry-title">…</span>
   <span class="score">score</span><span class="why">one line on why it ranked here</span></a>`.
   The `why` line follows the stand-alone rule above. The links become
   clickable jumps in the PDF.

**One `<article class="hyp" id="art-N">` per hypothesis** (each prints from a
new page; page numbers print in the footer)

1. `<p class="running-head"><span>CRUX Hypotheses · {topic}</span><span>Article N</span></p>`
2. `<h2 class="title">` — a plain-language title naming the intervention, the
   patients and the outcome.
3. `<p class="byline">` — `<span class="score">Rank N · score</span>` AI-assisted
   hypothesis synthesis · {papers} papers · {claims} cited claims (every
   distinct claim the article cites, and the papers they come from).
4. `<div class="abstract">` — **the idea in brief**, about 100 words, no
   citations: the findings the hypothesis combines, the new link it proposes
   between them, and why that combination is a promising answer to the
   question. A reader who stops here knows what is combined and why.
5. `<p class="keywords">` — 5–8 keywords.
6. Sections as `<h3>`, each short:
   1. **Relevance to the question** — one paragraph: how the hypothesis
      answers each part of the question (the intervention, who it is for, the
      outcome, the mechanism).
   2. **Background** — one paragraph: the condition and the biology the
      hypothesis acts on.
   3. **The chain of evidence** — an `<ol>` with one item per `claim_chain`
      link, in order: in one or two sentences, what the study found (cited)
      and which step of the mechanism it carries. The conjecture's item opens
      with "Proposed link (untested):".
   4. **Why this is a specific, feasible combination** — one paragraph: what
      makes it specific (dose, duration, population, outcome) and why it is
      within reach on current evidence.
   5. **Why it ranked here** — the score and the reasons for it, in at most
      four sentences.
   6. **Limitations and open questions** — a `<ul>`, one line per weak link or
      missing piece of evidence, from the critique's `issues` and
      `unsupported_hops`. An issue that asks for a change to the study becomes
      the evidence gap behind it.
   7. **References** — `<ol class="refs">` of the papers this article cites.

## Flow

1. Author the HTML as above. The issue is long: write the head and opening
   page first, then add one article per write.
2. Print to PDF with Edge or Chrome:
   `msedge --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=<run>/reports/<slug>_review.pdf <run>/reports/<slug>_review.html`
   (on Windows without `msedge` on PATH:
   `"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"`).
   `@media print` in `paper.css` is the PDF page.
3. Write the CRUX Viewer sidecar:
   `python <skill_root>/scripts/report_sidecar.py <run>/reports/<slug>_review.html`.
   It writes `<slug>_review.report.json` (`claim_ids` in citation order,
   `claim_anchors` = each claim's `claim-link` clause), so CRUX Viewer opens the
   PDF with its claim chain highlighted and each clause linked to its source
   quote. A nonzero exit means the HTML has no `claim-link` cites: fix the HTML.
   Re-run it after any edit to the HTML.
4. Link from `reports/index.html` (if missing, write it in the same chrome: a
   title and one link per report file).

Suggested authoring: `opus` / `high`.
