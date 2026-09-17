#!/usr/bin/env python3
"""Validate versioned final-release preview distributions against the HOLD candidate."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v2026.09.17"
FREEZE_COMMIT = "820b41e06bfdd8f861e1177eef10c6c6160ebecd"
SOURCE_CSV = ROOT / "datasets" / "release-candidate-2026-09-17.csv"
SOURCE_JSON = ROOT / "datasets" / "release-candidate-2026-09-17.json"
OUT = ROOT / "build" / "release-preview" / VERSION
OUT_CSV = OUT / "provider-dataset.csv"
OUT_JSON = OUT / "provider-dataset.json"
MANIFEST = OUT / "RELEASE_PREVIEW_MANIFEST.json"
CHECKSUMS = OUT / "SHA256SUMS.txt"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    source_rows = read_csv(SOURCE_CSV)
    release_rows = read_csv(OUT_CSV)
    if len(source_rows) != 14 or len(release_rows) != 14:
        fail("source and preview CSV must each contain exactly 14 providers")

    source_by_name = {r["provider_name"]: r for r in source_rows}
    release_by_name = {r["provider_name"]: r for r in release_rows}
    if set(source_by_name) != set(release_by_name):
        fail("provider identity set differs between candidate and release preview")

    allowed_metadata_differences = {"release_id", "record_version"}
    for provider, source in source_by_name.items():
        release = release_by_name[provider]
        if release.get("release_id") != VERSION:
            fail(f"{provider}: release_id is not {VERSION}")
        if release.get("record_version") != "1.0":
            fail(f"{provider}: record_version is not 1.0")
        for field, value in source.items():
            if field in allowed_metadata_differences:
                continue
            if release.get(field) != value:
                fail(f"{provider}: material field changed during final-preview build: {field}")

    source_payload = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    release_payload = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    if release_payload.get("status") != "FROZEN_PREPUBLICATION_HOLD":
        fail("release preview JSON status must remain FROZEN_PREPUBLICATION_HOLD")
    if release_payload.get("publication_authorized") is not False:
        fail("release preview publication_authorized must remain false")
    if release_payload.get("version") != VERSION:
        fail("release preview version mismatch")
    if release_payload.get("publication_date") is not None:
        fail("publication_date must remain null until actual release date is approved")
    if release_payload.get("doi") is not None:
        fail("DOI must remain null until Zenodo assigns it")
    if release_payload.get("orcid") is not None:
        fail("ORCID must remain null unless explicitly supplied and verified")
    if release_payload.get("source_freeze_commit") != FREEZE_COMMIT:
        fail("release preview source freeze commit mismatch")
    if release_payload.get("record_count") != 14 or len(release_payload.get("records", [])) != 14:
        fail("release preview JSON must contain exactly 14 records")

    json_by_name = {r["provider_name"]: r for r in release_payload["records"]}
    if set(json_by_name) != set(release_by_name):
        fail("CSV/JSON provider sets differ in final release preview")
    for provider, csv_row in release_by_name.items():
        json_row = json_by_name[provider]
        for field, csv_value in csv_row.items():
            json_value = json_row.get(field, "")
            if str(json_value) != csv_value:
                fail(f"{provider}: final preview CSV/JSON mismatch in {field}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION:
        fail("release preview manifest version mismatch")
    if manifest.get("publication_authorized") is not False or manifest.get("doi") is not None:
        fail("release preview manifest must remain unpublished and DOI-free")
    if manifest.get("source_freeze_commit") != FREEZE_COMMIT:
        fail("release preview manifest source freeze commit mismatch")
    if manifest.get("production_baseline") != "V70.7.5" or manifest.get("production_modified") is not False:
        fail("release preview manifest violates production firewall")

    expected = [
        f"{sha256(OUT_CSV)}  provider-dataset.csv",
        f"{sha256(OUT_JSON)}  provider-dataset.json",
        f"{sha256(MANIFEST)}  RELEASE_PREVIEW_MANIFEST.json",
    ]
    actual = [line for line in CHECKSUMS.read_text(encoding="utf-8").splitlines() if line]
    if actual != expected:
        fail("final release preview SHA256SUMS mismatch")

    print(
        f"PASS: {VERSION} release preview preserves all candidate material fields, "
        "has exact CSV/JSON parity and verified SHA-256 checksums; publication remains HOLD."
    )


if __name__ == "__main__":
    main()
