# Zenodo Deposit Fields — Pre-Publish Worksheet

Status: **HOLD — do not publish yet**

Use this worksheet only after Kling AI and Hailuo AI are closed or explicitly represented in the final release state and every release gate is green.

## Record type

- Upload type: **Dataset**

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

**DO NOT FILL WHILE HOLD**

Final format:
`vYYYY.MM.DD`

Use only the version attached to the frozen immutable GitHub release.

## Publication date

**DO NOT FILL WHILE HOLD**

Use the actual publication date of the immutable release.

## DOI

**DO NOT INVENT OR PRE-FILL.**

Record only the DOI actually assigned by Zenodo after publication.

## Access and rights

Canonical terms:
`https://aivideosignal.com/dataset-license/`

Effective date of current public terms: **2026-08-31**.

### Custom rights statement

> © 2026 AI Video Signal. Citation and limited excerpts are permitted for journalism, research, analysis, reviews and editorial work with attribution to AI Video Signal, the relevant checked date when applicable, and a link to the dataset or benchmark page where practical. Republishing complete files, mirroring them, selling them, incorporating substantial portions into a competing commercial dataset, or removing source attribution requires prior written permission. Underlying third-party facts remain subject to the relevant providers' rights and terms. Datasets are dated research snapshots provided for informational purposes; provider pricing, credits, features and legal terms can change. Permission requests: partners@aivideosignal.com.

### Rule

Do **not** silently accept CC BY 4.0, CC0, MIT or another broader standard license if it contradicts the canonical AI Video Signal terms.

If Zenodo's current deposit interface cannot represent the custom rights position accurately, stop before publication and keep the release on HOLD.

## Files to deposit

Minimum frozen package:

- final provider dataset CSV
- final provider dataset JSON
- methodology snapshot
- evidence/source manifest
- relationship-disclosure manifest
- CHANGELOG
- CITATION.cff
- rights/usage statement
- reproducibility instructions and validators
- release manifest
- checksums

## Required final checks before Publish

- final provider count reconciled
- CSV/JSON exact parity
- Kling state closed or explicitly represented
- Hailuo state closed or explicitly represented
- all quantitative fields sourced or clearly derived
- source manifest complete
- relationship disclosures current
- final derived metrics reproducible
- final version and date consistent everywhere
- custom rights statement previewed correctly
- no invented DOI or ORCID
- GitHub Actions green on the frozen commit
- Production V70.7.5 untouched

## Post-publication

After Zenodo assigns the DOI:

1. record the real DOI in citation metadata and the release manifest;
2. add the DOI to the canonical research page and structured Dataset metadata;
3. preserve the archived release unchanged;
4. record the DOI metadata update in the changelog;
5. begin external citation outreach using the immutable DOI-backed release.
