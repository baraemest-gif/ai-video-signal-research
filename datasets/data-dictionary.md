# Data Dictionary

The following fields define the intended citation-grade provider record. Fields may be unavailable or not normalized; those states must remain explicit.

| Field | Meaning |
|---|---|
| `provider_name` | Canonical provider name. |
| `canonical_url` | Canonical first-party URL. |
| `plan_name` | Plan name applicable to the record. |
| `billing_interval` | Monthly, annual or other documented billing interval. |
| `advertised_price` | Native advertised price before derived normalization. |
| `currency` | Native price currency. |
| `credits_or_allowance` | Documented credits, generation allowance or equivalent entitlement. |
| `model_name` | Model name where applicable. |
| `workflow_name` | Product workflow or generation path. |
| `duration` | Output duration constraint or benchmarked duration. |
| `resolution` | Output resolution constraint or benchmarked resolution. |
| `generation_mode` | Generation mode relevant to the record. |
| `nominal_generation_cost` | Reproducibly calculated nominal generation cost when defensible. |
| `retry_assumption` | Measured retry information or explicitly labeled scenario assumption. |
| `approved_output_cost` | Derived AOC value when calculation requirements are satisfied. |
| `free_access_state` | Free-entry, trial or no-free-access state with evidence. |
| `commercial_rights_evidence_status` | CRES classification. |
| `source_url` | Primary evidence source URL for the record. Conflicting/multiple sources belong in the evidence manifest or research note rather than being silently collapsed. |
| `source_type` | Source category, such as pricing, terms, docs, provider response or external report. |
| `evidence_tier` | Tier A, B, C or D under the methodology. |
| `checked_at` | Date or timestamp when evidence was verified. |
| `last_material_change_at` | Date of last documented material change when known. Unknown change dates stay blank. |
| `relationship_disclosure` | Affiliate/commercial relationship disclosure where relevant. A blank means not yet populated, not “no relationship.” |
| `normalization_state` | Data normalization state. |
| `reconciliation_status` | Current field-level/provider-level reconciliation state for a pre-release candidate. |
| `research_note` | Explicit explanation for material changes, uncertainty, conflicts or withheld normalization. |
| `release_id` | Immutable research release identifier, or explicit release-candidate identifier while status is HOLD. |
| `record_version` | Version of the individual record or schema state. |

## `normalization_state`

Allowed values:

- `normalized`
- `not_normalized`
- `unclear`
- `caution`
- `unavailable`

## `commercial_rights_evidence_status`

Allowed values:

- `documented_clear`
- `documented_conditional`
- `unclear`
- `restricted`
- `not_checked`

## `reconciliation_status`

Current release-candidate values include:

- `verified_no_material_change`
- `verified_material_change`
- `pending_first_party_access`
- `first_party_pricing_conflict`
- `partial_verified`
- `needs_correction_or_change_event`
- `evidence_expanded_still_not_monthly_normalized`

These are research-governance states, not provider quality scores.

## Null and missing-value policy

A blank or missing field must never be interpreted automatically as zero, false, no commercial use, unlimited usage, unavailable, “no relationship,” or any other substantive state. Unknowns remain unknown until evidence supports a classification.

## Release-candidate policy

A release-candidate identifier containing `HOLD` is not a published research release and must not be cited as if it has a DOI. Candidate files can be regenerated or corrected until the release gates pass. Once a DOI-backed release is published, that immutable release must not be overwritten.
