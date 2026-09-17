# AI Video Signal — Prepublication Freeze

Status: **HOLD — PREPUBLICATION FREEZE**

Freeze date: **2026-09-17**

This file records the transition from a mutable research-hardening candidate to a validated prepublication freeze. It does **not** authorize publication, create a DOI, activate Zenodo metadata, create a GitHub release, or modify Production.

## Authoritative frozen state

Branch:
`prepublication-freeze-2026-09-17`

Exact commit SHA:
`820b41e06bfdd8f861e1177eef10c6c6160ebecd`

GitHub Actions run on that exact SHA:
`35227905797`

CI conclusion:
**success**

The authoritative frozen state is the exact Git commit and tree above, not a manually duplicated copy of the dataset.

## Authoritative prepublication artifact

GitHub Actions artifact ID:
`10499757161`

Artifact name:
`AI-Video-Signal-v2026.09.17-PREPUBLISH-820b41e06bfdd8f861e1177eef10c6c6160ebecd`

Artifact size:
`53,226 bytes`

GitHub artifact digest:
`sha256:ca7851c4c7eaed9605918ba7c756b58ea0123d0799d10abf07ae13d570c10a8b`

Artifact expiry:
`2026-12-16T13:34:19Z`

This artifact was produced by CI from the exact freeze SHA and passed the frozen-package validator before upload.

A later artifact produced from `main` is a development/pre-publication preview only and must **not** replace this authoritative freeze artifact when preparing the first DOI deposit unless a new freeze is explicitly declared and validated.

## Supporting HOLD candidate artifact from the same freeze run

Artifact ID:
`10500016830`

Name:
`AI-Video-Signal-RC-2026-09-17-HOLD`

Digest:
`sha256:b76c011dd4b07db7a77a74ea1814e5fc18609495c62f1c69b5e1a243c014a48c`

This supporting artifact is retained for reproducibility and comparison. The versioned `v2026.09.17-PREPUBLISH` artifact above is the authoritative deposit candidate.

## What the frozen state contains

- reconciled 14-provider CSV and JSON candidate;
- methodology and data dictionary;
- source and relationship-disclosure manifests;
- provider reconciliation records;
- quantitative evidence checks;
- reproducibility validators;
- citation metadata;
- custom-rights/Zenodo preparation;
- deterministic package builder;
- machine-readable package manifest generation;
- SHA-256 checksum generation and verification;
- HOLD safety controls;
- release-status and release-manifest controls.

## Validation result

On the exact freeze SHA, CI passed:

- provider reconciliation;
- CSV/JSON candidate parity;
- evidence/source coverage;
- relationship-disclosure consistency;
- quantitative evidence coverage;
- citation and Zenodo pre-release metadata checks;
- pre-freeze readiness;
- HOLD publication guard;
- candidate metric derivation;
- deterministic candidate package reconstruction;
- candidate SHA-256 package verification;
- frozen `v2026.09.17` prepublication package build;
- frozen package CSV/JSON parity validation;
- frozen package SHA-256 validation;
- upload of the frozen prepublication artifact.

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

The Zenodo new-deposit interface requires authentication. In the unauthenticated browser check, Zenodo presented sign-in options and did not expose the deposit form. Therefore no draft, upload, DOI reservation or publication was created.

Before publication, the verified custom AI Video Signal rights statement must be entered and previewed in an authenticated Zenodo draft. Publication authorization must remain false until that preview and the remaining final release checks pass.
