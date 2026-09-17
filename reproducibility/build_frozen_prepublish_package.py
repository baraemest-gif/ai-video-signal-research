#!/usr/bin/env python3
"""Build the frozen pre-publication package for AI Video Signal v2026.09.17.

The resulting package is versioned and checksum-stable for a specific source
commit, but publication remains unauthorized. No DOI is invented and no active
Zenodo metadata is created.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v2026.09.17"
FREEZE_DATE = "2026-09-17"
OUT = ROOT / "build" / VERSION
SOURCE_CSV = ROOT / "datasets" / "release-candidate-2026-09-17.csv"
SOURCE_JSON = ROOT / "datasets" / "release-candidate-2026-09-17.json"

COPY_FILES = [
    "datasets/data-dictionary.md",
    "methodology/methodology.md",
    "evidence/source-manifest.csv",
    "evidence/relationship-disclosure-manifest.csv",
    "reconciliation/provider-reconciliation-2026-09-17.csv",
    "reconciliation/provider-reconciliation-2026-09-17.json",
    "reconciliation/provider-reconciliation-2026-09-17.md",
    "reports/release-candidate-summary-2026-09-17.md",
    "reproducibility/README.md",
    "reproducibility/validate_reconciliation.py",
    "reproducibility/validate_release_candidate.py",
    "reproducibility/validate_evidence_and_disclosures.py",
    "reproducibility/validate_quantitative_coverage.py",
    "reproducibility/validate_metadata.py",
    "reproducibility/validate_freeze_readiness.py",
    "reproducibility/validate_release_guard.py",
    "reproducibility/derive_release_candidate_metrics.py",
    "reproducibility/build_candidate_package.py",
    "reproducibility/validate_candidate_package.py",
    "reproducibility/build_frozen_prepublish_package.py",
    "reproducibility/validate_frozen_prepublish_package.py",
    "release-candidate/FREEZE_READINESS.md",
    "release-candidate/RELEASE_PLAYBOOK.md",
    "release-candidate/ZENODO_DEPOSIT_FIELDS.md",
    "CHANGELOG.md",
]

RIGHTS_TEXT = """# AI Video Signal — Dataset Rights & Reuse\n\nEffective public terms: 2026-08-31\nCanonical terms: https://aivideosignal.com/dataset-license/\n\n© 2026 AI Video Signal. Citation and limited excerpts are permitted for journalism, research, analysis, reviews and editorial work with attribution to AI Video Signal, the relevant checked date when applicable, and a link to the dataset or benchmark page where practical.\n\nRepublishing complete files, mirroring them, selling them, incorporating substantial portions into a competing commercial dataset, or removing source attribution requires prior written permission.\n\nUnderlying third-party facts remain subject to the relevant providers' rights and terms. AI Video Signal copyright applies to its original selection, normalization, structure, commentary and compilation.\n\nDatasets are dated research snapshots provided for informational purposes. Provider pricing, credits, features and legal terms can change. Verify current provider documentation before purchasing or making legal/commercial decisions.\n\nPermission requests: partners@aivideosignal.com\n\nThis is a custom rights statement. The package does not assert CC BY, CC0, MIT or another broader standard license.\n"""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(rows: list[dict[str, str]], fieldnames: list[str], path: Path) -> None:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    path.write_text(buffer.getvalue(), encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    with SOURCE_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if len(rows) != 14:
        raise SystemExit("FAIL: expected 14 source provider rows")

    frozen_rows: list[dict[str, str]] = []
    for row in rows:
        frozen = dict(row)
        frozen["release_id"] = VERSION
        frozen["record_version"] = "1.0"
        frozen_rows.append(frozen)

    write_csv(frozen_rows, fieldnames, OUT / "provider-dataset.csv")

    source_payload = json.loads(SOURCE_JSON.read_text(encoding="utf-8"))
    source_by_name = {r["provider_name"]: r for r in source_payload.get("records", [])}
    if set(source_by_name) != {r["provider_name"] for r in frozen_rows}:
        raise SystemExit("FAIL: source candidate CSV/JSON provider sets differ")

    frozen_json_rows: list[dict[str, str]] = []
    for frozen in frozen_rows:
        source = dict(source_by_name[frozen["provider_name"]])
        source["release_id"] = VERSION
        source["record_version"] = "1.0"
        frozen_json_rows.append(source)

    frozen_payload = {
        "document_type": "provider_dataset_release",
        "project": "AI Video Signal",
        "status": "FROZEN_PRE_PUBLISH",
        "version": VERSION,
        "freeze_date": FREEZE_DATE,
        "publication_date": None,
        "publication_authorized": False,
        "doi": None,
        "record_count": 14,
        "records": frozen_json_rows,
    }
    (OUT / "provider-dataset.json").write_text(
        json.dumps(frozen_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for rel in COPY_FILES:
        source = ROOT / rel
        if not source.is_file():
            raise SystemExit(f"FAIL: frozen package source file missing: {rel}")
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8").rstrip() + "\n"
    forbidden = ("\nversion:", "\ndate-released:", "\ndoi:")
    if any(token in cff.lower() for token in forbidden):
        raise SystemExit("FAIL: source CITATION.cff unexpectedly contains final-release metadata")
    cff += f'version: "{VERSION}"\n'
    (OUT / "CITATION.cff").write_text(cff, encoding="utf-8")

    (OUT / "RIGHTS.md").write_text(RIGHTS_TEXT, encoding="utf-8")

    source_commit = os.environ.get("GITHUB_SHA") or None
    package_files = [p for p in OUT.rglob("*") if p.is_file()]
    records = []
    for path in sorted(package_files, key=lambda p: p.relative_to(OUT).as_posix()):
        rel = path.relative_to(OUT).as_posix()
        records.append({"path": rel, "sha256": sha256(path), "size_bytes": path.stat().st_size})

    manifest = {
        "package_type": "frozen_prepublish_research_release",
        "project": "AI Video Signal",
        "version": VERSION,
        "freeze_date": FREEZE_DATE,
        "publication_date": None,
        "publication_authorized": False,
        "doi": None,
        "orcid": None,
        "production_baseline": "V70.7.5",
        "production_modified": False,
        "source_commit_sha": source_commit,
        "provider_count": 14,
        "rights_mode": "custom_ai_video_signal_terms",
        "rights_url": "https://aivideosignal.com/dataset-license/",
        "file_count": len(records),
        "files": records,
    }
    manifest_path = OUT / "RELEASE_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checksum_records = records + [
        {
            "path": "RELEASE_MANIFEST.json",
            "sha256": sha256(manifest_path),
            "size_bytes": manifest_path.stat().st_size,
        }
    ]
    lines = [f"{record['sha256']}  {record['path']}" for record in checksum_records]
    (OUT / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"PASS: built frozen pre-publication package {VERSION} from 14 providers; "
        f"{len(checksum_records)} checksummed files; publication_authorized=false; DOI=null."
    )


if __name__ == "__main__":
    main()
