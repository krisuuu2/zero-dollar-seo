"""Harvests Google Autocomplete for every seed topic: the seed itself, then seed + a..z (the "alphabet soup" method).
Then removes every phrase the site already gets impressions for (data/gsc_queries.csv), so what is left is NEW demand.
   python scripts/autocomplete_harvest.py ["extra seed" ...]
Writes data/autocomplete_all.csv (phrase, seed) and data/new_phrases.csv (phrases the site does not show up for yet).
Polite: ~0.4 s between calls; uses the public suggest endpoint, no key needed."""
import sys, time, string, json, requests
from common import cfg, read_csv, write_csv

C = cfg()
seeds = list(dict.fromkeys(C.get("seed_topics", []) + sys.argv[1:]))
if not seeds:
    sys.exit("Add seed_topics to config/site.json (3-10 short phrases your customers would type).")
hl, gl = C.get("market", {}).get("language", "en"), C.get("market", {}).get("country", "us")
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0"


def suggest(q):
    try:
        r = S.get("https://suggestqueries.google.com/complete/search", params={"client": "firefox", "hl": hl, "gl": gl, "q": q}, timeout=15)
        return json.loads(r.text)[1]
    except Exception:
        return []


found = {}
for seed in seeds:
    for suffix in [""] + [" " + c for c in string.ascii_lowercase]:
        for p in suggest(seed + suffix):
            found.setdefault(p.lower().strip(), seed)
        time.sleep(0.4)
    print(f"{seed}: {sum(1 for v in found.values() if v == seed)} phrases")

known = {r["query"].lower().strip() for r in read_csv("data/gsc_queries.csv")}
write_csv("data/autocomplete_all.csv", sorted([p, s] for p, s in found.items()), ["phrase", "seed"])
new = sorted([p, s] for p, s in found.items() if p not in known)
write_csv("data/new_phrases.csv", new, ["phrase", "seed"])
print(f"total {len(found)} · already ranking {len(found) - len(new)} · NEW {len(new)}")
print("Next: upload data/new_phrases.csv to Google Keyword Planner for search volumes (step 5 of workflows/setup.md explains how).")
