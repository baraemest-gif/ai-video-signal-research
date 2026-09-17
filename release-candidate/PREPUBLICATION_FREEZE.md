# AI Video Signal — Prepublication Freeze

Status: **HOLD — PREPUBLICATION FREEZE**

Freeze date: **2026-09-17**

This file records the transition from a mutable research-hardening candidate to a prepublication freeze target. It does **not** authorize publication, create a DOI, activate Zenodo metadata, create a GitHub release, or modify Production.

## Freeze semantics

The authoritative frozen state is an exact Git commit and its tree, not a manually duplicated copy of the dataset.

The freeze branch must point to a commit that contains:

- the reconciled 14-provider CSV and JSON candidate;
- methodology and data dictionary;
- source and relationship-disclosure manifests;
- provider reconciliation records;
- reproducibility validators;
- citation metadata;
- custom-rights/Zenodo preparation;
- deterministic package builder and SHA-256 verifier;
- release-status and release-manifest controls.

## Publication controls

While status remains HOLD:

- `publication_authorized` must remain `false`;
- DOI must remain `null`;
- ORCID must remain `null` unless explicitly supplied and verified;
- active `.zenodo.json` must not exist;
- Production baseline V70.7.5 must remain untouched;
- no GitHub Release or Zenodo publication is authorized.

## Next gate

After the freeze commit is recorded, run the complete CI workflow on the exact frozen state. Only after that succeeds may final release metadata and the Zenodo draft preview be prepared. Publication still requires a separate explicit release decision.
