# Changelog

All material research changes should be recorded here. Historical releases must never be silently overwritten.

## Unreleased — Repository foundation / pre-DOI research hardening

### Added
- Public research repository foundation.
- Citation metadata via `CITATION.cff`.
- Zenodo archival metadata template without invented DOI or ORCID.
- Release-readiness gate and HOLD status.
- Methodology, data dictionary, reproducibility and reports structure.
- Production firewall preserving V70.7.5.
- Provider reconciliation package for 2026-09-17 in Markdown, CSV and JSON.

### Validation progress — 2026-09-17
- Pictory pricing-source protocol confirmed by Pictory Affiliate Manager: use the current live Pricing page as source of truth, record verification date, and do not treat email figures as permanent plan entitlements.
- Google Search Console discoverability verified for `https://aivideosignal.com/`: 9,142 impressions and 14 clicks for finalized period 2026-08-18 through 2026-09-14. Research dataset page also received impressions.
- Search visibility issue reclassified from “indexation unknown” to “ranking/CTR optimization and page-level coverage”.
- Provider identity set fixed at 14 for the reconciliation pass.
- Runway, HeyGen, Fliki, Synthesia, ElevenLabs and OpusClip found materially consistent with the checked baseline fields.
- InVideo AI and Pika recorded as confirmed material changes requiring new dated change events rather than historical overwrite.
- Hailuo AI moved from pending access to `first_party_pricing_conflict`: official Subscription Service Terms support Standard $14.99/mo with 1,000 credits, while separate official Hailuo marketing/blog pages publish lower Standard prices. Current normalized pricing remains HOLD pending resolution or explicit scope separation.
- Hypernatural free-entry state remains HOLD because current official support states no free plan/trial while the public pricing page uses a “Start for free” CTA.
- Google Veo evidence expanded with explicit current endpoint pricing while monthly provider-plan pricing remains `not_normalized`.
- Reconciliation support CSV and JSON aligned to the same 14 provider status records.

### Policy
- Corrections ship in a new release with a correction note.
- Each citation-grade release must be immutable and independently retrievable.
- CSV and JSON distributions from the same release must reconcile.
- Conflicting first-party evidence must remain visible as conflict/uncertainty until resolved; it must not be averaged, guessed or silently normalized.
