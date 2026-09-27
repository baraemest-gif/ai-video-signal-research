#!/usr/bin/env python3
from pathlib import Path
import os, json, uuid, urllib.request, urllib.error, sys

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
AID_FILE = Path.home() / ".aivs-v33-account-id"
WORKER_FILE = Path.home() / "aivs-v33-tools/v33_preview_overlay_worker.js"
PROJECT = "ai-video-signal"
BRANCH = "v33-sales-ctr-preview"

if not TOKEN:
    print("TOKEN=NOT_LOADED")
    sys.exit(1)
if not AID_FILE.exists():
    print("ACCOUNT_ID_CACHE=NOT_FOUND")
    sys.exit(2)
if not WORKER_FILE.exists():
    print("WORKER_FILE=NOT_FOUND")
    sys.exit(3)

AID = AID_FILE.read_text().strip()
WORKER = WORKER_FILE.read_text(encoding="utf-8")

boundary = "----AIVSv33v4" + uuid.uuid4().hex
parts = []

def field(name, value):
    parts.extend([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
        str(value).encode(),
        b"\r\n"
    ])

def filepart(name, filename, content, ctype):
    parts.extend([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode(),
        f"Content-Type: {ctype}\r\n\r\n".encode(),
        content.encode(),
        b"\r\n"
    ])

field("branch", BRANCH)
field("commit_dirty", "true")
field("commit_message", "AIVS v33 sales CTR safe preview overlay v4")
field("manifest", "{}")
filepart("_worker.js", "_worker.js", WORKER, "application/javascript")
parts.append(f"--{boundary}--\r\n".encode())
body = b"".join(parts)

url = f"https://api.cloudflare.com/client/v4/accounts/{AID}/pages/projects/{PROJECT}/deployments"
req = urllib.request.Request(
    url,
    data=body,
    method="POST",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
        "User-Agent": "AIVS-v33-Termux"
    }
)

try:
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP=" + str(e.code))
    raw = e.read().decode(errors="ignore")
    try:
        obj = json.loads(raw)
        for err in obj.get("errors", []):
            print("CF_ERROR=" + str(err.get("code")) + " | " + str(err.get("message")))
    except Exception:
        print(raw[:1200])
    sys.exit(4)

if not data.get("success"):
    print("DEPLOYMENT=FAILED")
    print(json.dumps(data.get("errors", [])))
    sys.exit(5)

d = data.get("result") or {}
print("DEPLOYMENT=CREATED")
print("ENV=" + str(d.get("environment")))
print("ID=" + str(d.get("id")))
print("URL=" + str(d.get("url")))
print("BRANCH=" + str(((d.get("deployment_trigger") or {}).get("metadata") or {}).get("branch")))
print("PRODUCTION_UNTOUCHED=YES")
print("OVERLAY_VERSION=V33_V4")
