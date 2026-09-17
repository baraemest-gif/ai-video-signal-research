#!/usr/bin/env python3
"""Safety guard preventing accidental DOI/release activation while the project is on HOLD."""

from __future__ import annotations

import json
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

is_hold = "STATUS: HOLD" in status_text

if not manifest_file.exists():
    errors.append("release-candidate/release-manifest.json is missing")
    manifest = {}
else:
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"release manifest is invalid JSON: {exc}")
        manifest = {}

if is_hold:
    if active_zenodo.exists():
        errors.append("Active .zenodo.json exists while RELEASE_STATUS is HOLD")
    if manifest:
        if manifest.get("publication_authorized") is not False:
            errors.append("publication_authorized must be false while HOLD")
        if manifest.get("doi") is not None:
            errors.append("doi must be null while HOLD")
        if manifest.get("orcid") is not None:
            errors.append("orcid must be null while HOLD unless explicitly confirmed")
        if manifest.get("status") != "HOLD_PRE_DOI":
            errors.append("release manifest status must be HOLD_PRE_DOI while RELEASE_STATUS is HOLD")
else:
    errors.append(
        "RELEASE_STATUS no longer contains HOLD. This guard requires an explicit release-readiness update before publication."
    )

if errors:
    print("FAIL: release safety guard")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("PASS: HOLD safety guard active; publication remains unauthorized and no DOI is asserted.")
