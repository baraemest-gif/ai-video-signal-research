# AI Video Signal — Release Candidate Summary — 2026-09-17

Status: **HOLD — internal/public-repository research candidate, not a DOI-backed release**

Candidate: `RC-2026-09-17-HOLD`

This summary is derived from `datasets/release-candidate-2026-09-17.csv`. It must not replace the dated Aug 29 public baseline or be presented as a final market benchmark until the remaining release gates pass.

## Candidate scope

- Provider records: **14**
- Checked date: **2026-09-17**
- Exact CSV/JSON parity: enforced by validator and GitHub Actions
- Production baseline: **V70.7.5 untouched**

## Paid-price normalization snapshot

The release candidate currently contains **9** rows with both:

1. `normalization_state=normalized`, and
2. a non-empty numeric `advertised_price`.

Those 9 references are:

- Runway — $15
- HeyGen — $29
- InVideo AI — $20
- Fliki — $28
- Pika — $10
- Synthesia — $29
- ElevenLabs — $6
- OpusClip — $15
- Submagic — $19

Derived descriptive statistics for this HOLD candidate:

- Normalized paid-reference count: **9**
- Median: **$19/month or monthly-equivalent**
- Range: **$6–$29**

These figures are **candidate statistics, not final published benchmark figures**. Hailuo, Kling, Vizard, Hypernatural and Google Veo are excluded from this paid-price statistic because the current candidate does not support a clean comparable normalized paid price for those rows.

## Reconciliation-status distribution

- `verified_no_material_change`: **6**
- `verified_material_change`: **2**
- `partial_verified`: **2**
- `pending_first_party_access`: **1**
- `first_party_pricing_conflict`: **1**
- `needs_correction_or_change_event`: **1**
- `evidence_expanded_still_not_monthly_normalized`: **1**

## Normalization-state distribution

- `normalized`: **9**
- `caution`: **2**
- `not_normalized`: **2**
- `unavailable`: **1**

## Commercial Rights Evidence Status distribution

- `documented_conditional`: **4**
- `unclear`: **4**
- `not_checked`: **5**
- `restricted`: **1**
- `documented_clear`: **0**

The absence of `documented_clear` in this candidate is not a claim that no provider permits commercial use. It means the current provider-level candidate has intentionally preserved conditional, unclear or not-yet-checked states rather than overclaiming legal certainty.

## Why the candidate differs from the Aug 29 public baseline

The Aug 29 research brief reported 11 normalized paid references and a $15 median. The current HOLD candidate is deliberately more conservative because:

- InVideo AI and Pika have confirmed material current changes.
- Hailuo AI has conflicting current first-party pricing evidence.
- Kling AI still needs a fresh current first-party/provider confirmation.
- Vizard's paid Creator price was not stable enough in the retrieved representation for clean normalization.
- Hypernatural has a first-party free-access contradiction and no comparable paid price promoted in this candidate.
- Google Veo remains endpoint-priced rather than monthly-plan normalized.

The difference is therefore a **versioned research-state difference**, not a retroactive correction of the Aug 29 snapshot.

## Reproducibility

Run:

```bash
python reproducibility/validate_release_candidate.py
python reproducibility/derive_release_candidate_metrics.py
```

The first command validates the candidate structure/parity. The second derives the paid-price and status statistics directly from the candidate CSV.

## Release rule

Do not create a DOI, GitHub release, Zenodo publication, or production-site benchmark update from this candidate while `RELEASE_STATUS.md` remains HOLD.
