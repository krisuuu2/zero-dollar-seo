"""Merges a Google Keyword Planner export into the new-phrase list.
   python scripts/merge_volumes.py path/to/Keyword_Stats.csv
Keyword Planner exports UTF-16 tab-separated files with 2 title lines; this handles that and plain CSV.
Writes data/keywords_ranked.csv: phrase, seed, avg_monthly_searches, competition, intent_guess — sorted by volume."""
import sys, csv, io, re, pathlib
from common import read_csv, write_csv

if len(sys.argv) < 2:
    sys.exit("usage: python scripts/merge_volumes.py <Keyword Planner export>")
raw = pathlib.Path(sys.argv[1]).read_bytes()
text = raw.decode("utf-16") if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else raw.decode("utf-8-sig")
lines = text.splitlines()
start = next(i for i, l in enumerate(lines) if l.lower().startswith("keyword"))
delim = "\t" if "\t" in lines[start] else ","
rows = list(csv.DictReader(io.StringIO("\n".join(lines[start:])), delimiter=delim))
vol_col = next((k for k in rows[0] if k.lower().startswith("avg. monthly")), None)
comp_col = next((k for k in rows[0] if k.lower() == "competition"), None)


def num(v):
    v = (v or "").replace(",", "").strip()
    m = re.findall(r"\d+", v)
    return int(m[-1]) if m else 0   # ranges like "1K – 10K" are exported as numbers when no ads run; take the upper bound if text


vol = {r["Keyword"].lower().strip(): (num(r.get(vol_col)), r.get(comp_col, "")) for r in rows if r.get("Keyword")}
BUY = re.compile(r"\b(best|vs|alternative|price|pricing|cost|buy|review|for (small )?business|software|service|near me|template|tool)\b")
LEARN = re.compile(r"\b(how|what|why|when|guide|tutorial|ideas|examples|meaning)\b")
out = []
for p in read_csv("data/new_phrases.csv"):
    v, c = vol.get(p["phrase"].lower().strip(), (0, ""))
    intent = "buy" if BUY.search(p["phrase"]) else "learn" if LEARN.search(p["phrase"]) else "other"
    out.append([p["phrase"], p["seed"], v, c, intent])
out.sort(key=lambda r: -r[2])
write_csv("data/keywords_ranked.csv", out, ["phrase", "seed", "avg_monthly_searches", "competition", "intent_guess"])
print(f"{sum(1 for r in out if r[2])} of {len(out)} new phrases have a volume")
