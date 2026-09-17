#!/usr/bin/env python3
"""Build a deterministic directory package for the HOLD research candidate.

This creates a local/CI build artifact only. It does not create a GitHub release,
tag, Zenodo deposit, DOI, or production deployment.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_ID = "RC-2026-09-17-HOLD"
BUILD_ROOT = ROOT / "build" / CANDIDATE_ID

PACKAGE_FILES = [
    "datasets/release-candidate-2026-09-17.csv",
    "datasets/release-candidate-2026-09-17.json",
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
    "CITATION.cff",
    "LICENSE_STATUS.md",
    "CHANGELOG.md",
    "RELEASE_STATUS.md",
    "release-candidate/release-manifest.json",
    "release-candidate/RELEASE_PLAYBOOK.md",
    "release-candidate/ZENODO_DEPOSIT_FIELDS.md",
    ".zenodo.json.template",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if BUILD_ROOT.exists():
        shutil.rmtree(BUILD_ROOT)
    BUILD_ROOT.mkdir(parents=True)

    missing = [rel for rel in PACKAGE_FILES if not (ROOT / rel).is_file()]
    if missing:
        raise SystemExit(f"FAIL: required candidate package files missing: {missing}")

    records: list[dict[str, object]] = []
    for rel in sorted(PACKAGE_FILES):
        source = ROOT / rel
        target = BUILD_ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        records.append(
            {
                "path": rel,
                "sha256": sha256(target),
                "size_bytes": target.stat().st_size,
            }
        )

    manifest = {
        "package_type": "hold_candidate_research_package",
        "candidate_id": CANDIDATE_ID,
        "publication_authorized": False,
        "doi": None,
        "production_baseline": "V70.7.5",
        "production_modified": False,
        "file_count": len(records),
        "files": records,
    }
    manifest_path = BUILD_ROOT / "PACKAGE_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    checksum_lines = [f"{record['sha256']}  {record['path']}" for record in records]
    checksum_lines.append(f"{sha256(manifest_path)}  PACKAGE_MANIFEST.json")
    (BUILD_ROOT / "SHA256SUMS.txt").write_text(
        "\n".join(checksum_lines) + "\n",
        encoding="utf-8",
    )

    print(
        f"PASS: built {CANDIDATE_ID} package with {len(records)} source files, "
        "PACKAGE_MANIFEST.json and SHA256SUMS.txt; publication remains unauthorized."
    )


if __name__ == "__main__":
    main()
