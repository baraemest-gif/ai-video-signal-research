# AI Video Signal Research

Public research repository for **AI Video Signal** benchmark datasets, methodology, reproducibility, citation metadata, and versioned research releases.

## Mission

AI Video Signal is building a citation-grade evidence layer for AI-video market intelligence. The research program focuses on pricing, credits, plan entitlements, model-level production economics, free access, commercial-use evidence, and documented market changes.

This repository is not a generic “best AI video tools” ranking. It is designed so material claims can be traced to evidence, derived calculations can be reproduced, and historical releases remain citable.

## Current scope

The current research baseline covers **14 AI-video providers**. Provider count is not treated as a quality metric. New providers are added only when they pass the same evidence and normalization standards.

## Research principles

- First-party evidence first.
- Every material claim carries a verification date and source.
- Facts, calculations, assumptions, and editorial interpretation remain separate.
- Missing values are never silently interpreted as zero, no, unlimited, or equivalent.
- Commercial-use conclusions preserve uncertainty and are not legal advice.
- Historical releases are immutable; corrections ship in a new release.
- Affiliate or commercial relationships do not alter factual research states.
- Documentation review is never presented as hands-on testing.
- Conflicting first-party evidence remains visible as a conflict until resolved or explicitly scoped.

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
- `datasets/` — release-ready CSV/JSON distributions and data dictionary.
- `reconciliation/` — dated provider reconciliation, machine-readable status files and provider fact-check queue.
- `reproducibility/` — validation and reproduction instructions, including CSV/JSON reconciliation validation.
- `release-candidate/` — pre-DOI staging manifest and Zenodo/DOI readiness controls; not a published release.
- `reports/` — research briefs and release notes.
- `CITATION.cff` — citation metadata used by GitHub and retained for citation support.
- `.zenodo.json.template` — inactive Zenodo metadata template. It must not be activated until license/usage terms are resolved and metadata is validated.
- `LICENSE_STATUS.md` — current reuse/license decision state; no standard license is invented.
- `CHANGELOG.md` — research change history.
- `RELEASE_STATUS.md` — current publication gate and blockers.

## Release policy

Citation-grade releases use immutable version identifiers and retain prior states.

**GitHub release → Zenodo archival deposit → DOI → persistent metadata → external citation and reuse**

A DOI must identify an immutable research release, not a silently changing live page.

## Current status

**HOLD — PRE-DOI RESEARCH HARDENING**

The 14-provider identity set is reconciled and a dated provider-status package now exists in matching CSV/JSON form. Confirmed current changes include InVideo AI and Pika; Hailuo AI and Hypernatural currently contain conflicting first-party evidence that must remain explicit. Kling AI, Vizard and Submagic also retain field-level verification work before the first citation-grade release.

The active `.zenodo.json` has intentionally been removed during hardening because the archival license/usage-rights mapping is not yet finalized. An inactive template is retained instead, preventing accidental publication with an invented or unintended license.

The first DOI-backed release remains blocked until provider-change reconciliation is complete at field level, unresolved facts are closed or explicitly represented as uncertainty in the release candidate, final release CSV/JSON and public files reconcile, reuse/license terms are unambiguous, and the package can be regenerated from a known source state.

## Production firewall

This repository is intentionally separate from the live product deployment path. The frozen production baseline **V70.7.5** is not modified by research-governance work in this repository.

## Publisher

**AI Video Signal**  
Creator: **Youssef Mestetef Ennaji**

Repository: https://github.com/baraemest-gif/ai-video-signal-research
