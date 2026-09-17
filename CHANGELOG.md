# Changelog

All material research changes should be recorded here. Historical releases must never be silently overwritten.

## v2026.09.17 — DOI-backed first research release

### Published
- AI Video Signal Research Dataset 2026 published on Zenodo as a public Dataset.
- DOI assigned: `10.5281/zenodo.22816605`.
- DOI resolver: `https://doi.org/10.5281/zenodo.22816605`.
- Zenodo record: `https://zenodo.org/records/22816605`.
- Custom **AI Video Signal Dataset Rights & Reuse Terms** published instead of the default CC BY 4.0 license.
- Public independent download route established through Zenodo.

### Release integrity
- 14-provider reconciliation completed.
- CSV/JSON parity validated.
- Source-manifest and relationship-disclosure coverage validated.
- Material quantitative fields date/source scoped.
- Data freeze recorded at commit `820b41e06bfdd8f861e1177eef10c6c6160ebecd`.
- Package freeze recorded at commit `129273d47bde297de7ae4024ba8d07eaf3a00265`.
- Versioned prepublication artifact verified before deposit.
- Package manifest and SHA-256 checksums included in the deposited package.
- Production baseline `V70.7.5` remained untouched.

### Provider reconciliation highlights
- Pictory pricing-source protocol confirmed: live Pricing page is the current source of truth; checks are date-stamped and email figures are not treated as permanent entitlements.
- InVideo AI and Pika material changes propagated as dated changes rather than historical overwrite.
- Vizard current dynamic pricing resolved.
- Submagic limited free-entry state resolved.
- Hypernatural no-free-plan/no-trial state resolved from plan-specific official documentation.
- Kling AI current public CNY pricing retained as CNY and excluded from unsupported USD normalization.
- Hailuo AI monthly vs annual cadence resolved: Standard $14.99 monthly versus $8.40/month equivalent when billed $100.80/year, with 1,000 credits/month.
- Google Veo retained as endpoint-priced rather than forced into a monthly-plan comparison.

### Post-DOI synchronization
- `CITATION.cff` updated with the real DOI, version and publication date.
- Release manifest moved from `HOLD_PRE_DOI` to `PUBLISHED_ZENODO_DOI`.
- CI release-state validators updated to distinguish historical HOLD candidate integrity from the current published DOI state.

## Pre-release foundation / research hardening

### Added
- Public research repository foundation.
- Citation metadata via `CITATION.cff`.
- Inactive Zenodo archival metadata template without invented DOI or ORCID.
- Release-readiness gates and HOLD controls.
- Methodology, data dictionary, reproducibility and reports structure.
- Production firewall preserving V70.7.5.
- Provider reconciliation package for 2026-09-17 in Markdown, CSV and JSON.

### Validation progress — 2026-09-17
- Google Search Console discoverability verified for `https://aivideosignal.com/`: 9,142 impressions and 14 clicks for finalized period 2026-08-18 through 2026-09-14; the research dataset page also received impressions.
- Provider identity set fixed at 14 for the reconciliation pass.
- Automated evidence, quantitative, metadata, freeze and checksum validation added.

### Policy
- Corrections ship in a new release with a correction note.
- Each citation-grade release must be immutable and independently retrievable.
- CSV and JSON distributions from the same release must reconcile.
- Conflicting first-party evidence must remain visible as conflict/uncertainty until resolved; it must not be averaged, guessed or silently normalized.
