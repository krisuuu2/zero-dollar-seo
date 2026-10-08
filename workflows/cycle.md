# Workflow: the two-week cycle

Run one content cycle for the site in `config/site.json`. Work through every step; explain results in plain words; ask before changing anything on the live site.

1. **Fresh data.** `python scripts/gsc_pull.py`, `python scripts/ga4_pull.py` (if configured). Compare with the previous cycle in `content/runlog.md`: clicks, impressions, position, AI-assistant visits. Say in 2–3 sentences what changed and the most likely reason.
2. **Check last cycle's work.** For every article published in the last 4–8 weeks (`content/ledger.md`): impressions, clicks, average position of its target phrase. For every CTR change older than 3 weeks: did CTR improve? Keep what works; note what did not.
3. **Quick wins first.** `prompts/ctr_rewrite.md` for 2–3 low-CTR pages. Every 4th cycle also run `python scripts/crawl.py` and fix new broken links, orphans and missing meta.
4. **Pick the next articles.** `prompts/opportunities.md`. Plan as many as there are free weekly slots until the next cycle (normally 2). Count slots from the LATEST published or scheduled article, not from today, so no week is skipped. If there is no genuinely distinct topic, write fewer and say why — never a thin near-duplicate.
5. **Write them.** `prompts/article.md`, one at a time; show each to the user.
6. **Links in the same run.** `prompts/interlinks.md` for each new article, before the cycle ends.
7. **Schedule.** Publish into the weekly slots (`scripts/wp_publish.py --publish-at`, or hand over HTML for the CMS). Check in the CMS that each one is really scheduled.
8. **Log.** Append to `content/runlog.md`: date, the numbers from step 1, what was fixed, what was written and when it goes live, links added, and the plan for the next cycle. Update `content/ledger.md`.
