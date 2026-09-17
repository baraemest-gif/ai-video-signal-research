# Reproducibility

A citation-grade AI Video Signal release must allow an independent reader to reproduce every derived number from released inputs without depending on the live website.

## Required calculation provenance

Every derived metric must record:

- raw input fields
- exact formula
- explicit assumptions
- unit
- applicable provider and plan
- applicable model/workflow
- generation mode
- duration and resolution where relevant
- source URLs
- evidence checked date
- release identifier

## CSV / JSON parity

CSV and JSON distributions belonging to the same release must represent the same provider records and material states. A release fails the reproducibility gate if the formats disagree.

The dated provider-reconciliation support package has an automated standard-library validator:

```bash
python3 reproducibility/validate_reconciliation.py
```

The validator checks:

- exactly 14 provider records in both files
- identical provider sets
- no duplicate or blank provider IDs
- matching baseline and current-check dates
- exact parity for provider, status, baseline reference, current evidence summary and release action
- `HOLD` release status while pre-DOI gates remain open

This validator covers the reconciliation support files only. A separate final-release validator must also cover the eventual citation-grade dataset, benchmark distributions, release manifest and checksums.

## Scenario versus observation

Scenario-based calculations must be labeled as scenarios. Assumptions must never be presented as measured behavior. Documentation-derived evidence must not be described as hands-on testing.

## Release reconstruction

Before archival publication, the release package should be reproducible from a known source state and include, where practical:

- exact released data files
- methodology version
- evidence/source manifest
- calculation definitions
- release manifest
- changelog
- citation metadata
- checksums

## Corrections

Historical releases remain immutable. Corrections appear in a subsequent release and identify the affected field, old state, new state, evidence and reason for correction.
