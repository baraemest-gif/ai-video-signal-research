#!/usr/bin/env python3
"""Validate the frozen v2026.09.17 pre-publication package.

This validator confirms release-file parity, versioning, checksums and safety
state. A PASS is not publication authorization.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v2026.09.17"
OUT = ROOT / "build" / VERSION
CSV_PATH = OUT / "provider-dataset.csv"
JSON_PATH = OUT / "provider-dataset.json"
MANIFEST_PATH = OUT / "RELEASE_MANIFEST.json"
CHECKSUMS_PATH = OUT / "SHA256SUMS.txt"
EXPECTED_COUNT = 14


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized(record: dict[str, object]) -> dict[str, str]:
    return {key: "" if value is None else str(value) for key, value in record.items()}


def main() -> None:
    for path in (CSV_PATH, JSON_PATH, MANIFEST_PATH, CHECKSUMS_PATH):
        if not path.is_file():
            fail(f"missing frozen package file: {path.relative_to(ROOT)}")

    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        csv_rows = [normalized(row) for row in csv.DictReader(handle)]
    payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    json_rows = [normalized(row) for row in payload.get("records", [])]

    if len(csv_rows) != EXPECTED_COUNT or len(json_rows) != EXPECTED_COUNT:
        fail("frozen dataset must contain exactly 14 providers in both formats")
    if payload.get("record_count") != EXPECTED_COUNT:
        fail("frozen JSON record_count mismatch")
    if payload.get("status") != "FROZEN_PRE_PUBLISH":
        fail("frozen JSON must remain FROZEN_PRE_PUBLISH")
    if payload.get("version") != VERSION:
        fail("frozen JSON version mismatch")
    if payload.get("publication_authorized") is not False:
        fail("frozen JSON must not authorize publication")
    if payload.get("doi") is not None:
        fail("frozen JSON DOI must remain null before Zenodo assignment")

    csv_names = [row.get("provider_name", "") for row in csv_rows]
    json_names = [row.get("provider_name", "") for row in json_rows]
    if csv_names != json_names or len(set(csv_names)) != EXPECTED_COUNT:
        fail("frozen CSV/JSON provider identity/order mismatch")

    fields = set(csv_rows[0])
    for csv_row, json_row in zip(csv_rows, json_rows):
        provider = csv_row.get("provider_name", "<unknown>")
        if set(json_row) != fields:
            fail(f"{provider}: frozen JSON field set differs from CSV")
        if csv_row != json_row:
            differences = sorted(key for key in fields if csv_row.get(key) != json_row.get(key))
            fail(f"{provider}: frozen CSV/JSON mismatch in {differences}")
        if csv_row.get("release_id") != VERSION:
            fail(f"{provider}: frozen release_id must be {VERSION}")
        if csv_row.get("record_version") != "1.0":
            fail(f"{provider}: frozen record_version must be 1.0")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION:
        fail("release manifest version mismatch")
    if manifest.get("provider_count") != EXPECTED_COUNT:
        fail("release manifest provider_count mismatch")
    if manifest.get("publication_authorized") is not False:
        fail("release manifest must not authorize publication")
    if manifest.get("publication_date") is not None:
        fail("publication_date must remain null before publication")
    if manifest.get("doi") is not None:
        fail("release manifest DOI must remain null")
    if manifest.get("orcid") is not None:
        fail("release manifest ORCID must remain null unless explicitly supplied and verified")
    if manifest.get("production_baseline") != "V70.7.5" or manifest.get("production_modified") is not False:
        fail("Production firewall state mismatch")

    records = manifest.get("files", [])
    if manifest.get("file_count") != len(records) or not records:
        fail("release manifest file_count mismatch")

    expected_lines: list[str] = []
    seen: set[str] = set()
    for record in records:
        rel = record.get("path", "")
        if not rel or rel in seen:
            fail(f"invalid/duplicate release package path: {rel!r}")
        seen.add(rel)
        path = OUT / rel
        if not path.is_file():
            fail(f"manifested release file missing: {rel}")
        actual = sha256(path)
        if actual != record.get("sha256"):
            fail(f"SHA-256 mismatch: {rel}")
        if path.stat().st_size != record.get("size_bytes"):
            fail(f"size mismatch: {rel}")
        expected_lines.append(f"{actual}  {rel}")

    expected_lines.append(f"{sha256(MANIFEST_PATH)}  RELEASE_MANIFEST.json")
    actual_lines = [line for line in CHECKSUMS_PATH.read_text(encoding="utf-8").splitlines() if line]
    if actual_lines != expected_lines:
        fail("SHA256SUMS.txt does not exactly match the frozen manifest/files")

    cff = (OUT / "CITATION.cff").read_text(encoding="utf-8")
    if f'version: "{VERSION}"' not in cff:
        fail("frozen CITATION.cff does not carry the frozen version")
    for forbidden in ("doi:", "date-released:"):
        if any(line.strip().lower().startswith(forbidden) for line in cff.splitlines()):
            fail(f"frozen pre-publication CITATION.cff must not yet contain {forbidden}")

    if (OUT / ".zenodo.json").exists():
        fail("frozen pre-publication package must not activate .zenodo.json")

    print(
        f"PASS: frozen pre-publication package {VERSION}; 14-provider CSV/JSON parity exact; "
        f"{len(records) + 1} SHA-256 entries verified; publication remains unauthorized."
    )


if __name__ == "__main__":
    main()
