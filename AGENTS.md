# zero-dollar-seo: agent instructions

This repository turns an AI coding agent (Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot and others) into an SEO and content assistant that works on the data Google gives every site owner for free:
- Search Console: which searches bring people to the site.
- Google Analytics: what they do after they arrive, including visits from ChatGPT and other AI assistants.
- Google Autocomplete and Keyword Planner: what people search for.
- A crawler that audits the site.

The goal is to give a small business the core of a paid SEO suite without paying one.

## When this folder is opened
- If `config/site.json` does not exist, greet the user in one sentence and start the onboarding in `workflows/setup.md` right away.
- If it exists, read it and `content/runlog.md` (if present). Say in two sentences where things stand, then offer the next useful step: the cycle, the audit or the report.

## What the user can ask, in any agent
| The user says something like | Do this |
|---|---|
| "set up", "start", "onboard me", "set up zero-dollar-seo" | `workflows/setup.md` |
| "run the cycle", "next articles", "do the two-week run" | `workflows/cycle.md` |
| "audit my site", "what's broken" | `workflows/audit.md` |
| "how are we doing", "report" | `workflows/report.md` |

In Claude Code the same workflows are also slash commands: `/seo-setup`, `/seo-cycle`, `/seo-audit`, `/seo-report`.

## Rules
- **Real data only.** Every recommendation names the number it comes from: a query with its impressions and position, or a page with its CTR. Never invent statistics, rankings, search volumes or results.
- **Ask before changing the live site.** Show the exact change, before and after, and apply it only after the user says yes. The default publishing mode is a draft.
- **Secrets stay in `secrets/`.** Never print, paste or commit keys or passwords, and never put them in URLs.
- **Plain language.** The user may not know SEO terms. The first time you use one (CTR, impressions, orphan page), explain it in a short sentence.
- **Quality over volume.** One genuinely useful article per week beats five thin ones. Never publish a near-duplicate of an existing page (check `content/ledger.md`).
- **Links ship with the article.** Add internal links in the same session (`prompts/interlinks.md`), never as a later job.
- **Verify, don't trust a status.** After publishing, scheduling or an automatic run, check the result itself: the page, the CMS or the run log entry.

## Map
- `workflows/` holds the step-by-step procedures: setup, cycle, audit, report.
- `prompts/` covers:
  - how to choose topics
  - how to write articles that Google ranks and AI assistants quote
  - how to add internal links
  - how to rewrite titles that nobody clicks
- `scripts/` (Python 3.10+, `pip install -r requirements.txt`):
  - `check_access.py`
  - `gsc_pull.py`
  - `ga4_pull.py`
  - `autocomplete_harvest.py`
  - `merge_volumes.py`
  - `crawl.py`
  - `wp_publish.py` (optional)
- `config/site.json` holds everything about the business and is created during onboarding.
- `data/`, `reports/` and `content/` hold the outputs.
