"""Checks that the service account can read Search Console and GA4 for this site.
   python scripts/check_access.py
Prints what works, what doesn't, and the exact fix for each problem."""
from common import cfg, google_creds

C = cfg()
ok = True
SC = ["https://www.googleapis.com/auth/webmasters.readonly", "https://www.googleapis.com/auth/analytics.readonly"]
creds = google_creds(SC)
print("Service account:", creds.service_account_email)

try:
    from googleapiclient.discovery import build
    sc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    sites = [s["siteUrl"] for s in sc.sites().list().execute().get("siteEntry", [])]
    if C["gsc_property"] in sites:
        print(f"OK  Search Console: can read {C['gsc_property']}")
    else:
        ok = False
        print(f"NO  Search Console: {C['gsc_property']} is not shared with the service account.")
        print(f"    Visible properties: {sites or 'none'}")
        print(f"    Fix: Search Console > Settings > Users and permissions > Add user > {creds.service_account_email} > Restricted.")
        print("    If the property is listed with a different spelling (https://… vs sc-domain:…), put that exact value in config/site.json.")
except Exception as e:
    ok = False
    print("NO  Search Console API error:", e)
    print("    Fix: Google Cloud console > APIs & Services > Library > enable 'Google Search Console API'.")

if C.get("ga4_property_id"):
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
        ga = BetaAnalyticsDataClient(credentials=creds)
        r = ga.run_report(RunReportRequest(property=f"properties/{C['ga4_property_id']}", date_ranges=[DateRange(start_date="28daysAgo", end_date="today")], metrics=[Metric(name="sessions")]))
        print(f"OK  GA4: property {C['ga4_property_id']} returned {r.rows[0].metric_values[0].value if r.rows else 0} sessions in the last 28 days")
    except Exception as e:
        ok = False
        print("NO  GA4 error:", str(e)[:300])
        print("    Fix 1: Google Cloud console > enable 'Google Analytics Data API'.")
        print(f"    Fix 2: GA4 > Admin > Property access management > + > {creds.service_account_email} > Viewer.")
        print("    Fix 3: ga4_property_id must be the numeric Property ID (GA4 > Admin > Property details), not the G-XXXX measurement ID.")
else:
    print("--  GA4 skipped (no ga4_property_id in config/site.json)")

print("\nALL GOOD" if ok else "\nSome access is missing; fix the lines marked NO and run this again.")
