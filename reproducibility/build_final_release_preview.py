#!/usr/bin/env python3
"""Build versioned final-release preview distributions from the validated HOLD candidate.

The preview is generated from the reconciled candidate state and is deliberately
non-published. It creates release-named CSV/JSON plus manifest/checksums under
build/release-preview. It does not create a tag, GitHub Release, Zenodo record or DOI.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil

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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    with SOURCE_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise SystemExit("FAIL: candidate CSV has no header")
        rows = list(reader)

    if len(rows) != 14:
        raise SystemExit(f"FAIL: expected 14 candidate rows, found {len(rows)}")

    release_rows = []
    for source in rows:
        row = dict(source)
        row["release_id"] = VERSION
        row["record_version"] = "1.0"
        release_rows.append(row)

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(release_rows)

    source_payload = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    if source_payload.get("record_count") != 14:
        raise SystemExit("FAIL: candidate JSON record_count is not 14")

    json_rows = []
    for source in source_payload.get("records", []):
        row = dict(source)
        row["release_id"] = VERSION
        row["record_version"] = "1.0"
        json_rows.append(row)

    payload = {
        "document_type": "provider_dataset_release_preview",
        "project": "AI Video Signal",
        "status": "FROZEN_PREPUBLICATION_HOLD",
        "publication_authorized": False,
        "version": VERSION,
        "publication_date": None,
        "doi": None,
        "orcid": None,
        "source_candidate_id": source_payload.get("candidate_id"),
        "source_freeze_commit": FREEZE_COMMIT,
        "checked_at": source_payload.get("checked_at"),
        "record_count": 14,
        "records": json_rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "package_type": "final_release_preview",
        "project": "AI Video Signal",
        "version": VERSION,
        "status": "FROZEN_PREPUBLICATION_HOLD",
        "publication_authorized": False,
        "doi": None,
        "source_freeze_commit": FREEZE_COMMIT,
        "production_baseline": "V70.7.5",
        "production_modified": False,
        "files": [
            {"path": "provider-dataset.csv", "sha256": sha256(OUT_CSV), "size_bytes": OUT_CSV.stat().st_size},
            {"path": "provider-dataset.json", "sha256": sha256(OUT_JSON), "size_bytes": OUT_JSON.stat().st_size},
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"{sha256(OUT_CSV)}  provider-dataset.csv",
        f"{sha256(OUT_JSON)}  provider-dataset.json",
        f"{sha256(MANIFEST)}  RELEASE_PREVIEW_MANIFEST.json",
    ]
    CHECKSUMS.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"PASS: built {VERSION} final release preview with 14 provider rows; "
        "publication remains HOLD and DOI is null."
    )


if __name__ == "__main__":
    main()
