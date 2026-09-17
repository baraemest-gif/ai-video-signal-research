#!/usr/bin/env python3
"""Validate citation metadata in both pre-DOI and published states."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFF = ROOT / "CITATION.cff"
ZENODO_TEMPLATE = ROOT / ".zenodo.json.template"
ACTIVE_ZENODO = ROOT / ".zenodo.json"
MANIFEST = ROOT / "release-candidate" / "release-manifest.json"

errors: list[str] = []

try:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
except Exception as exc:  # noqa: BLE001
    errors.append(f"release manifest is missing or invalid JSON: {exc}")
    manifest = {}

published = manifest.get("status") == "PUBLISHED_ZENODO_DOI"
expected_doi = manifest.get("doi")
expected_version = manifest.get("version")
expected_date = manifest.get("publication_date")

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

    keyed: dict[str, str] = {}
    for raw_line in cff.splitlines():
        stripped = raw_line.lstrip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        keyed[key.strip().lower()] = value.strip().strip('"')

    if published:
        if not expected_doi or not re.fullmatch(r"10\.5281/zenodo\.\d+", str(expected_doi)):
            errors.append("published manifest DOI is absent or malformed")
        if keyed.get("doi") != expected_doi:
            errors.append("CITATION.cff DOI does not match the published manifest DOI")
        if keyed.get("version") != expected_version:
            errors.append("CITATION.cff version does not match the published manifest version")
        if keyed.get("date-released") != expected_date:
            errors.append("CITATION.cff date-released does not match the publication date")
        expected_url = f"https://doi.org/{expected_doi}"
        if keyed.get("url") != expected_url:
            errors.append("CITATION.cff URL does not resolve through the published DOI")
    else:
        forbidden_pre_release_keys = {"doi", "orcid", "date-released", "version"}
        for key in forbidden_pre_release_keys:
            if key in keyed:
                errors.append(
                    f"CITATION.cff contains pre-release field that must remain absent while HOLD: {key}:"
                )

if not ZENODO_TEMPLATE.exists():
    errors.append(".zenodo.json.template is missing")
else:
    try:
        z = json.loads(ZENODO_TEMPLATE.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f".zenodo.json.template is not valid JSON: {exc}")
        z = {}

    if z:
        if z.get("title") != "AI Video Signal Research Dataset 2026":
            errors.append("Zenodo template title mismatch")
        if z.get("upload_type") != "dataset":
            errors.append("Zenodo template upload_type must be dataset")
        creators = z.get("creators") or []
        if not creators or creators[0].get("name") != "Mestetef Ennaji, Youssef":
            errors.append("Zenodo template creator metadata mismatch")
        rights = z.get("_custom_rights_statement", "")
        for phrase in [
            "© 2026 AI Video Signal",
            "Citation and limited excerpts",
            "prior written permission",
            "partners@aivideosignal.com",
        ]:
            if phrase not in rights:
                errors.append(f"Zenodo custom rights template missing required phrase: {phrase}")

if ACTIVE_ZENODO.exists():
    errors.append("Active .zenodo.json is not expected; the published Zenodo deposit used the verified manual custom-rights path")

if errors:
    print("FAIL: metadata validation")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

if published:
    print("PASS: published DOI, version, release date, citation metadata and custom-rights template are consistent.")
else:
    print("PASS: pre-DOI citation metadata, custom-rights template and inert Zenodo state are valid.")
