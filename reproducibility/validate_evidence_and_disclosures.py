#!/usr/bin/env python3
"""Validate evidence-manifest coverage and relationship-disclosure consistency."""

from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "datasets" / "release-candidate-2026-09-17.csv"
SOURCE_MANIFEST = ROOT / "evidence" / "source-manifest.csv"
REL_MANIFEST = ROOT / "evidence" / "relationship-disclosure-manifest.csv"
EXPECTED_COUNT = 14


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    candidate = read_csv(CANDIDATE)
    sources = read_csv(SOURCE_MANIFEST)
    relationships = read_csv(REL_MANIFEST)

    if len(candidate) != EXPECTED_COUNT:
        fail(f"candidate must contain {EXPECTED_COUNT} providers")
    if len(relationships) != EXPECTED_COUNT:
        fail(f"relationship manifest must contain {EXPECTED_COUNT} providers")

    candidate_names = [r["provider_name"] for r in candidate]
    relationship_names = [r["provider"] for r in relationships]

    if len(set(candidate_names)) != EXPECTED_COUNT:
        fail("candidate provider names are not unique")
    if len(set(relationship_names)) != EXPECTED_COUNT:
        fail("relationship provider names are not unique")
    if set(candidate_names) != set(relationship_names):
        fail("relationship manifest provider set differs from candidate")

    source_urls = {r.get("source_url", "").strip() for r in sources if r.get("source_url", "").strip()}
    for row in candidate:
        provider = row["provider_name"]
        url = row.get("source_url", "").strip()
        if url and url not in source_urls:
            fail(f"{provider}: candidate source_url missing from evidence/source-manifest.csv: {url}")

    rel_by_provider = {r["provider"]: r for r in relationships}
    for row in candidate:
        provider = row["provider_name"]
        disclosure = row.get("relationship_disclosure", "").strip()
        if not disclosure:
            fail(f"{provider}: relationship_disclosure is blank")

        manifest = rel_by_provider[provider]
        state = manifest.get("disclosure_state", "").strip()
        visibility = manifest.get("source_visibility", "").strip()

        if visibility != "private_evidence_not_published":
            fail(f"{provider}: unexpected relationship evidence visibility")

        manifest_confirmed = state.startswith("confirmed_")
        candidate_confirmed = disclosure.startswith("confirmed_")
        if manifest_confirmed != candidate_confirmed:
            fail(f"{provider}: confirmed/non-confirmed relationship state differs between candidate and manifest")

        if state == "no_relationship_evidenced" and not disclosure.startswith("no_affiliate_relationship_evidenced"):
            fail(f"{provider}: no-evidence relationship wording must stay explicitly evidence-scoped")

    print(
        f"PASS: {EXPECTED_COUNT} relationship disclosures consistent; "
        "all nonblank candidate source URLs covered by source manifest"
    )


if __name__ == "__main__":
    main()
