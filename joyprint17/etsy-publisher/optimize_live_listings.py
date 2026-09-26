#!/usr/bin/env python3
import os, sys, requests

API = "https://api.etsy.com/v3"

LISTINGS = {
  4581934116: {
    "expect": "Window Cleaning",
    "title": "Window Cleaning Business Forms Bundle, 30 Editable Templates, Estimate, Quote, Work Order, Checklists, Client Forms",
    "tags": ["window clean forms","window business","cleaning forms","estimate template","quote template","work order form","client intake","service checklist","route planner","invoice template","window cleaner","business forms","cleaning toolkit"],
  },
  4581923768: {
    "expect": "Junk Removal",
    "title": "Junk Removal Business Forms Bundle, 30 Editable Templates, Estimate, Quote, Work Order, Load Sheet, Client & Job Forms",
    "tags": ["junk removal forms","junk business","hauling forms","cleanout forms","estimate template","invoice template","work order form","load sheet","route planner","client intake","job checklist","hauling business","business forms"],
  },
  4581841815: {
    "expect": "Handyman",
    "title": "Handyman Business Forms Bundle, 30 Editable Templates, Estimate, Quote, Work Order, Job Checklist, Client Intake Forms",
    "tags": ["handyman forms","handyman business","contractor forms","home repair forms","estimate template","quote template","invoice template","work order form","job checklist","client intake","scope of work","service business","business forms"],
  },
  4581829241: {
    "expect": "Lawn Care",
    "title": "Lawn Care Business Forms Bundle, 30 Editable Templates, Estimate, Quote, Invoice, Route Planner, Work Order & Client Forms",
    "tags": ["lawn care forms","lawn business","landscaping forms","lawn mowing forms","estimate template","quote template","invoice template","work order form","route planner","client intake","service checklist","lawn care business","business forms"],
  },
  4572422453: {
    "expect": "Pressure Washing",
    "title": "Pressure Washing Business Bundle, 178 Canva Templates, Social Media, Flyers, Door Hangers, Business Forms & Marketing Kit",
    "tags": ["pressure washing","power washing","canva templates","business bundle","social media kit","door hanger","flyer template","postcard template","estimate template","invoice template","marketing kit","exterior cleaning","cleaning business"],
  },
}

def need(name):
    value = os.environ.get(name, "").strip()
    if not value:
        print(f"MISSING_SECRET={name}")
    return value

def headers(token, keystring, shared_secret):
    return {
        "x-api-key": f"{keystring}:{shared_secret}",
        "Authorization": f"Bearer {token}",
    }

def refresh_access_token(keystring, refresh_token):
    r = requests.post(
        f"{API}/public/oauth/token",
        data={"grant_type":"refresh_token","client_id":keystring,"refresh_token":refresh_token},
        timeout=30,
    )
    if not r.ok:
        raise RuntimeError(f"OAuth refresh failed: HTTP {r.status_code} {r.text[:500]}")
    print("OAUTH_REFRESH=PASS")
    return r.json()["access_token"]

def get_listing(listing_id, token, keystring, shared_secret):
    r = requests.get(
        f"{API}/application/listings/{listing_id}",
        headers=headers(token,keystring,shared_secret), timeout=30
    )
    if not r.ok:
        raise RuntimeError(f"GET listing {listing_id}: HTTP {r.status_code} {r.text[:500]}")
    return r.json()

def patch_listing(shop_id, listing_id, spec, token, keystring, shared_secret):
    data = [("title", spec["title"])]
    for tag in spec["tags"]:
        data.append(("tags", tag))
    r = requests.patch(
        f"{API}/application/shops/{shop_id}/listings/{listing_id}",
        headers=headers(token,keystring,shared_secret),
        data=data, timeout=45
    )
    if not r.ok:
        raise RuntimeError(f"PATCH listing {listing_id}: HTTP {r.status_code} {r.text[:800]}")
    return r.json()

def main():
    keystring = need("ETSY_KEYSTRING")
    shared_secret = need("ETSY_SHARED_SECRET")
    refresh_token = need("ETSY_REFRESH_TOKEN")
    if not all((keystring, shared_secret, refresh_token)):
        print("PRECHECK=BLOCKED_MISSING_SECRETS")
        sys.exit(2)

    for listing_id, spec in LISTINGS.items():
        if len(spec["title"]) > 140:
            raise RuntimeError(f"TITLE_TOO_LONG={listing_id}:{len(spec['title'])}")
        if len(spec["tags"]) != 13:
            raise RuntimeError(f"TAG_COUNT_INVALID={listing_id}:{len(spec['tags'])}")
        for tag in spec["tags"]:
            if len(tag) > 20:
                raise RuntimeError(f"TAG_TOO_LONG={listing_id}:{tag}:{len(tag)}")

    token = refresh_access_token(keystring, refresh_token)

    shop_id = None
    snapshots = {}
    for listing_id, spec in LISTINGS.items():
        item = get_listing(listing_id, token, keystring, shared_secret)
        snapshots[listing_id] = item
        if shop_id is None:
            shop_id = item.get("shop_id")
        if not shop_id or item.get("shop_id") != shop_id:
            raise RuntimeError(f"SHOP_MISMATCH={listing_id}")
        if item.get("state") != "active":
            raise RuntimeError(f"NOT_ACTIVE={listing_id}:{item.get('state')}")
        current_title = (item.get("title") or "").strip()
        if spec["expect"].lower() not in current_title.lower():
            raise RuntimeError(f"TITLE_IDENTITY_MISMATCH={listing_id}:{current_title}")
        print(f"PRECHECK_PASS={listing_id}|{current_title}")

    for listing_id, spec in LISTINGS.items():
        out = patch_listing(shop_id, listing_id, spec, token, keystring, shared_secret)
        print(f"PATCH_PASS={listing_id}|{out.get('title')}")

    for listing_id, spec in LISTINGS.items():
        item = get_listing(listing_id, token, keystring, shared_secret)
        if item.get("title") != spec["title"]:
            raise RuntimeError(f"VERIFY_TITLE_FAIL={listing_id}")
        actual_tags = item.get("tags") or []
        if sorted(t.lower() for t in actual_tags) != sorted(t.lower() for t in spec["tags"]):
            raise RuntimeError(f"VERIFY_TAGS_FAIL={listing_id}:{actual_tags}")
        print(f"VERIFY_PASS={listing_id}")

    print("JOYPRINT17_LIVE_SEO_PATCH=SUCCESS")

if __name__ == "__main__":
    main()
