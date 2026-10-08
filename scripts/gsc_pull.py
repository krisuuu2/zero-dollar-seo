"""Pulls Search Console data for the site.
   python scripts/gsc_pull.py
Writes:
  data/gsc_monthly.csv      clicks, impressions, CTR, position per month (last 16 months)
  data/gsc_queries.csv      every query of the last 28 days with clicks, impressions, CTR, position, top page
  data/gsc_pages.csv        every page of the last 28 days with the same metrics
  data/opportunities.json   page-two queries, low-CTR pages and rising queries, ranked"""
import datetime as dt
from collections import defaultdict
from googleapiclient.discovery import build
from common import cfg, google_creds, write_csv, write_json

C = cfg()
sc = build("searchconsole", "v1", credentials=google_creds(["https://www.googleapis.com/auth/webmasters.readonly"]), cache_discovery=False)
PROP = C["gsc_property"]
end = dt.date.today() - dt.timedelta(days=3)          # Search Console data lags ~2-3 days


def q(start, stop, dims, limit=25000):
    rows, startRow = [], 0
    while True:
        r = sc.searchanalytics().query(siteUrl=PROP, body={"startDate": str(start), "endDate": str(stop), "dimensions": dims, "rowLimit": limit, "startRow": startRow}).execute().get("rows", [])
        rows += r
        if len(r) < limit:
            return rows
        startRow += limit


# monthly trend
m = defaultdict(lambda: [0, 0, 0.0])
for r in q(end - dt.timedelta(days=486), end, ["date"]):
    k = r["keys"][0][:7]; m[k][0] += r["clicks"]; m[k][1] += r["impressions"]; m[k][2] += r["position"] * r["impressions"]
write_csv("data/gsc_monthly.csv", [[k, v[0], v[1], round(v[0] / v[1] * 100, 2) if v[1] else 0, round(v[2] / v[1], 1) if v[1] else 0] for k, v in sorted(m.items())], ["month", "clicks", "impressions", "ctr_pct", "avg_position"])

# last 28 days vs the 28 before
s28 = end - dt.timedelta(days=27)
prev_s, prev_e = s28 - dt.timedelta(days=28), s28 - dt.timedelta(days=1)
qp = q(s28, end, ["query", "page"])
best = {}
for r in qp:
    qq, page = r["keys"]
    if qq not in best or r["clicks"] + r["impressions"] / 1000 > best[qq]["clicks"] + best[qq]["impressions"] / 1000:
        best[qq] = {"page": page, **r}
queries = q(s28, end, ["query"])
prev = {r["keys"][0]: r for r in q(prev_s, prev_e, ["query"])}
write_csv("data/gsc_queries.csv", [[r["keys"][0], r["clicks"], r["impressions"], round(r["ctr"] * 100, 2), round(r["position"], 1), best.get(r["keys"][0], {}).get("page", "")] for r in sorted(queries, key=lambda r: -r["impressions"])],
          ["query", "clicks", "impressions", "ctr_pct", "position", "top_page"])
pages = q(s28, end, ["page"])
write_csv("data/gsc_pages.csv", [[r["keys"][0], r["clicks"], r["impressions"], round(r["ctr"] * 100, 2), round(r["position"], 1)] for r in sorted(pages, key=lambda r: -r["impressions"])],
          ["page", "clicks", "impressions", "ctr_pct", "position"])

# opportunities
page_two = [{"query": r["keys"][0], "position": round(r["position"], 1), "impressions": r["impressions"], "page": best.get(r["keys"][0], {}).get("page")}
            for r in queries if 8 <= r["position"] <= 20 and r["impressions"] >= 20]
page_two.sort(key=lambda x: -x["impressions"])
exp_ctr = lambda pos: 0.28 if pos < 1.5 else 0.15 if pos < 2.5 else 0.10 if pos < 3.5 else 0.07 if pos < 5.5 else 0.04 if pos < 10.5 else 0.015
low_ctr = [{"page": r["keys"][0], "impressions": r["impressions"], "ctr_pct": round(r["ctr"] * 100, 2), "position": round(r["position"], 1),
            "missed_clicks": round(r["impressions"] * (exp_ctr(r["position"]) - r["ctr"]))}
           for r in pages if r["impressions"] >= 200 and r["ctr"] < exp_ctr(r["position"]) * 0.6]
low_ctr.sort(key=lambda x: -x["missed_clicks"])
rising = [{"query": k, "impressions_now": r["impressions"], "impressions_before": prev.get(k, {}).get("impressions", 0)}
          for k, r in ((r["keys"][0], r) for r in queries) if r["impressions"] >= 30 and r["impressions"] >= 2 * prev.get(k, {}).get("impressions", 0) + 10]
rising.sort(key=lambda x: -(x["impressions_now"] - x["impressions_before"]))
write_json("data/opportunities.json", {"window": [str(s28), str(end)], "page_two_queries": page_two[:60], "low_ctr_pages": low_ctr[:30], "rising_queries": rising[:40]})
print(f"queries: {len(queries)} · page-two: {len(page_two)} · low-CTR pages: {len(low_ctr)} · rising: {len(rising)}")
