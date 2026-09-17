# AI Video Signal — Freeze Readiness

Status: **READY FOR FREEZE ENGINEERING — PUBLICATION STILL HOLD**

Candidate: `RC-2026-09-17-HOLD`

Checked: **2026-09-17**

This document records that the current research candidate has passed the technical gates required to begin building a frozen final release package. It does **not** authorize publication, create a GitHub release, activate Zenodo metadata, assign a DOI, or modify Production.

## Passed gates

- 14-provider identity set reconciled.
- Provider-change reconciliation complete for the current candidate.
- No provider row remains in pending/conflict/partial reconciliation state.
- CSV/JSON candidate parity exact.
- Verification/check dates present.
- Relationship disclosures populated and evidence-scoped.
- Candidate source URLs covered by the source manifest.
- Material quantitative values are source/date scoped.
- Numeric advertised prices carry currency and billing context.
- Non-comparable CNY/endpoint pricing is not silently normalized into the USD benchmark.
- Commercial-rights uncertainty preserved.
- Pre-DOI `CITATION.cff` metadata validated.
- Inert Zenodo custom-rights template validated.
- Active `.zenodo.json` absent.
- HOLD release guard passes.
- Candidate metrics derive reproducibly from released inputs.
- Candidate package builds reproducibly in CI.
- Package manifest and SHA-256 checksums validate successfully.
- Production baseline remains `V70.7.5` and is not modified by research work.

## Current candidate metrics

- Provider records: **14**
- Normalized USD paid references: **11**
- USD paid-reference median: **$19/month or monthly-equivalent**
- USD range: **$6–$29**
- Kling AI: current public CNY pricing retained outside the USD-only statistic.
- Google Veo: endpoint-priced and intentionally not normalized as a monthly subscription.

These remain HOLD-candidate statistics until a final immutable release is frozen and published.

## Remaining publication gates

The research candidate is ready for freeze engineering, but publication remains blocked until:

1. final frozen CSV/JSON release distributions are created from this validated candidate;
2. the final frozen package receives release-specific SHA-256 checksums;
3. final version and publication-date citation metadata are inserted consistently;
4. the custom AI Video Signal rights statement is entered and previewed correctly in an actual Zenodo draft;
5. final public-release files are reconciled with the frozen package;
6. CI passes on the exact frozen commit;
7. publication is explicitly authorized in the release manifest;
8. Zenodo actually assigns the DOI.

## Safety state

- `RELEASE_STATUS.md`: HOLD
- `publication_authorized`: false
- DOI: null
- ORCID: null unless separately supplied and verified
- Active `.zenodo.json`: absent
- Production modified: false

## Production firewall

Nothing in this document authorizes any change to Production, `V70.7.5`, DNS, Cloudflare, payment systems, or the live application.
