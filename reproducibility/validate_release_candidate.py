#!/usr/bin/env python3
"""Validate AI Video Signal pre-DOI release-candidate CSV/JSON parity.

Standard-library only. This validator intentionally fails if the candidate is
not HOLD, if provider identity differs between formats, if enum values are
invalid, or if unresolved states are silently converted into normalized data.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "datasets" / "release-candidate-2026-09-17.csv"
JSON_PATH = ROOT / "datasets" / "release-candidate-2026-09-17.json"

ALLOWED_NORMALIZATION = {"normalized", "not_normalized", "unclear", "caution", "unavailable"}
ALLOWED_CRES = {"documented_clear", "documented_conditional", "unclear", "restricted", "not_checked"}
EXPECTED_COUNT = 14
EXPECTED_CANDIDATE_ID = "RC-2026-09-17-HOLD"

REQUIRED_FIELDS = {
    "provider_name",
    "canonical_url",
    "plan_name",
    "billing_interval",
    "advertised_price",
    "currency",
    "credits_or_allowance",
    "model_name",
    "workflow_name",
    "duration",
    "resolution",
    "generation_mode",
    "nominal_generation_cost",
    "retry_assumption",
    "approved_output_cost",
    "free_access_state",
    "commercial_rights_evidence_status",
    "source_url",
    "source_type",
    "evidence_tier",
    "checked_at",
    "last_material_change_at",
    "relationship_disclosure",
    "normalization_state",
    "reconciliation_status",
    "research_note",
    "release_id",
    "record_version",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def normalize_record(record: dict[str, str]) -> dict[str, str]:
    return {key: "" if value is None else str(value) for key, value in record.items()}


def main() -> None:
    if not CSV_PATH.exists() or not JSON_PATH.exists():
        fail("release-candidate CSV or JSON is missing")

    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        csv_rows = [normalize_record(row) for row in csv.DictReader(handle)]

    with JSON_PATH.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    if payload.get("status") != "HOLD":
        fail("candidate status must remain HOLD until all release gates pass")
    if payload.get("candidate_id") != EXPECTED_CANDIDATE_ID:
        fail("unexpected candidate_id")

    json_rows = [normalize_record(row) for row in payload.get("records", [])]
    if payload.get("record_count") != len(json_rows):
        fail("JSON record_count does not match records length")

    if len(csv_rows) != EXPECTED_COUNT or len(json_rows) != EXPECTED_COUNT:
        fail(f"expected {EXPECTED_COUNT} providers in both formats")

    csv_names = [row.get("provider_name", "") for row in csv_rows]
    json_names = [row.get("provider_name", "") for row in json_rows]
    if len(set(csv_names)) != EXPECTED_COUNT or len(set(json_names)) != EXPECTED_COUNT:
        fail("provider names must be unique")
    if csv_names != json_names:
        fail("CSV and JSON provider order/identity differ")

    csv_field_set = set(csv_rows[0]) if csv_rows else set()
    if REQUIRED_FIELDS - csv_field_set:
        fail(f"CSV missing required fields: {sorted(REQUIRED_FIELDS - csv_field_set)}")

    for index, (csv_row, json_row) in enumerate(zip(csv_rows, json_rows), start=1):
        provider = csv_row.get("provider_name", f"row {index}")
        if set(json_row) != csv_field_set:
            fail(f"{provider}: JSON field set differs from CSV")
        if csv_row != json_row:
            differences = [key for key in csv_field_set if csv_row.get(key, "") != json_row.get(key, "")]
            fail(f"{provider}: CSV/JSON mismatch in {differences}")

        if csv_row["normalization_state"] not in ALLOWED_NORMALIZATION:
            fail(f"{provider}: invalid normalization_state")
        if csv_row["commercial_rights_evidence_status"] not in ALLOWED_CRES:
            fail(f"{provider}: invalid CRES value")
        if csv_row["release_id"] != EXPECTED_CANDIDATE_ID:
            fail(f"{provider}: unexpected release_id")
        if not csv_row["checked_at"]:
            fail(f"{provider}: checked_at is required")

        unresolved = csv_row["reconciliation_status"] in {
            "pending_first_party_access",
            "first_party_pricing_conflict",
            "partial_verified",
            "needs_correction_or_change_event",
        }
        if unresolved and not csv_row["research_note"]:
            fail(f"{provider}: unresolved state requires an explicit research_note")

        if csv_row["reconciliation_status"] == "pending_first_party_access" and csv_row["advertised_price"]:
            fail(f"{provider}: pending current pricing must not carry a promoted current advertised_price")

        if csv_row["reconciliation_status"] == "first_party_pricing_conflict" and csv_row["normalization_state"] != "caution":
            fail(f"{provider}: first-party pricing conflict must remain caution")

    print(f"PASS: {EXPECTED_COUNT} providers; CSV/JSON parity exact; candidate remains HOLD")


if __name__ == "__main__":
    main()
