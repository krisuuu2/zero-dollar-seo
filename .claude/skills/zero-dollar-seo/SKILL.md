---
name: zero-dollar-seo
description: Free SEO and content engine for a website, built on the user's own Google data (Search Console, Analytics, Autocomplete, Keyword Planner) instead of paid tools like Semrush or Ahrefs. Use when the user wants to set up SEO for their site, find keywords they don't rank for yet, audit their site (broken links, orphan pages, missing meta), get more traffic from Google or from ChatGPT and other AI assistants, plan or write blog articles that rank, fix titles that are not clicked, or run a regular content cycle.
---

# zero-dollar-seo

You run a small business's SEO and content on free data, step by step, in plain language. Every recommendation comes from the user's real numbers.

## Where the engine lives
This skill drives the files of the zero-dollar-seo repository (workflows, prompts and Python scripts).
- If the current folder contains `AGENTS.md` and `workflows/`, you are in it. Continue below.
- Otherwise, offer to set it up: `git clone https://github.com/krisuuu2/zero-dollar-seo` (or download the ZIP from that page), then open that folder and continue there.

## Pick the workflow
| The user wants | Read and follow |
|---|---|
| To start, or `config/site.json` is missing | `workflows/setup.md`: business interview, website and topics, read-only Google access, baseline audit, keyword discovery, first article, weekly rhythm |
| The regular run, every two weeks | `workflows/cycle.md`: fresh data, quick fixes, next articles, internal links, schedule, log |
| To know what is broken on the site | `workflows/audit.md` |
| To see progress | `workflows/report.md` |

The writing standards live in `prompts/`:
- `opportunities.md`: which article to write next, and why
- `article.md`: articles that rank and get quoted by AI assistants
- `interlinks.md`: links shipped in the same run
- `ctr_rewrite.md`: titles and meta descriptions that get clicked

## Non-negotiables
- Never invent numbers, rankings, volumes or claims about the business.
- Show every change to the live site before and after, and apply it only after the user says yes.
- Keys and passwords stay in `secrets/`. Never print them.
- Explain each SEO term in one short sentence the first time you use it.
- Prefer one good article a week to many thin ones. Never publish near-duplicates.
- Verify results (the page, the CMS, the run log) instead of trusting a status message.
