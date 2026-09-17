# AI Video Signal — Release Candidate Summary — 2026-09-17

Status: **HOLD — research candidate, not a DOI-backed release**

Candidate: `RC-2026-09-17-HOLD`

This summary is derived from `datasets/release-candidate-2026-09-17.csv`. It must not replace the dated Aug 29 public baseline or be presented as a final market benchmark until the remaining non-provider release gates pass.

## Candidate scope

- Provider records: **14**
- Checked date: **2026-09-17**
- CSV/JSON parity: automated
- Provider-level pricing reconciliation: **complete**
- Production baseline: **V70.7.5 untouched**

## USD paid-price normalization snapshot

The candidate currently contains **11** rows with both `normalization_state=normalized`, `currency=USD`, and a non-empty numeric `advertised_price`:

- Runway — $15
- HeyGen — $29
- InVideo AI — $20
- Fliki — $28
- Pika — $10
- Hailuo AI — $14.99 monthly billing
- Synthesia — $29
- ElevenLabs — $6
- OpusClip — $15
- Vizard — $29
- Submagic — $19

Derived descriptive statistics:

- Normalized USD paid-reference count: **11**
- Median: **$19/month or monthly-equivalent**
- Range: **$6–$29**

These are **HOLD-candidate statistics, not final published benchmark figures**.

Kling AI is intentionally excluded from this USD-only statistic because its verified current public membership pricing is in **CNY**. Google Veo remains endpoint-priced rather than monthly-plan normalized. Hypernatural has no comparable paid price promoted in this candidate.

## Reconciliation-status distribution

- `verified_no_material_change`: **8**
- `verified_material_change`: **3**
- `verified_current_cny_web_pricing`: **1**
- `verified_current_monthly_and_annual_pricing`: **1**
- `evidence_expanded_still_not_monthly_normalized`: **1**

There are **no remaining provider rows in pending/conflict/partial status**.

## Normalization-state distribution

- `normalized`: **11**
- `not_normalized`: **3**
- `caution`: **0**
- `unavailable`: **0**

## Commercial Rights Evidence Status distribution

- `documented_conditional`: **4**
- `unclear`: **4**
- `not_checked`: **5**
- `restricted`: **1**
- `documented_clear`: **0**

The absence of `documented_clear` is not a claim that no provider permits commercial use. It means the candidate preserves conditional, unclear or not-yet-checked evidence states rather than overclaiming legal certainty.

## Changes versus the Aug 29 public baseline

The Aug 29 research brief reported 11 normalized paid references and a $15 median. The current HOLD candidate differs because the research state has changed:

- InVideo AI and Pika have confirmed material current changes.
- Vizard's live dynamic Creator price is verified and normalized at $29/month.
- Submagic's limited free-entry state is specifically evidenced while the $19 Starter reference remains supported.
- Hypernatural's official support establishes no free plan and no free trial; its paid price remains not normalized.
- Hailuo's apparent pricing conflict is resolved as a billing-cadence distinction: $14.99 monthly versus $8.40/month equivalent billed $100.80/year; both carry 1,000 credits/month.
- Kling AI current public pricing is now verified in CNY and deliberately kept out of the USD-only statistic rather than converted silently.
- Google Veo remains endpoint-priced rather than monthly-plan normalized.

This is a **versioned research-state difference**, not a retroactive rewrite of the Aug 29 snapshot.

## Reproducibility

```bash
python reproducibility/validate_reconciliation.py
python reproducibility/validate_release_candidate.py
python reproducibility/validate_evidence_and_disclosures.py
python reproducibility/validate_metadata.py
python reproducibility/validate_release_guard.py
python reproducibility/derive_release_candidate_metrics.py
```

## Remaining release work

Provider-level reconciliation is complete. Remaining work is release packaging and publication control:

- freeze the immutable final dataset package;
- generate release checksums from the frozen package;
- finalize citation version/date metadata;
- preview the custom rights statement in the actual Zenodo draft;
- keep GitHub Actions green on the frozen commit;
- only then authorize publication and accept the DOI actually assigned by Zenodo.

## Release rule

Do not create a DOI, GitHub release, Zenodo publication, or production-site benchmark update from this candidate while `RELEASE_STATUS.md` remains HOLD.
