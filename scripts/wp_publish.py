"""Optional: sends an article to WordPress through the REST API (an Application Password, no plugin needed).
   python scripts/wp_publish.py content/drafts/<slug>.json [--publish-at "2026-10-17 10:00"] [--draft]
The JSON is what the article prompt produces: title, slug, excerpt, meta_description, html, faq[].
Default is a DRAFT for you to review in WordPress. --publish-at schedules it (status "future").
The WordPress password lives in secrets/wp_app_password.txt (WordPress > Users > Profile > Application Passwords).
FAQ is appended as a visible section plus FAQPage JSON-LD, so AI assistants and Google can quote the answers."""
import sys, json, pathlib, html, requests
from common import ROOT, cfg

C = cfg(); WP = C["publishing"]
if len(sys.argv) < 2:
    sys.exit(__doc__)
art = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
pw_file = ROOT / "secrets" / "wp_app_password.txt"
if not pw_file.exists():
    sys.exit("Save your WordPress Application Password in secrets/wp_app_password.txt first.")
auth = (WP["wp_user"], pw_file.read_text(encoding="utf-8").strip())
api = WP.get("wp_url", C["site_url"]).rstrip("/") + "/wp-json/wp/v2/posts"

body = art["html"]
if art.get("faq"):
    body += "\n<h2>Frequently asked questions</h2>\n" + "\n".join(f"<h3>{html.escape(f['q'])}</h3>\n<p>{html.escape(f['a'])}</p>" for f in art["faq"])
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in art["faq"]]}
    body += f'\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
post = {"title": art["title"], "slug": art["slug"], "excerpt": art.get("excerpt", art.get("meta_description", "")), "content": body, "status": "draft"}
if "--publish-at" in sys.argv and "--draft" not in sys.argv:
    when = sys.argv[sys.argv.index("--publish-at") + 1].replace(" ", "T")
    post.update(status="future", date=when + (":00" if when.count(":") == 1 else ""))
r = requests.post(api, json=post, auth=auth, timeout=60)
if r.status_code >= 300:
    sys.exit(f"WordPress said {r.status_code}: {r.text[:400]}\nCheck wp_user, the Application Password, and that /wp-json is not blocked by a security plugin.")
d = r.json()
print(f"{d['status']}: {d['link']}  (id {d['id']})")
print("Set the SEO title and meta description in your SEO plugin if it does not read the excerpt:", art.get("seo_title"), "|", art.get("meta_description"))
