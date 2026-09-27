#!/usr/bin/env python3
from pathlib import Path
import os, json, urllib.request, urllib.error, sys

token = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
aid_file = Path.home() / ".aivs-v33-account-id"
if not token:
    print("TOKEN=NOT_LOADED"); sys.exit(1)
if not aid_file.exists():
    print("ACCOUNT_ID_CACHE=NOT_FOUND"); sys.exit(2)

aid = aid_file.read_text().strip()
project = "ai-video-signal"
url = f"https://api.cloudflare.com/client/v4/accounts/{aid}/pages/projects/{project}"
req = urllib.request.Request(url, headers={
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "User-Agent": "AIVS-v33-Termux"
})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        data=json.loads(r.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP="+str(e.code))
    try:
        body=json.loads(e.read().decode())
        for err in body.get("errors",[]): print("CF_ERROR="+str(err.get("code"))+" | "+str(err.get("message")))
    except Exception: pass
    sys.exit(3)

p=data.get("result") or {}
print("PROJECT="+str(p.get("name")))
print("PRODUCTION_BRANCH="+str(p.get("production_branch")))
print("USES_FUNCTIONS="+str(p.get("uses_functions")))
print("PRODUCTION_SCRIPT_NAME="+str(p.get("production_script_name")))
print("PREVIEW_SCRIPT_NAME="+str(p.get("preview_script_name")))
source=p.get("source")
if source:
    print("SOURCE_TYPE="+str(source.get("type")))
    cfg=source.get("config") or {}
    print("SOURCE_OWNER="+str(cfg.get("owner")))
    print("SOURCE_REPO="+str(cfg.get("repo_name")))
    print("SOURCE_PRODUCTION_DEPLOYMENTS="+str(cfg.get("production_deployments_enabled")))
    print("SOURCE_PREVIEW_SETTING="+str(cfg.get("preview_deployment_setting")))
else:
    print("SOURCE_TYPE=DIRECT_UPLOAD_OR_NONE")
build=p.get("build_config") or {}
print("BUILD_COMMAND="+str(build.get("build_command")))
print("DESTINATION_DIR="+str(build.get("destination_dir")))
print("ROOT_DIR="+str(build.get("root_dir")))
