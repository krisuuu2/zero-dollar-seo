# Prompt: give a new page incoming links (do this in the SAME run that publishes it)

A page that no other page links to starts as an island: Google finds it later and trusts it less. So every new page ships together with 2–4 links pointing to it from existing pages.

1. Pick 2–4 existing pages that are about a closely related topic. Use `data/gsc_pages.csv` (pages that already get impressions pass the most value) and the topic list in `content/ledger.md`.
2. For each one, write ONE new sentence, or extend an existing sentence, that fits naturally into a paragraph that is already there. The link goes on a descriptive phrase that says what the new page is about, ideally near the end of the sentence. Never "click here", never a list of links.
3. Show the user the exact paragraph before and after for each page.
4. Apply the change only after the user approves: in WordPress through the REST API (`PUT /wp-json/wp/v2/posts/<id>` or `/pages/<id>` with the updated content), or by giving the user the snippet to paste in their CMS.
5. Verify: fetch each source page and confirm the link is in the HTML. If the new page is scheduled for later, check the links in the CMS content instead. Do not end the run until every planned link is confirmed.
6. Run `python scripts/crawl.py` after the next publish: the new page must not appear under "orphans".

Do not create a separate scheduled job that "adds the links later". In our experience these jobs report success without doing the work. The links are added in the same session as the article.
