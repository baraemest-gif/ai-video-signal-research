#!/usr/bin/env python3
import base64, hashlib, os, urllib.parse, sys

key=os.environ.get("ETSY_KEYSTRING","").strip()
shared=os.environ.get("ETSY_SHARED_SECRET","").strip()
if not key or not shared:
    print("OAUTH_URL=BLOCKED_MISSING_ETSY_SECRETS")
    sys.exit(2)

def b64u(b):
    return base64.urlsafe_b64encode(b).decode().rstrip("=")

verifier=b64u(hashlib.sha256(f"joyprint17-pkce-v1:{key}:{shared}".encode()).digest())
challenge=b64u(hashlib.sha256(verifier.encode()).digest())
state=b64u(hashlib.sha256(f"joyprint17-state-v1:{shared}:{key}".encode()).digest())[:32]

params={
    "response_type":"code",
    "client_id":key,
    "redirect_uri":"https://yontorix.com/etsy/oauth/callback",
    "scope":"listings_r listings_w shops_r",
    "state":state,
    "code_challenge":challenge,
    "code_challenge_method":"S256",
}
url="https://www.etsy.com/oauth/connect?"+urllib.parse.urlencode(params)
print("JOYPRINT17_ETSY_AUTHORIZE_URL="+url)
print("REDIRECT_URI=https://yontorix.com/etsy/oauth/callback")
print("NEXT=Open the authorize URL, approve access, then copy the code query parameter into the GitHub secret ETSY_AUTH_CODE.")
