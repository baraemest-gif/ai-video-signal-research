#!/usr/bin/env python3
"""Check whether the current HOLD candidate is ready for freeze engineering.

A PASS here does NOT authorize publication, create a DOI, activate Zenodo metadata,
or change RELEASE_STATUS from HOLD. It only means provider/data reconciliation is
sufficiently closed to build a frozen final package.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "datasets" / "release-candidate-2026-09-17.csv"
JSON_PATH = ROOT / "datasets" / "release-candidate-2026-09-17.json"
MANIFEST_PATH = ROOT / "release-candidate" / "release-manifest.json"
STATUS_PATH = ROOT / "RELEASE_STATUS.md"
ACTIVE_ZENODO = ROOT / ".zenodo.json"
EXPECTED_COUNT = 14

UNRESOLVED_STATUSES = {
    "pending_first_party_access",
    "first_party_pricing_conflict",
    "partial_verified",
    "needs_correction_or_change_event",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    for path in (CSV_PATH, JSON_PATH, MANIFEST_PATH, STATUS_PATH):
        if not path.exists():
            fail(f"missing required pre-freeze file: {path.relative_to(ROOT)}")

    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    with JSON_PATH.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    with MANIFEST_PATH.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    status_text = STATUS_PATH.read_text(encoding="utf-8")

    if len(rows) != EXPECTED_COUNT:
        fail(f"expected {EXPECTED_COUNT} candidate providers")
    if payload.get("record_count") != EXPECTED_COUNT or len(payload.get("records", [])) != EXPECTED_COUNT:
        fail("JSON candidate does not contain exactly 14 records")
    if payload.get("status") != "HOLD":
        fail("release candidate must remain HOLD during freeze-readiness validation")
    if "STATUS: HOLD" not in status_text:
        fail("RELEASE_STATUS.md must remain HOLD during pre-freeze validation")

    names = [row.get("provider_name", "").strip() for row in rows]
    if len(set(names)) != EXPECTED_COUNT or any(not name for name in names):
        fail("candidate provider identity set is incomplete or duplicated")

    for row in rows:
        provider = row["provider_name"]
        status = row.get("reconciliation_status", "").strip()
        if status in UNRESOLVED_STATUSES:
            fail(f"{provider}: unresolved reconciliation status blocks freeze: {status}")
        if row.get("normalization_state", "").strip() in {"caution", "unavailable"}:
            fail(f"{provider}: caution/unavailable normalization state blocks freeze readiness")
        if not row.get("checked_at", "").strip():
            fail(f"{provider}: checked_at is required before freeze")
        if not row.get("research_note", "").strip():
            fail(f"{provider}: research_note is required before freeze")
        if not row.get("relationship_disclosure", "").strip():
            fail(f"{provider}: relationship disclosure is required before freeze")

    if manifest.get("provider_count") != EXPECTED_COUNT:
        fail("release manifest provider_count mismatch")
    if manifest.get("provider_reconciliation_complete_for_current_candidate") is not True:
        fail("release manifest does not mark current provider reconciliation complete")
    if manifest.get("status") != "HOLD_PRE_DOI":
        fail("release manifest must remain HOLD_PRE_DOI")
    if manifest.get("publication_authorized") is not False:
        fail("publication_authorized must remain false")
    if manifest.get("doi") is not None:
        fail("DOI must remain null before Zenodo assigns one")
    if manifest.get("orcid") is not None:
        fail("ORCID must remain null unless explicitly supplied and verified")
    if manifest.get("production_baseline") != "V70.7.5":
        fail("production baseline mismatch")
    if manifest.get("production_modified_by_research_work") is not False:
        fail("research work must not modify Production")
    if ACTIVE_ZENODO.exists():
        fail("active .zenodo.json must not exist while HOLD")

    required_pre_freeze_files = [
        ROOT / "CITATION.cff",
        ROOT / ".zenodo.json.template",
        ROOT / "LICENSE_STATUS.md",
        ROOT / "evidence" / "source-manifest.csv",
        ROOT / "evidence" / "relationship-disclosure-manifest.csv",
        ROOT / "methodology" / "methodology.md",
        ROOT / "datasets" / "data-dictionary.md",
        ROOT / "release-candidate" / "RELEASE_PLAYBOOK.md",
        ROOT / "release-candidate" / "ZENODO_DEPOSIT_FIELDS.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required_pre_freeze_files if not path.exists()]
    if missing:
        fail(f"missing required pre-freeze artifacts: {missing}")

    print(
        "PASS: current 14-provider candidate is READY_FOR_FREEZE_ENGINEERING; "
        "publication remains HOLD, unauthorized, and DOI-free."
    )


if __name__ == "__main__":
    main()
