# Workflow: onboarding (setup)

You are onboarding a new user to this SEO engine. Talk to them in their language, in short, plain sentences. Explain WHY each step matters in one sentence before asking them to do it. Never ask more than 2–3 questions at once. Never print or repeat secrets (keys, passwords).

Keep a checklist at the top of each reply (✅ done / ⏳ now / ⬜ next) for these steps:
1. About your business
2. Your website and topics
3. Google access (Search Console, Analytics)
4. Baseline: site audit + your data
5. Keyword discovery
6. Your first content plan
7. Publishing and the two-week rhythm

## Step 0 — environment (do it yourself, silently if it works)
- Check Python 3.10+ (`python --version` or `py --version`). Install the requirements: `pip install -r requirements.txt`. If something fails, explain the fix in one sentence.

## Step 1 — about your business (ask)
- What does the business sell or do, in one sentence? Who is the ideal customer, and what problem are they trying to solve when they search?
- What are the main products or services, with their URLs? Anything you never want to claim or write about?
- How should the articles sound (for example practical and friendly, or formal and expert)?

## Step 2 — your website and topics (ask, then research)
- Ask for the website URL and the main country and language of the customers.
- Visit the site yourself (fetch the homepage, the sitemap and 5–10 key pages) and summarise back what you understood in 3 sentences. Ask them to correct you.
- Propose 5–8 **seed topics**: short phrases a customer would type into Google before they know the brand (not the brand name). Let them edit the list.
- Ask for 2–5 competitors (optional; you can suggest some from a quick search).
- Write everything to `config/site.json` (copy `config/site.example.json` first). Show them the file.

## Step 3 — Google access (guide them, one click-path at a time)
Explain: "Claude needs read-only access to your own Google data. This is free and it is the same data paid SEO tools try to estimate."
1. **Search Console.** Ask if the site is verified at search.google.com/search-console. If not, guide them through adding a *Domain* property (DNS TXT record) or a *URL prefix* property. Ask which property name they see (`sc-domain:example.com` or `https://example.com/`) and save it as `gsc_property`.
2. **Google Cloud service account** (5 minutes, free):
   - console.cloud.google.com → create a project (any name).
   - APIs & Services → Library → enable **Google Search Console API** and **Google Analytics Data API**.
   - IAM & Admin → Service Accounts → Create (any name) → no roles needed → Done → open it → Keys → Add key → JSON. The file downloads.
   - Ask them to move that file to `secrets/google-sa.json` in this folder (never paste its content into the chat).
3. Read the service account email from the file yourself (`client_email`) and give it to them.
   - Search Console → Settings → Users and permissions → Add user → that email → **Restricted**.
   - GA4 (optional but recommended) → Admin → Property access management → + → that email → **Viewer**. Ask for the numeric **Property ID** (Admin → Property details) and save it as `ga4_property_id`.
4. Run `python scripts/check_access.py`. Fix every line marked NO with them before moving on.

## Step 4 — baseline (run it, then explain it like a consultant)
- `python scripts/crawl.py` → read `reports/audit.md`.
- `python scripts/gsc_pull.py` → read `data/gsc_monthly.csv` and `data/opportunities.json`.
- `python scripts/ga4_pull.py` (if GA4 is connected) → note visits from AI assistants (ChatGPT, Perplexity, Gemini, Copilot).
- Write `reports/baseline.md` (date it): the monthly trend, the 5 biggest problems from the audit with the fix for each, the top 10 page-two queries, the top 5 low-CTR pages, and AI-assistant visits. Explain each in plain words: what it is, why it matters, what we will do.
- Offer to fix the quick audit items now (missing meta descriptions, titles that are too long, broken links), always showing the change first.

## Step 5 — keyword discovery
- `python scripts/autocomplete_harvest.py` → it removes phrases the site already gets impressions for, so `data/new_phrases.csv` is new demand.
- Explain Keyword Planner (free, needs a Google Ads account; running ads is not required): ads.google.com → Tools → Keyword Planner → **Get search volume and forecasts** → upload `data/new_phrases.csv` → Historical metrics → Download (CSV). Ask them to drop the file into `data/`.
- `python scripts/merge_volumes.py data/<their file>` → `data/keywords_ranked.csv`.
- If they skip Keyword Planner, continue without volumes and say that ranking will rely on intent and Search Console only.

## Step 6 — first content plan
- Create `content/ledger.md` with three sections: **Already covered** (list every existing article/page topic from the sitemap, one line each), **Planned**, **Published or scheduled**, plus **CTR changes**.
- Follow `prompts/opportunities.md` and present the first 4 article ideas with the reason for each (real numbers).
- Write the first article with `prompts/article.md`, show it, and revise it with them until they are happy.

## Step 7 — publishing and the two-week rhythm
- Ask how they publish: WordPress (offer `scripts/wp_publish.py` with an Application Password saved in `secrets/wp_app_password.txt`; default is a draft they approve), another CMS (you give them the clean HTML and meta fields to paste), or drafts only.
- Agree the rhythm: **one new article every week on the same day and time** (default Saturday 10:00), produced in a session every two weeks (the cycle workflow). A steady weekly slot beats bursts.
- Tell them how to run it every two weeks: open this folder in your AI coding agent and say "run the SEO cycle" (in Claude Code: `/seo-cycle`). If they want it automatic, explain their agent's scheduling option (Claude Code: scheduled tasks or `/schedule`; Codex and others: a cron job or CI that starts the agent with "run the SEO cycle"), and the rule that matters most: after each automatic run, check `content/runlog.md` — if today's entry is missing, the run did not happen, whatever the status says.
- Finish with a 5-line summary: what was set up, what we found, what gets published when, and what they do every two weeks.
