# Workflow: site audit

Run `python scripts/crawl.py` and read `reports/audit.md`. Explain the result in plain words, ordered by impact:
broken links first (visitors and Google hit dead ends), then orphan pages (Google finds them late), missing or duplicate titles and meta descriptions (they decide whether people click), missing H1 and thin pages, then noindex pages listed in the sitemap.
For each item give the concrete fix. Offer to apply the fixes you can make through the CMS, and show every change before applying it. Slow pages: re-run once before acting, because a cold cache causes false alarms.
