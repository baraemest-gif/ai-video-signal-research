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
- `reproducibility/` — validation and reproduction instructions.
- `reports/` — research briefs and release notes.
- `CITATION.cff` — citation metadata.
- `.zenodo.json` — archival metadata for Zenodo integration.
- `CHANGELOG.md` — research change history.
- `RELEASE_STATUS.md` — current publication gate and blockers.

## Release policy

Citation-grade releases use immutable version identifiers and retain prior states.

**GitHub release → Zenodo archival deposit → DOI → persistent metadata → external citation and reuse**

A DOI must identify an immutable research release, not a silently changing live page.

## Current status

**HOLD — PRE-DOI RESEARCH HARDENING**

The first DOI-backed release remains blocked until provider-change reconciliation is complete, unresolved pricing facts are closed or explicitly represented as uncertainty, CSV/JSON and public files reconcile, and the package can be regenerated from a known source state.

## Production firewall

This repository is intentionally separate from the live product deployment path. The frozen production baseline **V70.7.5** is not modified by research-governance work in this repository.

## Publisher

**AI Video Signal**  
Creator: **Youssef Mestetef Ennaji**

Repository: https://github.com/baraemest-gif/ai-video-signal-research
