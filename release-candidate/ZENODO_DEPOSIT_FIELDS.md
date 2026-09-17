# Zenodo Deposit Fields — Pre-Publish Worksheet

Status: **HOLD — do not publish yet**

Use this worksheet only with the authoritative package-freeze artifact recorded in `PREPUBLICATION_FREEZE.md`. Provider reconciliation is complete; the remaining mandatory manual gate is authenticated Zenodo review.

## Authoritative package to review in Zenodo

Package-freeze branch:
`package-freeze-v2026.09.17-prepublish`

Package-freeze commit:
`129273d47bde297de7ae4024ba8d07eaf3a00265`

GitHub Actions run:
`35228530529`

Artifact ID:
`10500370413`

Artifact name:
`AI-Video-Signal-v2026.09.17-PREPUBLISH-129273d47bde297de7ae4024ba8d07eaf3a00265`

Artifact SHA-256 digest:
`sha256:5e14ea9f7a7845206bae936b5426413eeb77d623f6c9b1b3776ca40eb52e381f`

Do not substitute a later `main` artifact unless a new explicit package freeze is declared and validated.

## Record type

- Resource/upload type: **Dataset**

## Title

**AI Video Signal Research Dataset 2026**

## Creator

**Mestetef Ennaji, Youssef**

Do not add an ORCID unless a real ORCID has been supplied and verified.

## Publisher / project

**AI Video Signal**

## Description

Versioned AI-video market-intelligence research covering provider pricing, credits and allowances, plan entitlements, model-level production economics, free-access states, commercial-use evidence, relationship disclosures, source provenance and documented market changes. The release includes machine-readable provider data, methodology, evidence manifests and reproducibility material. Historical states are preserved rather than silently overwritten when providers change pricing or entitlements.

## Keywords

- ai video
- generative video
- pricing benchmark
- market intelligence
- reproducible research
- dataset
- production economics

## Related identifier

Repository:
`https://github.com/baraemest-gif/ai-video-signal-research`

Relationship:
`isSupplementTo`

## Version

Prepublication package version:
`v2026.09.17`

Do not create a public GitHub Release or Zenodo publication while status remains HOLD.

## Publication date

**DO NOT FINALIZE WHILE HOLD.**

Use the actual publication date only when publication is explicitly authorized.

## DOI

**DO NOT INVENT OR PRE-FILL.**

Record only a DOI actually reserved/assigned by Zenodo through the authenticated deposit workflow.

## License — mandatory high-risk check

Zenodo's current public documentation states that the **License field is required** and that Zenodo **defaults to Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Therefore:

1. Do **not** leave the default CC BY 4.0 selected.
2. Click/edit the License field in the authenticated draft.
3. Select/create the custom-license/custom-rights option supported by the current Zenodo interface.
4. Enter the AI Video Signal rights text below without broadening the rights.
5. Preview the saved draft and verify that **CC BY 4.0 is no longer asserted**.
6. If Zenodo cannot represent these rights accurately, STOP and keep the release on HOLD.

Canonical terms:
`https://aivideosignal.com/dataset-license/`

Effective date: **2026-08-31**.

### Custom rights statement

> © 2026 AI Video Signal. Citation and limited excerpts are permitted for journalism, research, analysis, reviews and editorial work with attribution to AI Video Signal, the relevant checked date when applicable, and a link to the dataset or benchmark page where practical. Republishing complete files, mirroring them, selling them, incorporating substantial portions into a competing commercial dataset, or removing source attribution requires prior written permission. Underlying third-party facts remain subject to the relevant providers' rights and terms. Datasets are dated research snapshots provided for informational purposes; provider pricing, credits, features and legal terms can change. Permission requests: partners@aivideosignal.com.

Do **not** silently substitute CC BY 4.0, CC0, MIT or another broader standard license.

## Access

The package may be publicly accessible only if the selected Zenodo access configuration can coexist accurately with the custom reuse restrictions above. Public accessibility is not itself permission for unrestricted redistribution.

## Files to deposit

Use the authoritative package-freeze artifact. It contains the versioned prepublication dataset and supporting research package, including:

- `provider-dataset.csv`
- `provider-dataset.json`
- methodology snapshot
- evidence/source manifest
- relationship-disclosure manifest
- changelog
- `CITATION.cff`
- `RIGHTS.md`
- reproducibility instructions and validators
- `RELEASE_MANIFEST.json`
- `SHA256SUMS.txt`

## Required checks before any Publish action

- authenticated Zenodo draft opened
- authoritative package-freeze artifact used
- dataset resource type selected
- title and creator exact
- version `v2026.09.17` exact
- publication date intentionally chosen
- repository related identifier correct
- default CC BY 4.0 explicitly removed/replaced
- custom AI Video Signal rights text visible in preview
- no unintended standard license displayed
- provider count 14
- CSV/JSON parity exact
- all quantitative fields sourced or clearly derived
- source manifest present
- relationship disclosures present
- SHA-256 files present
- DOI/ORCID not invented
- GitHub Actions green on the authoritative package-freeze commit
- `publication_authorized=false` until final explicit authorization
- Production V70.7.5 untouched

## Post-publication

Only after Zenodo actually publishes/assigns the DOI:

1. record the real DOI in citation metadata and the release manifest;
2. add the DOI to the canonical research page and structured Dataset metadata;
3. preserve the archived release unchanged;
4. record the DOI metadata update in the changelog;
5. begin external citation outreach using the immutable DOI-backed release.
