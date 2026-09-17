# Release Status

## STATUS: HOLD — PACKAGE FROZEN, ZENODO PREVIEW PENDING

AI Video Signal has completed provider reconciliation, quantitative/source validation, deterministic package construction and a versioned prepublication freeze for **v2026.09.17**. Publication is still **not authorized** and no DOI has been assigned.

## Current frozen state

### Data freeze

- Branch: `prepublication-freeze-2026-09-17`
- Commit: `820b41e06bfdd8f861e1177eef10c6c6160ebecd`
- CI run: `35227905797`
- Result: **SUCCESS**

### Package freeze

- Branch: `package-freeze-v2026.09.17-prepublish`
- Commit: `129273d47bde297de7ae4024ba8d07eaf3a00265`
- CI run: `35228530529`
- Result: **SUCCESS**

### Frozen prepublication artifact

- Version: `v2026.09.17`
- Artifact: `AI-Video-Signal-v2026.09.17-PREPUBLISH-129273d47bde297de7ae4024ba8d07eaf3a00265`
- Artifact ID: `10500370413`
- Size: `55,535 bytes`
- Archive SHA-256: `5e14ea9f7a7845206bae936b5426413eeb77d623f6c9b1b3776ca40eb52e381f`
- Retention: 90 days
- Publication authorized: **false**
- DOI: **null**

## Research gates completed

- [x] 14-provider identity set reconciled.
- [x] Provider-change reconciliation complete at field level.
- [x] No current provider value is guessed; non-comparable scopes remain explicit.
- [x] Candidate CSV/JSON exact parity automated.
- [x] InVideo AI and Pika material changes propagated without rewriting history.
- [x] Kling AI current public CNY membership pricing scoped and verified.
- [x] Hailuo AI monthly vs annual pricing cadence resolved.
- [x] Vizard dynamic current pricing resolved.
- [x] Submagic limited free-entry state resolved.
- [x] Hypernatural no-free-plan/no-trial state resolved.
- [x] Material quantitative fields source/date-scoped.
- [x] Source manifest coverage automated.
- [x] Relationship disclosures evidence-scoped and validated.
- [x] Commercial-rights uncertainty preserved through CRES.
- [x] Methodology and data dictionary included.
- [x] Candidate metrics reproducible from released inputs.
- [x] Pre-release citation metadata validated.
- [x] HOLD publication guard active.
- [x] Deterministic candidate package reconstruction verified.
- [x] Versioned `v2026.09.17` prepublication package built.
- [x] Versioned package CSV/JSON parity verified.
- [x] Package manifest and SHA-256 checksums generated and verified.
- [x] Exact package-freeze commit passed GitHub Actions.
- [x] Production **V70.7.5 remains untouched**.

## Current quantitative snapshot

The frozen candidate contains **11 normalized USD paid references**.

- Median: **$19/month or monthly-equivalent**
- Range: **$6–$29**
- Kling AI is excluded from the USD statistic because its directly verified current web price is CNY-scoped.
- Google Veo remains endpoint-priced rather than monthly-plan normalized.

These numbers remain prepublication research until the DOI-backed release is published.

## Rights / license state

Canonical public terms:
`https://aivideosignal.com/dataset-license/`

Effective date: **2026-08-31**.

Zenodo requires a license and defaults to CC BY 4.0. AI Video Signal must **not** accept that default silently because the current public terms reserve full-file redistribution, mirroring, sale and substantial competing commercial reuse without prior permission.

The package therefore uses a **custom AI Video Signal rights statement**. The exact rights text is already prepared for the Zenodo draft.

## Remaining gates before publication

- [ ] Enter the prepared custom rights/license in an actual Zenodo draft and verify the preview does not broaden the public terms.
- [ ] Verify title, creator, version and related repository identifier in the Zenodo draft.
- [ ] Set the actual publication date only when publication is authorized.
- [ ] Keep DOI blank until Zenodo assigns the real DOI.
- [ ] Verify final public release/download route independently from the live buyer-facing application.
- [ ] Confirm prior version/release retrievability when versioning begins.
- [ ] Keep CI green on the publication commit/tag.
- [ ] Explicitly authorize publication only after every final gate above passes.
- [ ] After Zenodo assigns the DOI, record that real DOI in citation metadata and the canonical research page without rewriting the archived release.

## Publication rule

Until the remaining gates pass:

- no GitHub Release publication;
- no Zenodo publication;
- no invented DOI;
- no invented ORCID;
- no active `.zenodo.json` that could publish incorrect rights;
- `publication_authorized=false`;
- status remains **HOLD**.

## Production firewall

Production baseline **V70.7.5 remains frozen**. Research packaging, citation metadata, GitHub branches, artifacts and Zenodo preparation do not authorize production code changes, deployments, DNS changes, infrastructure changes or live-data-model changes.
