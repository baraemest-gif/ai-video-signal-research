import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

token = os.getenv("CLOUDFLARE_API_TOKEN", "").strip()
account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"].strip()
database_id = os.environ["CLOUDFLARE_D1_DATABASE_ID"].strip()

if not token:
    print("::error::Missing GitHub Actions secret CLOUDFLARE_API_TOKEN")
    sys.exit(2)

sql_path = Path("ops/belorie/pending.sql")
sql = sql_path.read_text(encoding="utf-8").strip()
if not sql:
    print("::error::pending.sql is empty")
    sys.exit(2)

url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/d1/database/{database_id}/query"
payload = json.dumps({"sql": sql}).encode("utf-8")
request = urllib.request.Request(
    url,
    data=payload,
    method="POST",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "belorie-github-d1-ops/1.0",
    },
)

try:
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read().decode("utf-8")
except urllib.error.HTTPError as exc:
    body = exc.read().decode("utf-8", "replace")
    print(f"::error::Cloudflare HTTP {exc.code}: {body}")
    sys.exit(1)

data = json.loads(body)
if not data.get("success"):
    print("::error::Cloudflare D1 query failed")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    sys.exit(1)

print("BELORIE_D1_APPLY_OK")
print(json.dumps(data.get("result"), indent=2, ensure_ascii=False))
