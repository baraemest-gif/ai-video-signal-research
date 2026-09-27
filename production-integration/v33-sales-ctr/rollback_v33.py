#!/usr/bin/env python3
from pathlib import Path
import os, json, urllib.request, sys

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
AID_FILE = Path.home() / ".aivs-v33-account-id"
STATE_FILE = Path.home() / ".aivs-v33-rollback.json"
PROJECT = "ai-video-signal"

if not TOKEN:
    print("TOKEN=NOT_LOADED"); sys.exit(1)
if not AID_FILE.exists():
    print("ACCOUNT_ID_CACHE=NOT_FOUND"); sys.exit(2)
if not STATE_FILE.exists():
    print("ROLLBACK_STATE=NOT_FOUND"); sys.exit(3)

AID = AID_FILE.read_text().strip()
state = json.loads(STATE_FILE.read_text())
deployment_id = state.get("rollback_deployment_id")
if not deployment_id:
    print("ROLLBACK_ID=NOT_FOUND"); sys.exit(4)

url = f"https://api.cloudflare.com/client/v4/accounts/{AID}/pages/projects/{PROJECT}/deployments/{deployment_id}/rollback"
req = urllib.request.Request(
    url,
    data=b"",
    method="POST",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "AIVS-v33-Rollback"
    }
)
with urllib.request.urlopen(req, timeout=60) as r:
    data = json.loads(r.read().decode())

if not data.get("success"):
    print("ROLLBACK=FAILED"); sys.exit(5)

print("ROLLBACK=SUCCESS")
print("PROJECT=ai-video-signal")
print("TARGET_URL=" + str(state.get("rollback_url")))
