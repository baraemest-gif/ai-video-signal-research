#!/usr/bin/env python3
from pathlib import Path
import os, json, uuid, urllib.request, urllib.error, sys, time, hashlib

TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "").strip()
AID_FILE = Path.home() / ".aivs-v33-account-id"
WORKER_FILE = Path.home() / "aivs-v33-tools/v33_production_overlay_worker.js"
STATE_FILE = Path.home() / ".aivs-v33-rollback.json"

PROJECT = "ai-video-signal"
EXPECTED_CURRENT_PREFIX = "https://57ec6ea9.ai-video-signal.pages.dev"
PRODUCTION_BRANCH = "main"
PUBLIC_BASE = "https://aivideosignal.com"
UPSTREAM_BASE = "https://57ec6ea9.ai-video-signal.pages.dev"

TARGETS = {
    "/elevenlabs-cancellation-refund-policy/": "ElevenLabs Refund Policy 2026: 14-Day Rule, Cancellation",
    "/filmora-free-vs-paid/": "Filmora Free vs Paid 2026: Watermark, Price",
    "/best-ai-video-tools-for-compliance-training/": "Compare AI compliance video tools for policy/SOP training",
    "/filmora-free-trial/": "Filmora free trial guide for 2026",
    "/ai-video-pricing-benchmarks/": "compare AI video generators by workflow and pricing",
    "/ai-video-annual-vs-monthly-pricing-comparison/": "compare the leading AI video generators before choosing a billing term",
    "/ai-video-credits-usage-comparison/": "compare AI video generators by pricing model and workflow",
}
CONTROLS = ["/", "/best-ai-video-generators/", "/assets/site.js", "/assets/styles.css"]

if not TOKEN:
    print("TOKEN=NOT_LOADED"); sys.exit(1)
if not AID_FILE.exists():
    print("ACCOUNT_ID_CACHE=NOT_FOUND"); sys.exit(2)
if not WORKER_FILE.exists():
    print("WORKER_FILE=NOT_FOUND"); sys.exit(3)

AID = AID_FILE.read_text().strip()
WORKER = WORKER_FILE.read_text(encoding="utf-8")

def api(path, method="GET", data=None, headers=None):
    url = "https://api.cloudflare.com/client/v4" + path
    h = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
        "User-Agent": "AIVS-v33-Production-Safe"
    }
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
        return json.loads(raw.decode()) if raw else {}

def fetch(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AIVS-v33-QA",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, dict(r.headers.items()), r.read()

def rollback(deployment_id):
    print("ROLLBACK=START")
    path = f"/accounts/{AID}/pages/projects/{PROJECT}/deployments/{deployment_id}/rollback"
    data = api(path, method="POST", data=b"", headers={"Content-Type": "application/json"})
    if not data.get("success"):
        print("ROLLBACK=FAILED")
        return False
    print("ROLLBACK=SUCCESS")
    return True

# 1) Resolve current production and fail closed if it changed.
deps = api(f"/accounts/{AID}/pages/projects/{PROJECT}/deployments")
if not deps.get("success"):
    print("DEPLOYMENT_LIST=FAILED"); sys.exit(4)

productions = []
for d in deps.get("result", []):
    if d.get("environment") != "production":
        continue
    stage = d.get("latest_stage") or {}
    if stage.get("status") != "success":
        continue
    productions.append(d)

if not productions:
    print("CURRENT_PRODUCTION=NOT_FOUND"); sys.exit(5)

productions.sort(key=lambda x: x.get("created_on") or "", reverse=True)
current = productions[0]
current_id = current.get("id")
current_url = current.get("url") or ""

print("CURRENT_PRODUCTION_FOUND=YES")
print("CURRENT_URL_PREFIX_OK=" + ("YES" if current_url.startswith(EXPECTED_CURRENT_PREFIX) else "NO"))

if not current_url.startswith(EXPECTED_CURRENT_PREFIX):
    print("STOP=PRODUCTION_CHANGED_SINCE_QA")
    sys.exit(6)

STATE_FILE.write_text(json.dumps({
    "project": PROJECT,
    "rollback_deployment_id": current_id,
    "rollback_url": current_url,
    "saved_at": int(time.time())
}, indent=2))
print("ROLLBACK_STATE=SAVED")

# 2) Build multipart Direct Upload production deployment.
boundary = "----AIVSv33prod" + uuid.uuid4().hex
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

field("branch", PRODUCTION_BRANCH)
field("commit_dirty", "true")
field("commit_message", "AIVS v33 sales CTR production safe overlay")
field("manifest", "{}")
filepart("_worker.js", "_worker.js", WORKER, "application/javascript")
parts.append(f"--{boundary}--\r\n".encode())
body = b"".join(parts)

path = f"/accounts/{AID}/pages/projects/{PROJECT}/deployments"
try:
    data = api(path, method="POST", data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    })
except urllib.error.HTTPError as e:
    print("DEPLOYMENT_HTTP=" + str(e.code))
    print("PRODUCTION_UNCHANGED=YES")
    sys.exit(7)

if not data.get("success"):
    print("DEPLOYMENT=FAILED")
    print("PRODUCTION_UNCHANGED=YES")
    sys.exit(8)

new = data.get("result") or {}
new_id = new.get("id")
new_url = new.get("url")
new_env = new.get("environment")

print("DEPLOYMENT=CREATED")
print("ENV=" + str(new_env))
print("NEW_ID=" + str(new_id))
print("NEW_URL=" + str(new_url))

if new_env != "production":
    print("STOP=NOT_PRODUCTION")
    rollback(current_id)
    sys.exit(9)

# 3) Production QA with retries.
def sha256(b):
    return hashlib.sha256(b).hexdigest()

def qa_once():
    stamp = str(int(time.time()))
    for path, marker in TARGETS.items():
        status, headers, body = fetch(PUBLIC_BASE + path + "?v33qa=" + stamp)
        text = body.decode("utf-8", errors="ignore")
        if status != 200:
            return False, path + ":status"
        if marker not in text:
            return False, path + ":marker"
        if "https://aivideosignal.com" + path not in text:
            return False, path + ":canonical"
        if "noindex" in (headers.get("X-Robots-Tag", "") + headers.get("x-robots-tag", "")).lower():
            return False, path + ":noindex"

    for path in CONTROLS:
        _, _, a = fetch(PUBLIC_BASE + path + "?v33qa=" + stamp)
        _, _, b = fetch(UPSTREAM_BASE + path + "?v33qa=" + stamp)
        if sha256(a) != sha256(b):
            return False, path + ":control-diff"

    return True, "ok"

ok = False
reason = "unknown"
for i in range(12):
    try:
        ok, reason = qa_once()
    except Exception as e:
        ok, reason = False, type(e).__name__
    if ok:
        break
    time.sleep(3)

if not ok:
    print("QA=FAILED")
    print("QA_REASON=" + reason)
    rb = rollback(current_id)
    print("AUTO_ROLLBACK=" + ("SUCCESS" if rb else "FAILED"))
    sys.exit(10)

print("QA_7_OF_7=PASS")
print("NON_TARGET_CONTROL=PASS")
print("NO_NOINDEX=PASS")
print("PRODUCTION_V33=SUCCESS")
print("ROLLBACK_READY=YES")
