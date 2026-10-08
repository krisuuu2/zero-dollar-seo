# Prompt: write one article that ranks on Google and gets quoted by AI assistants

You write for the site in `config/site.json`, in its `voice`, for its `customer`, in the site's language. The target phrase and intent come from the opportunity step.

## Absolute rules
1. **Original only.** You may read top-ranking pages to see what the searcher expects, but never copy their structure, sentences or examples. Write a better, more complete answer in your own words.
2. **No invented facts.** Only claim about the business what `config/site.json` says or what you read on the site itself. Never invent numbers, prices, features, customers or results. If a statistic helps, use a real one and link the source.
3. **Teach first, sell second.** The article is genuinely useful even for a reader who never buys. The offer appears where it is the natural answer, plus one calm call to action near the end.
4. Respect `avoid` in the config.

## Write so AI assistants quote you (GEO)
- **Answer first.** Open the article, and each main section, with a direct 40–60 word answer in plain, definitional language. No "in this article we will".
- **Self-contained sections** of roughly 120–180 words. Each section must make sense if it is lifted out alone, so never write "as mentioned above".
- **Use the searcher's own words**: the target phrase and the phrases from `data/new_phrases.csv` that ask the same question.
- **Neutral, expert tone.** Hype words ("game-changer", "revolutionary", "ultimate") make pages less likely to be quoted.
- **End with a real FAQ**: 5–7 questions a customer would actually type, each answered in 40–80 words. These become FAQPage structured data.

## Structure
- 1,200–1,800 words. Short paragraphs. Concrete examples from the customer's real situation.
- Arc: the reader's problem, why it happens, the solution, how to do it step by step, where the offer helps, the FAQ, one closing line with a link.
- One H1 (the title), H2 for sections, H3 only inside a section. Lists only where the content is a real list.
- 2–4 internal links to existing pages of the site, on descriptive anchor text inside sentences (never "click here"). Use pages from `data/gsc_pages.csv` or the sitemap, never invented URLs.

## Output: save to `content/drafts/<slug>.json`
```json
{
  "title": "H1, contains the target phrase, under 65 characters",
  "seo_title": "the <title> tag, under 60 characters",
  "meta_description": "140-160 characters, contains the target phrase, says what the reader gets",
  "slug": "short-lowercase-hyphenated",
  "excerpt": "1-2 plain sentences",
  "target_phrase": "...",
  "internal_links": ["https://...", "https://..."],
  "html": "<p>…the article body as clean HTML, without the H1…</p>",
  "faq": [{"q": "...", "a": "..."}]
}
```
Also save a readable copy as `content/drafts/<slug>.md`, and add the topic to the **Published or scheduled** section of `content/ledger.md` once it goes live.

## Self-check before saving
- Word count is between 1,200 and 1,800.
- The first paragraph answers the target phrase directly.
- Every internal link URL exists in `data/gsc_pages.csv` or the sitemap.
- No sentence makes a claim about the business that the config or the site does not support.
- The meta description is 140–160 characters, the SEO title is under 60.
