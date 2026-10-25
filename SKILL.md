---
name: crux-report
description: >-
  CRUX report: write skim HTML or PDF from a run’s existing artifacts. Use when
  rendering claims, proposals, critiques, hypotheses, tournament, scout, or
  review-paper pages — never to convert sources, extract claims, or run the
  hypothesis loop. At start ask presentation (required) if missing from chat
  or run.json.
---

# CRUX report

Never run conversion, extraction, generation, or tournament. Author skim HTML
under `<run>/reports/` from artifacts already on disk. Follow
[prompts/chrome.md](prompts/chrome.md). Copy `scripts/paper.css` into `<style>`
(`scripts/template.html` is the chrome). Do not invent a `<style>` block.

Human how-to: [README.md](README.md).

## Kickoff (always, this skill)

At the **start** of this skill — before writing HTML/PDF — collect what is
still missing. Skip any item the user already gave in chat **or** that is
already set in `<run>/run.json`. Re-ask only if the user changes it.

Write `<run>/run.json` when missing (create if needed). Omit keys that are not
set yet. Do not write empty strings as “unknown.”

1. **Presentation mode**, if missing (**required** for this skill).
   Professional — field jargon ok. General — plain language; define or avoid
   jargon. Presentation only affects chat and HTML; banked artifacts stay
   technically precise.
2. **Research goal**, if missing and the artifact uses it in the lead
   (hypotheses, tournament, review paper). Claims-only reports may proceed
   without it.
3. **Run mode**, if missing. Manual: wait for go-ahead after each report file
   when this skill is rendering several. Autonomous: write/refresh the needed
   reports without pausing between files.
4. If the user did not name which output, infer from the run (write/refresh
   the stage report that matches the latest artifacts). Review paper and
   literature-map HTML only when asked.

## Runtime

`<skill_root>` = `${CLAUDE_PLUGIN_ROOT}/.claude/skills/crux-report`
(plugin/Cowork) or `.claude/skills/crux-report` (this repo).

No slash workflows. Always refresh `reports/index.html` when you write a
stage file.

## Who does what

| Role | Responsibility |
| --- | --- |
| **Main (you)** | This skill’s kickoff; author HTML from on-disk artifacts using `prompts/chrome.md`; optional review paper |
| **Provided scripts** | `paper.css` and `template.html` — chrome only, no LLM |
| **Not provided** | A render script; conversion / extract / generation / tournament |

## Chrome

Follow [prompts/chrome.md](prompts/chrome.md): verifier+advocate voice,
quantified `lead-claim`, stance `tally`, hover-to-quote in CRUX Viewer (`a.claim-link` +
`sup.cite` linking each claim id).

| After these artifacts exist | File |
| --- | --- |
| `claims.jsonl` / `gists.json` | `02_claims.html` (gist per paper from `gists.json`) |
| `proposals.jsonl` | `03_proposals.html` |
| `critiques.jsonl` | `04_critiques.html` |
| Seed enrichment | `04b_seed_enrichment.html` |
| `hypotheses.jsonl` | `05_hypotheses.html` |
| Tournament cycle (judge) | `06_tournament.html` |
| Web scout (if used) | `01_web_scout.html` |
| Literature map (if used) | `literature_map.html` |
| Review paper: a journal issue (if asked) | `<slug>_review.html` + `.pdf` |

## Review paper (only when asked)

A journal issue: a summary page, then one short article per hypothesis on
what it combines and why.
Follow [prompts/review-paper.md](prompts/review-paper.md); author HTML using
`paper.css`. Suggested: `opus` / `high`.

## Invariants

- Never convert sources, extract claims, or run propose/critique/revise/judge.
- Do not invent quotes, sources, or counts — use stored `quotes` and artifact
  ids.
- Presentation from `run.json` / kickoff applies to jargon in the HTML.
- Manual run mode waits for go-ahead after each report file when writing
  several in one invoke.
