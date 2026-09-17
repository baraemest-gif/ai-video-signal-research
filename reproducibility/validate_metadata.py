#!/usr/bin/env python3
"""Validate pre-DOI citation and Zenodo template metadata without external dependencies."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFF = ROOT / "CITATION.cff"
ZENODO_TEMPLATE = ROOT / ".zenodo.json.template"
ACTIVE_ZENODO = ROOT / ".zenodo.json"

errors: list[str] = []

if not CFF.exists():
    errors.append("CITATION.cff is missing")
else:
    cff = CFF.read_text(encoding="utf-8")
    required_fragments = [
        "cff-version: 1.2.0",
        'title: "AI Video Signal Research Dataset 2026"',
        "type: dataset",
        "authors:",
        'family-names: "Mestetef Ennaji"',
        'given-names: "Youssef"',
        'repository-code: "https://github.com/baraemest-gif/ai-video-signal-research"',
    ]
    for fragment in required_fragments:
        if fragment not in cff:
            errors.append(f"CITATION.cff missing required fragment: {fragment}")

    forbidden_pre_release_keys = ["doi:", "orcid:", "date-released:", "version:"]
    lowered = cff.lower()
    for key in forbidden_pre_release_keys:
        if key in lowered:
            errors.append(f"CITATION.cff contains pre-release field that must remain absent while HOLD: {key}")

if not ZENODO_TEMPLATE.exists():
    errors.append(".zenodo.json.template is missing")
else:
    try:
        z = json.loads(ZENODO_TEMPLATE.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f".zenodo.json.template is not valid JSON: {exc}")
        z = {}

    if z:
        if z.get("_status") != "TEMPLATE_ONLY_DO_NOT_RENAME_UNTIL_LICENSE_IS_RESOLVED":
            errors.append("Zenodo template control status is missing or changed")
        if z.get("title") != "AI Video Signal Research Dataset 2026":
            errors.append("Zenodo template title mismatch")
        if z.get("upload_type") != "dataset":
            errors.append("Zenodo template upload_type must be dataset")
        creators = z.get("creators") or []
        if not creators or creators[0].get("name") != "Mestetef Ennaji, Youssef":
            errors.append("Zenodo template creator metadata mismatch")
        serialized = json.dumps(z, ensure_ascii=False).lower()
        for forbidden in ['"doi"', '"orcid"', '"publication_date"', '"version"']:
            if forbidden in serialized:
                errors.append(f"Zenodo template contains pre-release metadata key: {forbidden}")

if ACTIVE_ZENODO.exists():
    errors.append("Active .zenodo.json must not exist while the release is HOLD")

if errors:
    print("FAIL: metadata validation")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("PASS: pre-DOI citation metadata and inert Zenodo template are valid.")
