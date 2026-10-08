"""Pulls GA4 data: sessions by channel per month (including AI assistants such as ChatGPT), top landing pages from organic search
and from AI assistants, and key events (conversions).
   python scripts/ga4_pull.py
Writes data/ga4_channels.csv, data/ga4_ai_sources.csv, data/ga4_landing.csv"""
import re
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Dimension, Metric
from common import cfg, google_creds, write_csv

C = cfg()
if not C.get("ga4_property_id"):
    raise SystemExit("No ga4_property_id in config/site.json; GA4 is optional, skipping.")
ga = BetaAnalyticsDataClient(credentials=google_creds(["https://www.googleapis.com/auth/analytics.readonly"]))
P = f"properties/{C['ga4_property_id']}"
AI = re.compile(r"chatgpt|openai|perplexity|gemini\.google|copilot|claude\.ai|you\.com|phind|deepseek|grok", re.I)


def rep(dims, mets, start="400daysAgo", limit=10000):
    r = ga.run_report(RunReportRequest(property=P, date_ranges=[DateRange(start_date=start, end_date="yesterday")], dimensions=[Dimension(name=d) for d in dims], metrics=[Metric(name=m) for m in mets], limit=limit))
    return [[v.value for v in x.dimension_values] + [x.metric_values[i].value for i in range(len(mets))] for x in r.rows]


rows = rep(["yearMonth", "sessionDefaultChannelGroup"], ["sessions", "keyEvents"])
write_csv("data/ga4_channels.csv", sorted(rows), ["month", "channel", "sessions", "key_events"])
src = [r for r in rep(["yearMonth", "sessionSource"], ["sessions"]) if AI.search(r[1])]
write_csv("data/ga4_ai_sources.csv", sorted(src), ["month", "source", "sessions"])
land = rep(["sessionDefaultChannelGroup", "landingPagePlusQueryString"], ["sessions", "keyEvents"], start="90daysAgo")
land = [r for r in land if r[0] in ("Organic Search", "AI Assistant") or AI.search(r[0])]
land.sort(key=lambda r: -int(r[2]))
write_csv("data/ga4_landing.csv", land[:300], ["channel", "landing_page", "sessions", "key_events"])

by_m = {}
for m, ch, s, k in rows:
    if ch in ("Organic Search", "AI Assistant"):
        by_m.setdefault(m, {})[ch] = int(s)
for m in sorted(by_m)[-6:]:
    print(m, by_m[m])
