# AI Video Signal — Release Candidate Summary — 2026-09-17

Status: **HOLD — research candidate, not a DOI-backed release**

Candidate: `RC-2026-09-17-HOLD`

This summary is derived from `datasets/release-candidate-2026-09-17.csv`. It must not replace the dated Aug 29 public baseline or be presented as a final market benchmark until the remaining release gates pass.

## Candidate scope

- Provider records: **14**
- Checked date: **2026-09-17**
- CSV/JSON parity: automated
- Production baseline: **V70.7.5 untouched**

## Paid-price normalization snapshot

The candidate currently contains **10** rows with both `normalization_state=normalized` and a non-empty numeric `advertised_price`:

- Runway — $15
- HeyGen — $29
- InVideo AI — $20
- Fliki — $28
- Pika — $10
- Synthesia — $29
- ElevenLabs — $6
- OpusClip — $15
- Vizard — $29
- Submagic — $19

Derived descriptive statistics:

- Normalized paid-reference count: **10**
- Median: **$19.50/month or monthly-equivalent**
- Range: **$6–$29**

These are **HOLD-candidate statistics, not final published benchmark figures**. Kling AI, Hailuo AI, Hypernatural and Google Veo remain excluded from this monthly paid-price statistic because the current candidate does not support a clean comparable normalized paid price for those rows.

## Reconciliation-status distribution

- `verified_no_material_change`: **8**
- `verified_material_change`: **3**
- `pending_first_party_access`: **1**
- `first_party_pricing_conflict`: **1**
- `evidence_expanded_still_not_monthly_normalized`: **1**

## Normalization-state distribution

- `normalized`: **10**
- `caution`: **1**
- `not_normalized`: **2**
- `unavailable`: **1**

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
- Vizard's live dynamic Creator price is now verified and normalized at $29/month.
- Submagic's limited free-entry state is now specifically evidenced while the $19 Starter reference remains supported.
- Hypernatural's current official support establishes no free plan and no free trial; its paid price remains not normalized in this candidate.
- Hailuo AI has incompatible current first-party Standard-plan prices and is excluded from the current paid-price statistic.
- Kling AI still needs direct current plan-price/credit verification.
- Google Veo remains endpoint-priced rather than monthly-plan normalized.

This is a **versioned research-state difference**, not a retroactive rewrite of the Aug 29 snapshot.

## Reproducibility

```bash
python reproducibility/validate_reconciliation.py
python reproducibility/validate_release_candidate.py
python reproducibility/validate_evidence_and_disclosures.py
python reproducibility/derive_release_candidate_metrics.py
```

## Release rule

Do not create a DOI, GitHub release, Zenodo publication, or production-site benchmark update from this candidate while `RELEASE_STATUS.md` remains HOLD.
