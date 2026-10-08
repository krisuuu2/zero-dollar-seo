# Prompt: rewrite titles and meta descriptions of pages that are seen but not clicked

Often the biggest quick win is not a new article. It is a page Google already shows many times, whose title does not make people click.

1. Take `low_ctr_pages` from `data/opportunities.json` (pages with many impressions and a click-through rate well below what their position should get).
2. For each page, find the queries it shows up for: filter `data/gsc_queries.csv` by `top_page`.
3. Fetch the page and read its current `<title>` and meta description.
4. Write 2 alternatives for each page:
   - The title uses the words of the top queries, promises the specific thing the searcher wants, stays under 60 characters, and keeps the brand at the end only if there is room.
   - The meta description is 140–160 characters, answers the query in one sentence and says what the reader gets on the page.
   - Never promise what the page does not deliver. A click that bounces back hurts more than no click.
5. Show the user current vs proposed side by side, with the impressions and CTR, and apply only the ones they approve (in the SEO plugin or CMS).
6. Note the date and the old CTR in `content/ledger.md` under **CTR changes**, so the next cycle can check whether it worked (wait at least 3–4 weeks before judging).
