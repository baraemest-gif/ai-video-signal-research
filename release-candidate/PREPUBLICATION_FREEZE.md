# AI Video Signal — Prepublication Freeze

Status: **HOLD — PREPUBLICATION FREEZE**

Freeze date: **2026-09-17**

This file records the validated prepublication freeze chain. It does **not** authorize publication, create a DOI, activate Zenodo metadata, create a GitHub Release, or modify Production.

## 1. Authoritative data freeze

Branch:
`prepublication-freeze-2026-09-17`

Exact commit SHA:
`820b41e06bfdd8f861e1177eef10c6c6160ebecd`

GitHub Actions run:
`35227905797`

CI conclusion:
**success**

The data freeze fixes the reconciled provider state and research evidence. It is the authoritative source state from which the prepublication package lineage begins.

## 2. Authoritative package freeze

Branch:
`package-freeze-v2026.09.17-prepublish`

Exact commit SHA:
`129273d47bde297de7ae4024ba8d07eaf3a00265`

GitHub Actions run:
`35228530529`

CI conclusion:
**success**

This package-freeze commit is the authoritative build state for the `v2026.09.17` prepublication artifact. It contains the validated package builder/validator state derived from the frozen research data while publication remains disabled.

## 3. Authoritative prepublication artifact for Zenodo review

GitHub Actions artifact ID:
`10500370413`

Artifact name:
`AI-Video-Signal-v2026.09.17-PREPUBLISH-129273d47bde297de7ae4024ba8d07eaf3a00265`

Artifact size:
`55,535 bytes`

GitHub artifact digest:
`sha256:5e14ea9f7a7845206bae936b5426413eeb77d623f6c9b1b3776ca40eb52e381f`

Artifact expiry:
`2026-12-16T13:40:11Z`

The artifact was created by CI on the exact package-freeze SHA after the frozen package builder and validator completed successfully.

**This is the artifact to use for the authenticated Zenodo draft/review unless a new package freeze is explicitly declared, validated, and recorded.**

## 4. Supporting HOLD artifact from the same package-freeze run

Artifact ID:
`10499694738`

Name:
`AI-Video-Signal-RC-2026-09-17-HOLD`

Digest:
`sha256:3f41c9a1cd6e6170a2f9772cf857d0a5d258589d0547e70d901bba5380a6e3fc`

This supporting artifact is retained for candidate reproducibility. It is not the versioned Zenodo deposit candidate.

## 5. Historical artifact lineage

An earlier artifact built directly from data-freeze SHA `820b41e...` remains valid evidence of reproducibility, but it is superseded as the deposit candidate by the explicitly declared package-freeze chain above.

Do not use arbitrary later `main` artifacts as a DOI deposit unless they become a new explicit package freeze with their own branch, SHA, successful CI run and recorded digest.

## What the frozen package contains

- 14-provider CSV and JSON distributions;
- methodology and data dictionary;
- source and relationship-disclosure manifests;
- provider reconciliation records;
- quantitative evidence checks;
- reproducibility validators;
- versioned prepublication citation metadata;
- custom rights statement;
- deterministic package builder;
- machine-readable release manifest;
- SHA-256 checksum file;
- HOLD publication controls.

## Validation result

On the authoritative package-freeze state, CI passed the complete pipeline, including:

- provider reconciliation;
- CSV/JSON parity;
- evidence/source coverage;
- relationship-disclosure consistency;
- quantitative evidence coverage;
- citation and Zenodo pre-release metadata checks;
- freeze readiness;
- HOLD publication guard;
- metric derivation;
- HOLD package reconstruction and checksum verification;
- frozen `v2026.09.17` package build;
- frozen package validation and SHA-256 verification;
- artifact upload.

## Publication controls

While status remains HOLD:

- `publication_authorized` remains `false`;
- DOI remains `null`;
- ORCID remains `null` unless explicitly supplied and verified;
- active `.zenodo.json` does not exist;
- no GitHub Release is authorized;
- no Zenodo publication is authorized;
- Production baseline **V70.7.5 remains untouched**.

## Remaining external gate

The Zenodo new-deposit interface requires authentication. In the unauthenticated browser check, Zenodo presented sign-in options and did not expose the deposit form. No draft, upload, DOI reservation or publication was created.

Before publication, the verified custom AI Video Signal rights statement must be entered and previewed in an authenticated Zenodo draft. Publication authorization stays false until that preview and the remaining release checks pass.
