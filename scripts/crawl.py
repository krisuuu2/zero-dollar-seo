"""Site audit crawler: the checks a paid SEO site audit does, for free.
   python scripts/crawl.py [https://example.com]   (default: site_url from config/site.json)
Finds the sitemap by itself (robots.txt, /sitemap.xml, /sitemap_index.xml, /wp-sitemap.xml; nested sitemap indexes are followed),
crawls every page in it, builds the internal-link graph and status-checks every internal link.
Reports:
  orphan pages        in the sitemap, but no other page links to them (Google finds and values them less)
  broken links        internal links that return 4XX/5XX, with the pages that contain them
  missing meta        indexable pages without a meta description
  title problems      missing, too long (>60 chars) or duplicated titles
  missing H1          pages with no <h1>
  thin pages          indexable pages with fewer than 300 words of visible text
  noindex in sitemap  pages the sitemap lists but that tell Google not to index them
  slow pages          HTML took longer than 2 s (cold cache can cause false alarms: re-run before acting)
Writes reports/audit.json and reports/audit.md (the human summary)."""
import sys, re, json, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup
from common import ROOT, cfg

BASE = (sys.argv[1] if len(sys.argv) > 1 else cfg()["site_url"]).rstrip("/")
HOST = urlparse(BASE).netloc.lower().removeprefix("www.")
S = requests.Session(); S.headers.update({"User-Agent": "Mozilla/5.0 (compatible; SEOEngineAudit/1.0)"})
WORKERS, TIMEOUT, SLOW = 8, 25, 2.0


def norm(u):
    u, _ = urldefrag(u); p = urlparse(u)
    if not p.scheme.startswith("http"):
        return ""
    path = p.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    return f"https://{p.netloc.lower().removeprefix('www.')}{path}" + (f"?{p.query}" if p.query else "")


internal = lambda u: urlparse(u).netloc.lower().removeprefix("www.") == HOST


def sitemap_urls():
    cands = []
    try:
        cands += re.findall(r"(?im)^sitemap:\s*(\S+)", S.get(BASE + "/robots.txt", timeout=TIMEOUT).text)
    except Exception:
        pass
    cands += [BASE + p for p in ("/sitemap_index.xml", "/sitemap.xml", "/wp-sitemap.xml")]
    seen, urls = set(), {}
    stack = list(dict.fromkeys(cands))
    while stack:
        sm = stack.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        try:
            r = S.get(sm, timeout=TIMEOUT)
            if r.status_code != 200 or "<" not in r.text[:200]:
                continue
        except Exception:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
        if "<sitemapindex" in r.text:
            stack += [l for l in locs if l not in seen]
        else:
            for l in locs:
                if internal(l):
                    urls[norm(l)] = sm.rsplit("/", 1)[-1]
    return urls


def crawl(u):
    rec = {"url": u, "status": None, "elapsed": None, "title": None, "meta": None, "h1": 0, "words": 0, "noindex": False, "links": [], "error": None}
    try:
        t0 = time.time(); r = S.get(u, timeout=TIMEOUT); rec["elapsed"] = round(time.time() - t0, 2); rec["status"] = r.status_code
        if "html" not in r.headers.get("Content-Type", ""):
            return rec
        soup = BeautifulSoup(r.text, "lxml")
        rec["title"] = soup.title.string.strip() if soup.title and soup.title.string else None
        md = soup.find("meta", attrs={"name": "description"}); rec["meta"] = (md.get("content") or "").strip() if md else None
        rb = soup.find("meta", attrs={"name": "robots"}); rec["noindex"] = bool(rb and "noindex" in (rb.get("content") or "").lower())
        rec["h1"] = len(soup.find_all("h1"))
        links = set()
        for a in soup.find_all("a", href=True):
            h = a["href"].strip()
            if h.startswith(("mailto:", "tel:", "javascript:", "#")):
                continue
            au = urljoin(u, h)
            if internal(au) and "/cdn-cgi/" not in au:   # Cloudflare's email-protection links always 404 for crawlers
                links.add(norm(au))
        rec["links"] = sorted(l for l in links if l)
        for t in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            t.decompose()
        rec["words"] = len(soup.get_text(" ").split())
    except Exception as e:
        rec["error"] = str(e)[:200]
    return rec


def status(u):
    try:
        r = S.get(u, timeout=TIMEOUT, stream=True); c = r.status_code; r.close(); return u, c
    except Exception:
        return u, None


def main():
    print(f"== Site audit: {BASE} ==")
    sm = sitemap_urls()
    if not sm:
        sys.exit("No sitemap found (robots.txt, /sitemap.xml, /sitemap_index.xml, /wp-sitemap.xml). Add one, or pass a site that has it.")
    pages = sorted(sm)
    print(f"{len(pages)} pages in the sitemap; crawling...")
    with ThreadPoolExecutor(WORKERS) as ex:
        recs = {r["url"]: r for r in ex.map(crawl, pages)}
    incoming, targets = {u: set() for u in pages}, {}
    for src, r in recs.items():
        for t in r["links"]:
            targets.setdefault(t, set()).add(src)
            if t in incoming and t != src:
                incoming[t].add(src)
    print(f"status-checking {len(targets)} internal link targets...")
    with ThreadPoolExecutor(WORKERS) as ex:
        codes = dict(ex.map(status, list(targets)))
    idx = [u for u in pages if recs[u]["status"] == 200 and not recs[u]["noindex"]]
    titles = Counter(recs[u]["title"] for u in idx if recs[u]["title"])
    R = {
        "site": BASE, "pages": len(pages), "internal_targets": len(targets),
        "orphans": [u for u in idx if not incoming[u] and urlparse(u).path not in ("", "/")],
        "broken": [{"url": t, "status": codes[t], "linked_from": sorted(targets[t])[:10]} for t in targets if codes.get(t) is None or codes[t] >= 400],
        "missing_meta": [u for u in idx if not recs[u]["meta"]],
        "title_missing": [u for u in idx if not recs[u]["title"]],
        "title_too_long": [{"url": u, "title": recs[u]["title"], "chars": len(recs[u]["title"])} for u in idx if recs[u]["title"] and len(recs[u]["title"]) > 60],
        "title_duplicate": [{"title": t, "pages": [u for u in idx if recs[u]["title"] == t]} for t, n in titles.items() if n > 1],
        "missing_h1": [u for u in idx if recs[u]["h1"] == 0],
        "thin": [{"url": u, "words": recs[u]["words"]} for u in idx if recs[u]["words"] < 300],
        "noindex_in_sitemap": [u for u in pages if recs[u]["noindex"]],
        "slow": sorted([{"url": u, "seconds": recs[u]["elapsed"]} for u in pages if (recs[u]["elapsed"] or 0) >= SLOW], key=lambda x: -x["seconds"]),
        "errors": [{"url": u, "status": recs[u]["status"], "error": recs[u]["error"]} for u in pages if recs[u]["status"] != 200],
    }
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports/audit.json").write_text(json.dumps(R, indent=2, ensure_ascii=False), encoding="utf-8")
    keys = ["orphans", "broken", "missing_meta", "title_missing", "title_too_long", "title_duplicate", "missing_h1", "thin", "noindex_in_sitemap", "slow", "errors"]
    md = [f"# Site audit · {BASE}", "", f"Pages in sitemap: {len(pages)} · internal link targets checked: {len(targets)}", "", "| Check | Count |", "|---|---|"]
    md += [f"| {k.replace('_', ' ')} | {len(R[k])} |" for k in keys]
    for k in keys:
        if R[k]:
            md += ["", f"## {k.replace('_', ' ')}"] + [f"- {x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)}" for x in R[k][:40]]
    (ROOT / "reports/audit.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    for k in keys:
        print(f"{k:20s} {len(R[k])}")
    print("-> reports/audit.md, reports/audit.json")


if __name__ == "__main__":
    main()
