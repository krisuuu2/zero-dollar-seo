# Prompt: pick what to write next

You are choosing the next 1–3 articles for the site described in `config/site.json`. Use only real data from this project.

## Read first
- `config/site.json`: the business, the customer, the offers, topics to avoid.
- `data/opportunities.json`: page-two queries, low-CTR pages and rising queries from Search Console.
- `data/keywords_ranked.csv` (or `data/new_phrases.csv` if volumes were not added yet): new phrases the site does not show up for.
- `data/ga4_landing.csv`: which pages already bring visitors from Google and from AI assistants.
- `content/ledger.md`: every topic the site already covers. Never plan a page that overlaps one of these.

## How to choose, in this order
1. **Page-two queries first.** A query at position 8–20 with real impressions is the cheapest win, because Google already thinks the site is relevant. Decide whether the existing page should be improved or a new, more focused page is needed. Improve when the query matches the existing page's topic; create a new page when the query is a different question.
2. **New phrases with buying intent.** From the new phrases, prefer ones that show the reader is close to a decision ("best", "vs", "alternative", "for <use case>", "price", "how to choose"), and that the business's offer genuinely answers.
3. **Definition pages.** "What is X" and glossary-style pages rank fast and are the pages AI assistants quote most. Plan at least one when the niche has terms customers search for.
4. **Comparison pages.** "X vs Y" and "X alternative" pages carry buying intent and keep earning. Name competitors only with true, checkable statements, and never invent their prices.
5. Skip freebie-hunter traffic ("free download", "torrent", "crack") unless the business has a real free offer.
6. One topic = one page. If two phrases have the same answer, they belong on the same page.

## Output
For each pick: the target phrase, the search intent in one sentence, why it was chosen (the numbers from the files), new page or improvement of which URL, 2–4 existing pages that should link to it, and the offer it naturally leads to.
Then add the chosen topics to the **Planned** section of `content/ledger.md`.
