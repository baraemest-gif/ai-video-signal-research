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
- deterministic package reconstruction;
- SHA-256 package verification.

## Publication controls

While status remains HOLD:

- `publication_authorized` remains `false`;
- DOI remains `null`;
- ORCID remains `null` unless explicitly supplied and verified;
- active `.zenodo.json` does not exist;
- no GitHub Release is authorized;
- no Zenodo publication is authorized;
- Production baseline **V70.7.5 remains untouched**.

## Next gate

The research state is now reproducibly frozen for prepublication review. Remaining work is release metadata and deposit governance: construct the final release-named distributions from this exact frozen state, assign the final immutable version/date consistently, preview the custom rights inside an actual Zenodo draft, and keep publication authorization false until every final gate passes.
