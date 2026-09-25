#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
import requests

API = "https://api.etsy.com/v3"
REFERENCE_LISTING_ID = 4581730353
TITLE = "HVAC Business Kit Canva Templates, Heating & Cooling Estimate, Quote, Client Forms, Marketing & Operations Bundle"
PRICE = "14.99"
QUANTITY = 999
TAGS = [
    "hvac business kit","hvac templates","hvac canva","heating cooling",
    "hvac estimate","hvac quote","hvac marketing","hvac contractor",
    "ac repair forms","service business","client intake","hvac flyer","operations kit"
]
DESCRIPTION = """Build a more organized and professional HVAC business with 18 editable Canva templates for leads, quoting, scheduling, job delivery, customer experience, local marketing and monthly tracking.

This digital kit is designed for HVAC contractors, heating and cooling businesses, AC repair companies and local home-service operators who want one practical system instead of disconnected forms and marketing files.

18 TEMPLATES INCLUDED
1. Quick Start Guide
2. Brand Positioning Worksheet
3. Service Menu & Pricing Sheet
4. Customer Intake Form
5. Estimate / Quote Template
6. Appointment & Job Confirmation
7. Job Execution Checklist
8. Quality Control Scorecard
9. Customer After-Service Care Sheet
10. Review + Referral Cards
11. Flyer Template
12. Door Hanger Template
13. 12 Social Media Post Templates
14. 30-Day Local Marketing Plan
15. Local SEO & Google Profile Checklist
16. SMS & Email Script Bank
17. Monthly KPI Tracker
18. Customization & Deployment Guide

EDITABLE IN CANVA
Customize your business name, logo, colors, services, service area, pricing, contact details, photos, offers and calls to action.

HOW IT WORKS
1. Purchase this digital listing.
2. Download the buyer-access PDF.
3. Open the Canva template link.
4. Create your own copy.
5. Customize the templates.
6. Export finished pages as PDF, PNG or JPG.

IMPORTANT
This is a digital product. No physical item will be shipped.
This kit is a business workflow and marketing template system. It is not legal, tax, accounting, engineering, licensing or regulatory advice. Review local requirements and replace sample information with truthful business information before use.
The editable template link and source design may not be resold, shared or redistributed as a competing template product.
"""

ROOT = Path(__file__).resolve().parent
IMAGE_PATH = ROOT / "assets" / "hvac-cover.png"
BUYER_PDF_PATH = ROOT / "build" / "HVAC_Business_Growth_Operations_18_BUYER_ACCESS.pdf"

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

def api_json(method, url, *, token, keystring, shared_secret, data=None, params=None):
    r = requests.request(
        method, url, headers=headers(token,keystring,shared_secret),
        data=data, params=params, timeout=45
    )
    if not r.ok:
        raise RuntimeError(f"{method} {url} failed: HTTP {r.status_code} {r.text[:1200]}")
    return r.json() if r.content else {}

def get_reference_listing(token, keystring, shared_secret):
    return api_json(
        "GET", f"{API}/application/listings/{REFERENCE_LISTING_ID}",
        token=token, keystring=keystring, shared_secret=shared_secret
    )

def find_existing(shop_id, token, keystring, shared_secret):
    for state in ("active","draft","inactive"):
        r = requests.get(
            f"{API}/application/shops/{shop_id}/listings",
            headers=headers(token,keystring,shared_secret),
            params={"state":state,"limit":100,"offset":0},
            timeout=45,
        )
        if not r.ok:
            continue
        for item in r.json().get("results",[]):
            if (item.get("title") or "").strip() == TITLE:
                return item
    return None

def create_draft(shop_id, ref, token, keystring, shared_secret):
    payload = [
        ("quantity",str(QUANTITY)),("title",TITLE),("description",DESCRIPTION),
        ("price",PRICE),("who_made",ref.get("who_made") or "i_did"),
        ("when_made",ref.get("when_made") or "2020_2026"),
        ("taxonomy_id",str(ref["taxonomy_id"])),("type","download"),
        ("is_supply","true"),("should_auto_renew","true")
    ]
    for tag in TAGS:
        payload.append(("tags",tag))
    out = api_json(
        "POST", f"{API}/application/shops/{shop_id}/listings",
        token=token,keystring=keystring,shared_secret=shared_secret,data=payload
    )
    print(f"DRAFT_CREATED={out.get('listing_id')}")
    return out

def get_images(shop_id, listing_id, token, keystring, shared_secret):
    r = requests.get(
        f"{API}/application/shops/{shop_id}/listings/{listing_id}/images",
        headers=headers(token,keystring,shared_secret), timeout=45
    )
    return r.json().get("results",[]) if r.ok else []

def get_files(shop_id, listing_id, token, keystring, shared_secret):
    r = requests.get(
        f"{API}/application/shops/{shop_id}/listings/{listing_id}/files",
        headers=headers(token,keystring,shared_secret), timeout=45
    )
    return r.json().get("results",[]) if r.ok else []

def upload_image(shop_id, listing_id, token, keystring, shared_secret):
    with IMAGE_PATH.open("rb") as fh:
        r = requests.post(
            f"{API}/application/shops/{shop_id}/listings/{listing_id}/images",
            headers=headers(token,keystring,shared_secret),
            files={"image":("hvac-cover.png",fh,"image/png")},
            data={"rank":"1","overwrite":"true"}, timeout=90
        )
    if not r.ok:
        raise RuntimeError(f"Image upload failed: HTTP {r.status_code} {r.text[:1200]}")
    print("IMAGE_UPLOAD=PASS")

def pdf_escape(s):
    return s.replace("\\","\\\\").replace("(","\\(").replace(")","\\)")

def make_minimal_pdf(canva_url):
    BUYER_PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "JOYPRINT17 - HVAC BUSINESS GROWTH & OPERATIONS KIT",
        "18 editable Canva templates - Digital product","",
        "YOUR CANVA TEMPLATE LINK",canva_url,"",
        "How to use:","1. Open the Canva template link.",
        "2. Choose Use template / Create your own copy.",
        "3. Replace placeholders with your business information.",
        "4. Customize logo, colors, services, pricing and calls to action.",
        "5. Export finished pages as PDF, PNG or JPG.","",
        "No physical item will be shipped.",
        "Do not resell or redistribute the editable template link or source design."
    ]
    content = ["BT","/F1 13 Tf","50 790 Td"]
    for line in lines:
        content.append(f"0 -24 Td ({pdf_escape(line)}) Tj")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1","replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets=[0]
    for i,obj in enumerate(objects,start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode()); pdf.extend(obj); pdf.extend(b"\nendobj\n")
    xref=len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n".encode()); pdf.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode())
    pdf.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    BUYER_PDF_PATH.write_bytes(pdf)
    print("BUYER_PDF_CREATED=PASS")

def upload_file(shop_id, listing_id, token, keystring, shared_secret):
    with BUYER_PDF_PATH.open("rb") as fh:
        r = requests.post(
            f"{API}/application/shops/{shop_id}/listings/{listing_id}/files",
            headers=headers(token,keystring,shared_secret),
            files={"file":(BUYER_PDF_PATH.name,fh,"application/pdf")},
            data={"name":"HVAC Business Growth & Operations Kit - START HERE"}, timeout=90
        )
    if not r.ok:
        raise RuntimeError(f"Digital file upload failed: HTTP {r.status_code} {r.text[:1200]}")
    print("DIGITAL_FILE_UPLOAD=PASS")

def activate(shop_id, listing_id, token, keystring, shared_secret):
    out = api_json(
        "PATCH", f"{API}/application/shops/{shop_id}/listings/{listing_id}",
        token=token,keystring=keystring,shared_secret=shared_secret,
        data={"state":"active","type":"download"}
    )
    print(f"LISTING_STATE={out.get('state')}")
    return out

def main():
    keystring=need("ETSY_KEYSTRING")
    shared_secret=need("ETSY_SHARED_SECRET")
    refresh_token=need("ETSY_REFRESH_TOKEN")
    canva_url=need("ETSY_HVAC_CANVA_TEMPLATE_URL")
    if not all((keystring,shared_secret,refresh_token,canva_url)):
        print("PRECHECK=BLOCKED_MISSING_SECRETS")
        sys.exit(2)
    if not IMAGE_PATH.exists():
        print(f"MISSING_ASSET={IMAGE_PATH}")
        sys.exit(3)

    token=refresh_access_token(keystring,refresh_token)
    ref=get_reference_listing(token,keystring,shared_secret)
    shop_id=ref.get("shop_id")
    taxonomy_id=ref.get("taxonomy_id")
    if not shop_id or not taxonomy_id:
        raise RuntimeError("Could not derive shop_id/taxonomy_id from reference listing")
    print(f"SHOP_ID_RESOLVED={shop_id}")
    print(f"TAXONOMY_ID_RESOLVED={taxonomy_id}")

    existing=find_existing(shop_id,token,keystring,shared_secret)
    if existing:
        listing=existing
        print(f"EXISTING_LISTING_FOUND={listing.get('listing_id')}")
        if listing.get("state")=="active":
            print("ALREADY_ACTIVE=YES")
            return
    else:
        listing=create_draft(shop_id,ref,token,keystring,shared_secret)

    listing_id=listing["listing_id"]
    if get_images(shop_id,listing_id,token,keystring,shared_secret):
        print("IMAGE_UPLOAD=SKIP_ALREADY_PRESENT")
    else:
        upload_image(shop_id,listing_id,token,keystring,shared_secret)

    make_minimal_pdf(canva_url)
    if get_files(shop_id,listing_id,token,keystring,shared_secret):
        print("DIGITAL_FILE_UPLOAD=SKIP_ALREADY_PRESENT")
    else:
        upload_file(shop_id,listing_id,token,keystring,shared_secret)

    out=activate(shop_id,listing_id,token,keystring,shared_secret)
    if out.get("state")!="active":
        raise RuntimeError(f"Activation did not return active state: {json.dumps(out)[:1200]}")
    print(f"PUBLISHED_LISTING_ID={listing_id}")
    print("JOYPRINT17_HVAC_PUBLISH=SUCCESS")

if __name__=="__main__":
    main()
