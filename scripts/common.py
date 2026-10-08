"""Shared helpers: load config/site.json, Google credentials, small CSV/JSON writers."""
import json, csv, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.stdout.reconfigure(encoding="utf-8")


def cfg():
    p = ROOT / "config" / "site.json"
    if not p.exists():
        sys.exit("config/site.json is missing. Run the onboarding first: ask your AI agent to 'set up zero-dollar-seo' (Claude Code: /seo-setup).")
    return json.loads(p.read_text(encoding="utf-8"))


def google_creds(scopes):
    from google.oauth2 import service_account
    key = ROOT / cfg().get("google_sa_key", "secrets/google-sa.json")
    if not key.exists():
        sys.exit(f"Google service-account key not found at {key}. Follow step 3 of workflows/setup.md.")
    return service_account.Credentials.from_service_account_file(str(key), scopes=scopes)


def write_csv(path, rows, header):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path.relative_to(ROOT)} ({len(rows)} rows)")


def read_csv(path):
    path = ROOT / path
    if not path.exists():
        return []
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_json(path, obj):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")
