#!/usr/bin/env python3
"""Validate the locally built HOLD candidate package and SHA-256 manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_ID = "RC-2026-09-17-HOLD"
PACKAGE_ROOT = ROOT / "build" / CANDIDATE_ID
MANIFEST = PACKAGE_ROOT / "PACKAGE_MANIFEST.json"
CHECKSUMS = PACKAGE_ROOT / "SHA256SUMS.txt"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if not PACKAGE_ROOT.is_dir():
        fail("candidate package has not been built")
    if not MANIFEST.is_file() or not CHECKSUMS.is_file():
        fail("PACKAGE_MANIFEST.json or SHA256SUMS.txt missing")

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if payload.get("candidate_id") != CANDIDATE_ID:
        fail("candidate package id mismatch")
    if payload.get("publication_authorized") is not False:
        fail("candidate package must not authorize publication")
    if payload.get("doi") is not None:
        fail("candidate package must not assert a DOI")
    if payload.get("production_baseline") != "V70.7.5":
        fail("production baseline mismatch")
    if payload.get("production_modified") is not False:
        fail("candidate package must confirm Production is untouched")

    records = payload.get("files", [])
    if payload.get("file_count") != len(records) or not records:
        fail("package manifest file_count mismatch")

    expected_checksum_lines: list[str] = []
    seen: set[str] = set()
    for record in records:
        rel = record.get("path", "")
        if not rel or rel in seen:
            fail(f"invalid or duplicate package path: {rel!r}")
        seen.add(rel)
        path = PACKAGE_ROOT / rel
        if not path.is_file():
            fail(f"packaged file missing: {rel}")
        actual_hash = sha256(path)
        if actual_hash != record.get("sha256"):
            fail(f"SHA-256 mismatch: {rel}")
        if path.stat().st_size != record.get("size_bytes"):
            fail(f"size mismatch: {rel}")
        expected_checksum_lines.append(f"{actual_hash}  {rel}")

    expected_checksum_lines.append(f"{sha256(MANIFEST)}  PACKAGE_MANIFEST.json")
    actual_lines = [line for line in CHECKSUMS.read_text(encoding="utf-8").splitlines() if line]
    if actual_lines != expected_checksum_lines:
        fail("SHA256SUMS.txt differs from the package manifest/file hashes")

    print(
        f"PASS: {len(records)} packaged source files plus manifest verified by SHA-256; "
        "candidate remains HOLD and unpublished."
    )


if __name__ == "__main__":
    main()
