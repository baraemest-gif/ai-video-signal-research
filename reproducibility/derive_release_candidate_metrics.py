#!/usr/bin/env python3
"""Derive transparent descriptive metrics from the HOLD release candidate.

This script computes only metrics supported by explicit normalized candidate
fields. It intentionally excludes caution, unavailable and not_normalized paid
prices from the paid-price benchmark, and it does not infer free-entry or
commercial-rights counts from ambiguous text.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "datasets" / "release-candidate-2026-09-17.csv"


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rows = load_rows()

    normalized_paid = []
    for row in rows:
        price = row.get("advertised_price", "").strip()
        if row.get("normalization_state") == "normalized" and price:
            try:
                normalized_paid.append(float(price))
            except ValueError:
                pass

    status_counts: dict[str, int] = {}
    normalization_counts: dict[str, int] = {}
    cres_counts: dict[str, int] = {}

    for row in rows:
        for field, bucket in [
            ("reconciliation_status", status_counts),
            ("normalization_state", normalization_counts),
            ("commercial_rights_evidence_status", cres_counts),
        ]:
            value = row.get(field, "") or "blank"
            bucket[value] = bucket.get(value, 0) + 1

    metrics = {
        "candidate_id": rows[0]["release_id"] if rows else None,
        "status": "HOLD",
        "provider_count": len(rows),
        "normalized_paid_reference_count": len(normalized_paid),
        "normalized_paid_reference_median_usd": median(normalized_paid) if normalized_paid else None,
        "normalized_paid_reference_min_usd": min(normalized_paid) if normalized_paid else None,
        "normalized_paid_reference_max_usd": max(normalized_paid) if normalized_paid else None,
        "reconciliation_status_counts": dict(sorted(status_counts.items())),
        "normalization_state_counts": dict(sorted(normalization_counts.items())),
        "cres_counts": dict(sorted(cres_counts.items())),
        "method_note": (
            "Paid-price statistics include only rows with normalization_state=normalized "
            "and a non-empty numeric advertised_price. They exclude caution, unavailable "
            "and not_normalized states. No free-entry count is derived because unresolved "
            "or differently scoped free-access states remain in the candidate."
        ),
    }

    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
