# CRUX Reports

HTML output of a CRUX run. Pages for claims, proposals, critiques, hypotheses,
and the tournament.

## Works with

| Host        | Status      |
|-------------|-------------|
| [Claude Code](https://claude.com/claude-code) | Supported |
| Codex       | In progress |
| Claude Cowork | In progress |

## Install

Clone it into the skills folder of a CRUX checkout, from inside the CRUX folder:

```bash
git clone https://github.com/damiansproject/CRUX-REPORTS.git .claude/skills/crux-report
```

Install it only there, under exactly that name; the CRUX skills find each other
by these paths. The [CRUX quickstart](https://github.com/damiansproject/CRUX#quickstart)
installs the whole suite this way.

## Usage

```
/crux-report
```

Pages land in the run's `reports/`, starting at `reports/index.html`. The other
CRUX skills call it after each stage. Ask for the review paper to get one
paper-style page of the whole run, with a PDF.

## The CRUX suite

| Repo | Stage |
|------|-------|
| [CRUX Claims](https://github.com/damiansproject/CRUX-CLAIMS) | Sources → atomic claim bank |
| [CRUX](https://github.com/damiansproject/CRUX) | Hypothesis loop: propose → critique → revise → tournament |
| **CRUX Reports** (this repo) | Skim HTML / PDF pages of a run |
| [CRUX Viewer](https://github.com/damiansproject/CRUX-VIEWER) | Claim quotes highlighted on the original sources |
