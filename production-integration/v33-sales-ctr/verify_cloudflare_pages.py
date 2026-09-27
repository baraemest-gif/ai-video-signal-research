#!/usr/bin/env python3
from pathlib import Path
import os, re, json, urllib.request, urllib.error, sys

token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
if not token:
    print("TOKEN=NOT_LOADED")
    sys.exit(1)

home = Path.home()
sources = [
    home / ".wrangler/config/default.toml",
    home / ".wrangler/cache/wrangler-account.json",
    home / ".wrangler/cache/pages.json",
]
ids = set()
for f in sources:
    if f.exists():
        txt = f.read_text(errors="ignore")
        ids.update(re.findall(r"\b[a-fA-F0-9]{32}\b", txt))

if not ids:
    print("ACCOUNT_CACHE=NOT_FOUND")
    sys.exit(2)

found = False
auth_ok = False
for account_id in sorted(ids):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "AIVS-v33-Termux"
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"AUTH_HTTP={e.code}")
        try:
            body = json.loads(e.read().decode())
            for err in body.get("errors", []):
                print(f"CF_ERROR={err.get('code')} | {err.get('message')}")
        except Exception:
            pass
        continue
    except Exception as e:
        print("NETWORK_ERROR=" + type(e).__name__)
        continue

    if not data.get("success"):
        continue

    auth_ok = True
    print("CLOUDFLARE_AUTH=OK")
    projects = data.get("result", [])
    print("PAGES_PROJECTS=" + str(len(projects)))
    for p in projects:
        name = str(p.get("name", ""))
        print("PROJECT=" + name)
        if name == "ai-video-signal":
            found = True
            (home / ".aivs-v33-account-id").write_text(account_id)
            print("PROJECT_FOUND=YES")
            print("PROJECT_NAME=ai-video-signal")
            print("PRODUCTION_BRANCH=" + str(p.get("production_branch", "UNKNOWN")))
            print("SUBDOMAIN=" + str(p.get("subdomain", "UNKNOWN")))

if not auth_ok:
    print("CLOUDFLARE_AUTH=FAILED")
    sys.exit(3)
if not found:
    print("PROJECT_FOUND=NO")
    sys.exit(4)
