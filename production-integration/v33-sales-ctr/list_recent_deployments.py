#!/usr/bin/env python3
from pathlib import Path
import os, json, urllib.request, urllib.error, sys

token=os.environ.get("CLOUDFLARE_API_TOKEN","").strip()
aid_file=Path.home()/".aivs-v33-account-id"
if not token:
    print("TOKEN=NOT_LOADED"); sys.exit(1)
if not aid_file.exists():
    print("ACCOUNT_ID_CACHE=NOT_FOUND"); sys.exit(2)

aid=aid_file.read_text().strip()
project="ai-video-signal"
url=f"https://api.cloudflare.com/client/v4/accounts/{aid}/pages/projects/{project}/deployments?per_page=5"
req=urllib.request.Request(url,headers={
    "Authorization":f"Bearer {token}",
    "Accept":"application/json",
    "User-Agent":"AIVS-v33-Termux"
})
try:
    with urllib.request.urlopen(req,timeout=20) as r:
        data=json.loads(r.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP="+str(e.code))
    try:
        body=json.loads(e.read().decode())
        for err in body.get("errors",[]): print("CF_ERROR="+str(err.get("code"))+" | "+str(err.get("message")))
    except Exception: pass
    sys.exit(3)

items=data.get("result") or []
print("DEPLOYMENTS="+str(len(items)))
for i,d in enumerate(items,1):
    print(f"--- DEPLOYMENT_{i} ---")
    print("ID="+str(d.get("id")))
    print("ENV="+str(d.get("environment")))
    print("CREATED_ON="+str(d.get("created_on")))
    print("LATEST_STAGE="+str((d.get("latest_stage") or {}).get("status")))
    trig=d.get("deployment_trigger") or {}
    meta=trig.get("metadata") or {}
    print("BRANCH="+str(meta.get("branch")))
    print("COMMIT_HASH="+str(meta.get("commit_hash")))
    print("URL="+str(d.get("url")))
    aliases=d.get("aliases") or []
    if aliases: print("ALIASES="+" | ".join(map(str,aliases)))
