#!/usr/bin/env python3
"""Validate parity of the dated provider-reconciliation CSV and JSON files.

Standard-library only. Exits non-zero on any mismatch.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "reconciliation" / "provider-reconciliation-2026-09-17.csv"
JSON_PATH = ROOT / "reconciliation" / "provider-reconciliation-2026-09-17.json"
EXPECTED_PROVIDER_COUNT = 14
COMPARE_FIELDS = (
    "provider",
    "status",
    "baseline_reference",
    "current_evidence_summary",
    "release_action",
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    with CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))

    with JSON_PATH.open("r", encoding="utf-8") as handle:
        json_doc = json.load(handle)

    json_rows = json_doc.get("providers")
    if not isinstance(json_rows, list):
        fail("JSON 'providers' must be a list")

    if len(csv_rows) != EXPECTED_PROVIDER_COUNT:
        fail(f"CSV provider count is {len(csv_rows)}, expected {EXPECTED_PROVIDER_COUNT}")
    if len(json_rows) != EXPECTED_PROVIDER_COUNT:
        fail(f"JSON provider count is {len(json_rows)}, expected {EXPECTED_PROVIDER_COUNT}")

    baseline_date = json_doc.get("baseline_date")
    current_check_date = json_doc.get("current_check_date")
    if not baseline_date or not current_check_date:
        fail("JSON must define baseline_date and current_check_date")

    csv_by_provider = {}
    for row in csv_rows:
        provider = row.get("provider", "").strip()
        if not provider:
            fail("CSV contains a blank provider")
        if provider in csv_by_provider:
            fail(f"Duplicate CSV provider: {provider}")
        if row.get("baseline_date") != baseline_date:
            fail(f"CSV baseline_date mismatch for {provider}")
        if row.get("current_check_date") != current_check_date:
            fail(f"CSV current_check_date mismatch for {provider}")
        csv_by_provider[provider] = row

    json_by_provider = {}
    for row in json_rows:
        provider = str(row.get("provider", "")).strip()
        if not provider:
            fail("JSON contains a blank provider")
        if provider in json_by_provider:
            fail(f"Duplicate JSON provider: {provider}")
        json_by_provider[provider] = row

    if set(csv_by_provider) != set(json_by_provider):
        only_csv = sorted(set(csv_by_provider) - set(json_by_provider))
        only_json = sorted(set(json_by_provider) - set(csv_by_provider))
        fail(f"Provider sets differ. only_csv={only_csv}; only_json={only_json}")

    for provider in sorted(csv_by_provider):
        csv_row = csv_by_provider[provider]
        json_row = json_by_provider[provider]
        for field in COMPARE_FIELDS:
            csv_value = str(csv_row.get(field, "")).strip()
            json_value = str(json_row.get(field, "")).strip()
            if not csv_value:
                fail(f"Blank CSV {field} for {provider}")
            if not json_value:
                fail(f"Blank JSON {field} for {provider}")
            if csv_value != json_value:
                fail(
                    f"Mismatch for {provider}.{field}: "
                    f"CSV={csv_value!r} JSON={json_value!r}"
                )

    if json_doc.get("release_status") != "HOLD":
        fail("Reconciliation JSON must remain HOLD before the release gates pass")

    print(
        f"PASS: {EXPECTED_PROVIDER_COUNT} providers; CSV/JSON reconciliation parity verified "
        f"for {current_check_date}."
    )


if __name__ == "__main__":
    main()
