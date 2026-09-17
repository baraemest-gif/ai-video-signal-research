#!/usr/bin/env python3
"""Validate source coverage for material quantitative fields in the HOLD candidate.

This validator does not decide whether a provider is globally comparable. It only
checks that any material quantitative value promoted in the candidate is traceable
to evidence, date-scoped, and not presented as a derived metric without inputs.
"""

from __future__ import annotations

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "datasets" / "release-candidate-2026-09-17.csv"
SOURCE_MANIFEST = ROOT / "evidence" / "source-manifest.csv"
EXPECTED_COUNT = 14

MATERIAL_FIELDS = (
    "advertised_price",
    "credits_or_allowance",
    "nominal_generation_cost",
    "approved_output_cost",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def nonblank(value: str | None) -> bool:
    return bool((value or "").strip())


def main() -> None:
    candidate = read_csv(CANDIDATE)
    sources = read_csv(SOURCE_MANIFEST)

    if len(candidate) != EXPECTED_COUNT:
        fail(f"candidate must contain {EXPECTED_COUNT} providers")

    source_urls = {
        row.get("source_url", "").strip()
        for row in sources
        if row.get("source_url", "").strip()
    }

    promoted_fields = 0
    numeric_price_rows = 0

    for row in candidate:
        provider = row.get("provider_name", "<unknown>")
        source_url = row.get("source_url", "").strip()
        evidence_tier = row.get("evidence_tier", "").strip()
        checked_at = row.get("checked_at", "").strip()

        material_present = [field for field in MATERIAL_FIELDS if nonblank(row.get(field))]
        promoted_fields += len(material_present)

        if material_present:
            if not source_url:
                fail(f"{provider}: material quantitative fields {material_present} require source_url")
            if source_url not in source_urls:
                fail(f"{provider}: quantitative source_url is absent from source manifest: {source_url}")
            if not evidence_tier:
                fail(f"{provider}: material quantitative fields require evidence_tier")
            if not checked_at:
                fail(f"{provider}: material quantitative fields require checked_at")

        price = row.get("advertised_price", "").strip()
        if price:
            try:
                Decimal(price)
            except InvalidOperation:
                fail(f"{provider}: advertised_price must be numeric when populated: {price!r}")
            numeric_price_rows += 1
            if not row.get("currency", "").strip():
                fail(f"{provider}: advertised_price requires currency")
            if not row.get("billing_interval", "").strip():
                fail(f"{provider}: advertised_price requires billing_interval")

        aoc = row.get("approved_output_cost", "").strip()
        if aoc:
            if not row.get("nominal_generation_cost", "").strip():
                fail(f"{provider}: approved_output_cost requires nominal_generation_cost")
            if not row.get("retry_assumption", "").strip():
                fail(f"{provider}: approved_output_cost requires retry_assumption or measured retry input")
            note = row.get("research_note", "").lower()
            if not any(token in note for token in ("derived", "assumption", "observed", "scenario")):
                fail(f"{provider}: approved_output_cost requires derivation/assumption status in research_note")

        if row.get("normalization_state") == "normalized" and price:
            # Current cross-provider paid-price summary is explicitly USD-only.
            if row.get("currency") != "USD":
                fail(
                    f"{provider}: normalized numeric paid price must be USD in the current candidate; "
                    "region/currency-scoped prices must remain not_normalized"
                )

    if promoted_fields == 0:
        fail("candidate contains no material quantitative fields to validate")

    print(
        f"PASS: {EXPECTED_COUNT} providers; {promoted_fields} populated material quantitative fields "
        f"and {numeric_price_rows} numeric paid-price rows are evidence/date scoped."
    )


if __name__ == "__main__":
    main()
