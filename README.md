# AI Video Signal Research

Public research repository for **AI Video Signal** benchmark datasets, methodology, reproducibility, citation metadata, and versioned research releases.

## Mission

AI Video Signal is building a citation-grade evidence layer for AI-video market intelligence. The research program focuses on pricing, credits, plan entitlements, model-level production economics, free access, commercial-use evidence, and documented market changes.

This repository is not a generic “best AI video tools” ranking. It is designed so material claims can be traced to evidence, derived calculations can be reproduced, and historical releases remain citable.

## DOI-backed release

**AI Video Signal Research Dataset 2026 — v2026.09.17**

- DOI: **10.5281/zenodo.22816605**
- DOI URL: https://doi.org/10.5281/zenodo.22816605
- Zenodo record: https://zenodo.org/records/22816605
- Publication date: **2026-09-17**
- Resource type: **Dataset**
- Creator: **Youssef Mestetef Ennaji**
- Rights: **AI Video Signal Dataset Rights & Reuse Terms**

The Zenodo record provides an independently retrievable immutable research package with machine-readable data, methodology, evidence manifests, reproducibility material, release manifests and cryptographic checksums.

## Start here

- **Research brief:** `reports/ai-video-pricing-market-snapshot-v2026.09.17.md`
- **External citation kit:** `outreach/CITATION_KIT.md`
- **Outreach tracker:** `outreach/OUTREACH_TRACKER.md`
- **Dataset JSON-LD:** `metadata/dataset.schema.jsonld`
- **Release status:** `RELEASE_STATUS.md`
- **Citation metadata:** `CITATION.cff`
- **BibTeX:** `CITATION.bib`
- **RIS:** `CITATION.ris`
- **CSL-JSON:** `CITATION.json`

## Current scope

The release covers **14 AI-video providers**. Provider count is not treated as a quality metric. New providers are added only when they pass the same evidence and normalization standards.

## Research principles

- First-party evidence first.
- Every material claim carries a verification date and source.
- Facts, calculations, assumptions, and editorial interpretation remain separate.
- Missing values are never silently interpreted as zero, no, unlimited, or equivalent.
- Commercial-use conclusions preserve uncertainty and are not legal advice.
- Historical releases are immutable; corrections ship in a new release.
- Affiliate or commercial relationships do not alter factual research states.
- Documentation review is never presented as hands-on testing.
- Conflicting first-party evidence remains visible until resolved or explicitly scoped.

## Core metrics

### Approved Output Cost (AOC)

`AOC = nominal generation cost × expected attempts per approved output`

If attempts are not measured, the value must be labeled as a scenario or assumption rather than an observation.

### Pricing Volatility Index (PVI)

A future longitudinal metric for documented material pricing, credit, allowance, or entitlement changes. No PVI score will be published until enough date-stamped historical observations exist to support a defensible methodology.

### Commercial Rights Evidence Status (CRES)

Evidence classification only, not legal advice and not a provider quality score.

States: `documented_clear`, `documented_conditional`, `unclear`, `restricted`, `not_checked`.

## Repository structure

- `methodology/` — benchmark rules, evidence hierarchy, normalization and calculation methods.
- `datasets/` — release/candidate CSV/JSON distributions and data dictionary.
- `reconciliation/` — dated provider reconciliation, machine-readable status files and provider fact-check records.
- `evidence/` — source and relationship-disclosure manifests.
- `reproducibility/` — validation, derivation and package reconstruction controls.
- `release-candidate/` — historical freeze, release-manifest and DOI/Zenodo governance records.
- `reports/` — research briefs and release notes.
- `outreach/` — external citation kit and outreach tracking.
- `metadata/` — machine-discovery metadata prepared for future deployment.
- `CITATION.cff` — current citation metadata including the real DOI.
- `.zenodo.json.template` — inactive historical/custom-rights metadata template; it is not the mechanism used for the published manual Zenodo deposit.
- `LICENSE_STATUS.md` — reuse/license governance.
- `CHANGELOG.md` — research change history.
- `RELEASE_STATUS.md` — current publication and synchronization state.

## Reproducibility

The release process validates provider reconciliation, CSV/JSON parity, evidence coverage, relationship disclosures, quantitative fields, citation metadata, release state, derived metrics and package checksums through GitHub Actions.

The source candidate remains preserved as a historical HOLD snapshot. The DOI-backed release records the exact publication metadata without rewriting that historical candidate state.

## Rights and reuse

Canonical terms:
https://aivideosignal.com/dataset-license/

Zenodo was published with the custom **AI Video Signal Dataset Rights & Reuse Terms**, not a silently substituted CC BY 4.0 license.

## Current status

**PUBLISHED — DOI ACTIVE**

DOI: **10.5281/zenodo.22816605**

Post-DOI repository synchronization is tracked in `RELEASE_STATUS.md`. A GitHub Release/tag is still a distribution-sync item and must point to the immutable freeze state rather than a later mutable `main` commit.

## Production firewall

This repository is intentionally separate from the live product deployment path. The frozen production baseline **V70.7.5** is not modified by research-governance or DOI publication work in this repository.

## Publisher / project

**AI Video Signal**  
Creator: **Youssef Mestetef Ennaji**

Repository: https://github.com/baraemest-gif/ai-video-signal-research
