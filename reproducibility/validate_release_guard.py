#!/usr/bin/env python3
"""Validate release-state safety before and after DOI publication."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
status_file = ROOT / "RELEASE_STATUS.md"
manifest_file = ROOT / "release-candidate" / "release-manifest.json"
active_zenodo = ROOT / ".zenodo.json"

errors: list[str] = []

if not status_file.exists():
    errors.append("RELEASE_STATUS.md is missing")
    status_text = ""
else:
    status_text = status_file.read_text(encoding="utf-8")

if not manifest_file.exists():
    errors.append("release-candidate/release-manifest.json is missing")
    manifest = {}
else:
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"release manifest is invalid JSON: {exc}")
        manifest = {}

manifest_status = manifest.get("status") if manifest else None
is_hold = "STATUS: HOLD" in status_text
is_published = "STATUS: PUBLISHED" in status_text

if active_zenodo.exists():
    errors.append("Active .zenodo.json is not expected; verified manual Zenodo deposit path is authoritative")

if is_hold:
    if manifest:
        if manifest.get("publication_authorized") is not False:
            errors.append("publication_authorized must be false while HOLD")
        if manifest.get("doi") is not None:
            errors.append("doi must be null while HOLD")
        if manifest.get("orcid") is not None:
            errors.append("orcid must be null while HOLD unless explicitly confirmed")
        if manifest_status != "HOLD_PRE_DOI":
            errors.append("release manifest status must be HOLD_PRE_DOI while RELEASE_STATUS is HOLD")
elif is_published:
    if manifest_status != "PUBLISHED_ZENODO_DOI":
        errors.append("published RELEASE_STATUS requires PUBLISHED_ZENODO_DOI manifest status")
    if manifest.get("publication_authorized") is not True:
        errors.append("publication_authorized must be true after verified publication")
    doi = manifest.get("doi")
    if not isinstance(doi, str) or not re.fullmatch(r"10\.5281/zenodo\.\d+", doi):
        errors.append("published manifest must contain a real Zenodo DOI")
    if manifest.get("zenodo_record_published") is not True:
        errors.append("zenodo_record_published must be true after publication")
    if manifest.get("production_baseline") != "V70.7.5":
        errors.append("production baseline mismatch")
    if manifest.get("production_modified_by_research_work") is not False:
        errors.append("research publication must not modify Production")
else:
    errors.append("RELEASE_STATUS must explicitly declare HOLD or PUBLISHED state")

if errors:
    print("FAIL: release state guard")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

if is_published:
    print("PASS: published DOI state is internally consistent and Production remains untouched.")
else:
    print("PASS: HOLD safety guard active; publication remains unauthorized and no DOI is asserted.")
