#!/usr/bin/env python3
"""AI Video Signal v33 sales/CTR patch.

Purpose:
- Apply only small, reversible SEO/CRO changes to a CURRENT AI Video Signal source tree.
- Refuse to write if expected live metadata / structure is not present.
- Never touch _worker.js, affiliate URLs, checkout, CSS, JS, canonical or robots.

Usage:
  python patch_current_production.py /path/to/current/site             # dry run
  python patch_current_production.py /path/to/current/site --apply     # write

Exit code 0 = checks passed (and writes completed when --apply).
Any mismatch aborts before any file is written.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PATCH_ID = "AIVS-v33-SALES-CTR-2026-09-27"

@dataclass(frozen=True)
class MetaPatch:
    path: str
    canonical: str
    expected_titles: tuple[str, ...]
    new_title: str | None = None
    expected_descriptions: tuple[str, ...] = ()
    new_description: str | None = None

META_PATCHES = [
    MetaPatch(
        path="elevenlabs-cancellation-refund-policy/index.html",
        canonical="https://aivideosignal.com/elevenlabs-cancellation-refund-policy/",
        expected_titles=("ElevenLabs Cancellation & Refund Policy 2026: 14-Day Rule",),
        new_title="ElevenLabs Refund Policy 2026: 14-Day Rule, Cancellation & Credits",
        expected_descriptions=("ElevenLabs cancellation and refund policy for 2026: how to cancel, the 14-day unused-credit refund rule, credit loss, mobile purchases and EU rights.",),
        new_description="ElevenLabs refund policy 2026: see the 14-day unused-credit rule, how cancellation works, what happens to credits, and mobile/EU refund paths.",
    ),
    MetaPatch(
        path="filmora-free-vs-paid/index.html",
        canonical="https://aivideosignal.com/filmora-free-vs-paid/",
        expected_titles=("Filmora Free vs Paid 2026: Watermark, Limits & Price",),
        new_title="Filmora Free vs Paid 2026: Watermark, Price & Is It Worth It?",
        expected_descriptions=("Filmora Free vs Paid in 2026: compare free-version limitations, watermark rules, exports, AI credits and paid-plan differences before you upgrade.",),
        new_description="Filmora Free vs Paid 2026: compare watermark rules, export limits, AI credits, current pricing and when upgrading is actually worth it.",
    ),
    MetaPatch(
        path="best-ai-video-tools-for-compliance-training/index.html",
        canonical="https://aivideosignal.com/best-ai-video-tools-for-compliance-training/",
        expected_titles=("AI Compliance Videos 2026: Best Tools for Training",),
        new_title=None,
        expected_descriptions=("A practical comparison of AI video platforms for compliance training, policy updates and multilingual employee education.",),
        new_description="Compare AI compliance video tools for policy/SOP training, SCORM/LMS delivery, completion tracking, localization, version updates and knowledge checks.",
    ),
    MetaPatch(
        path="filmora-free-trial/index.html",
        canonical="https://aivideosignal.com/filmora-free-trial/",
        expected_titles=("Filmora Free Trial 2026: Watermark, Free Export & What You Get",),
        new_title=None,
        expected_descriptions=("Filmora free trial, watermark rules, account rewards and buying guidance for 2026.",),
        new_description="Filmora free trial guide for 2026: watermark rules, the current free-export reward, achievement trials, Creative Assets trial and when to upgrade.",
    ),
]

LINK_PATCHES = [
    {
        "path": "ai-video-pricing-benchmarks/index.html",
        "canonical": "https://aivideosignal.com/ai-video-pricing-benchmarks/",
        "anchor": "compare AI video generators by workflow and pricing",
        "href": "/best-ai-video-generators/",
        "marker": "<h2>What the benchmark actually says</h2>",
        "paragraph": '<p class="internal-authority-link v33-sales-ctr">Before choosing from the benchmark, <a href="/best-ai-video-generators/">compare AI video generators by workflow and pricing</a> to match subscription cost with the job you actually need to do.</p>',
    },
    {
        "path": "ai-video-annual-vs-monthly-pricing-comparison/index.html",
        "canonical": "https://aivideosignal.com/ai-video-annual-vs-monthly-pricing-comparison/",
        "anchor": "compare the leading AI video generators before choosing a billing term",
        "href": "/best-ai-video-generators/",
        "marker": "<h2>Evidence behind this decision</h2>",
        "paragraph": '<p class="internal-authority-link v33-sales-ctr">If you have not settled on a provider yet, <a href="/best-ai-video-generators/">compare the leading AI video generators before choosing a billing term</a>; annual savings matter only after the workflow fit is proven.</p>',
    },
    {
        "path": "ai-video-credits-usage-comparison/index.html",
        "canonical": "https://aivideosignal.com/ai-video-credits-usage-comparison/",
        "anchor": "compare AI video generators by pricing model and workflow",
        "href": "/best-ai-video-generators/",
        "marker": "<h2>How six AI usage systems compare</h2>",
        "paragraph": '<p class="internal-authority-link v33-sales-ctr">For the broader purchase decision, <a href="/best-ai-video-generators/">compare AI video generators by pricing model and workflow</a> before treating any vendor credit as equivalent value.</p>',
    },
]

CRITICAL_UNTOUCHED = ["_worker.js", "assets/site.js", "assets/styles.css", "_headers"]

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def normalize_text(s: str) -> str:
    return html.unescape(s).strip()

def get_title(doc: str) -> str | None:
    m = re.search(r"<title>(.*?)</title>", doc, flags=re.I | re.S)
    return normalize_text(m.group(1)) if m else None

def replace_title(doc: str, new: str) -> str:
    return re.sub(r"(<title>)(.*?)(</title>)", lambda m: m.group(1) + html.escape(new, quote=False) + m.group(3), doc, count=1, flags=re.I | re.S)

def iter_meta_tags(doc: str):
    for m in re.finditer(r"<meta\b[^>]*>", doc, flags=re.I | re.S):
        yield m

def attr_value(tag: str, attr: str) -> str | None:
    m = re.search(rf"\b{re.escape(attr)}\s*=\s*([\"'])(.*?)\1", tag, flags=re.I | re.S)
    return html.unescape(m.group(2)) if m else None

def get_meta(doc: str, key: str) -> str | None:
    for m in iter_meta_tags(doc):
        tag = m.group(0)
        if attr_value(tag, "name") == key or attr_value(tag, "property") == key:
            return attr_value(tag, "content")
    return None

def replace_meta(doc: str, key: str, new: str, required: bool = True) -> str:
    matches = []
    for m in iter_meta_tags(doc):
        tag = m.group(0)
        if attr_value(tag, "name") == key or attr_value(tag, "property") == key:
            matches.append(m)
    if not matches:
        if required:
            raise ValueError(f"missing meta {key}")
        return doc
    if len(matches) != 1:
        raise ValueError(f"expected one meta {key}, found {len(matches)}")
    m = matches[0]
    tag = m.group(0)
    escaped = html.escape(new, quote=True)
    if re.search(r"\bcontent\s*=", tag, flags=re.I):
        new_tag = re.sub(r"\bcontent\s*=\s*([\"'])(.*?)\1", lambda x: f'content="{escaped}"', tag, count=1, flags=re.I | re.S)
    else:
        new_tag = tag[:-1] + f' content="{escaped}">'
    return doc[:m.start()] + new_tag + doc[m.end():]

def validate_canonical(doc: str, canonical: str) -> None:
    tags = [m.group(0) for m in re.finditer(r"<link\b[^>]*>", doc, flags=re.I | re.S) if attr_value(m.group(0), "rel") == "canonical"]
    hrefs = [attr_value(t, "href") for t in tags]
    if canonical not in hrefs:
        raise ValueError(f"canonical mismatch; expected {canonical!r}, got {hrefs!r}")

def update_social_meta(doc: str, title: str | None, desc: str | None) -> str:
    out = doc
    if title:
        for key in ("og:title", "twitter:title"):
            if get_meta(out, key) is not None:
                out = replace_meta(out, key, title)
    if desc:
        for key in ("og:description", "twitter:description"):
            if get_meta(out, key) is not None:
                out = replace_meta(out, key, desc)
    return out

def patch_meta_file(doc: str, spec: MetaPatch) -> str:
    validate_canonical(doc, spec.canonical)
    old_title = get_title(doc)
    if old_title not in spec.expected_titles:
        raise ValueError(f"title guard failed: {old_title!r}; expected one of {spec.expected_titles!r}")
    old_desc = get_meta(doc, "description")
    if spec.expected_descriptions and old_desc not in spec.expected_descriptions:
        raise ValueError(f"description guard failed: {old_desc!r}; expected one of {spec.expected_descriptions!r}")
    out = doc
    if spec.new_title:
        out = replace_title(out, spec.new_title)
    if spec.new_description:
        out = replace_meta(out, "description", spec.new_description)
    return update_social_meta(out, spec.new_title, spec.new_description)

def patch_link_file(doc: str, spec: dict) -> str:
    validate_canonical(doc, spec["canonical"])
    if spec["anchor"].lower() in html.unescape(doc).lower():
        return doc
    marker = spec["marker"]
    if marker not in doc:
        raise ValueError(f"insertion marker missing: {marker}")
    return doc.replace(marker, spec["paragraph"] + marker, 1)

def read_bytes_if_exists(root: Path, rel: str):
    p = root / rel
    return p.read_bytes() if p.exists() else None

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="Current AI Video Signal site root")
    ap.add_argument("--apply", action="store_true", help="Write changes. Without this flag: dry-run only.")
    ap.add_argument("--manifest", type=Path, help="Optional JSON QA manifest output path")
    args = ap.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        print(f"ERROR: site root not found: {root}", file=sys.stderr)
        return 2

    critical_before = {rel: read_bytes_if_exists(root, rel) for rel in CRITICAL_UNTOUCHED}
    staged, before_sha, after_sha, errors = {}, {}, {}, []

    for spec in META_PATCHES:
        p = root / spec.path
        if not p.exists():
            errors.append(f"{spec.path}: missing file")
            continue
        raw = p.read_bytes(); before_sha[spec.path] = sha256_bytes(raw)
        try:
            new = patch_meta_file(raw.decode("utf-8"), spec)
            staged[p] = new
            after_sha[spec.path] = sha256_bytes(new.encode("utf-8"))
        except Exception as e:
            errors.append(f"{spec.path}: {e}")

    for spec in LINK_PATCHES:
        p = root / spec["path"]
        if not p.exists():
            errors.append(f"{spec['path']}: missing file")
            continue
        raw = p.read_bytes(); before_sha[spec["path"]] = sha256_bytes(raw)
        try:
            new = patch_link_file(raw.decode("utf-8"), spec)
            staged[p] = new
            after_sha[spec["path"]] = sha256_bytes(new.encode("utf-8"))
        except Exception as e:
            errors.append(f"{spec['path']}: {e}")

    if errors:
        print("ABORT: current source failed safety guards. Nothing was written.")
        for e in errors:
            print(" -", e)
        return 3

    changed = [str(p.relative_to(root)) for p, content in staged.items() if p.read_text("utf-8") != content]
    unchanged = [str(p.relative_to(root)) for p, content in staged.items() if p.read_text("utf-8") == content]

    if args.apply:
        for p, content in staged.items():
            if p.read_text("utf-8") == content:
                continue
            tmp = p.with_suffix(p.suffix + ".v33tmp")
            tmp.write_text(content, encoding="utf-8")
            tmp.replace(p)

    critical_after = {rel: read_bytes_if_exists(root, rel) for rel in CRITICAL_UNTOUCHED}
    critical_status = {}
    for rel in CRITICAL_UNTOUCHED:
        b, a = critical_before[rel], critical_after[rel]
        critical_status[rel] = {"exists": b is not None, "unchanged": b == a, "sha256": sha256_bytes(a) if a is not None else None}
        if b != a:
            print(f"FATAL: critical file changed unexpectedly: {rel}", file=sys.stderr)
            return 4

    manifest = {
        "patch_id": PATCH_ID,
        "mode": "apply" if args.apply else "dry-run",
        "root": str(root),
        "changed_files": changed,
        "already_compliant_files": unchanged,
        "before_sha256": before_sha,
        "after_sha256_expected": after_sha,
        "critical_untouched": critical_status,
        "safety": {
            "affiliate_urls_modified": False,
            "worker_modified": False,
            "javascript_modified": False,
            "css_modified": False,
            "canonical_modified": False,
            "robots_modified": False,
        },
    }
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    if args.manifest:
        args.manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
