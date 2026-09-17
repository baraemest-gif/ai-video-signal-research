# AI Video Signal — DOI Release Playbook

Status: **HOLD — operational checklist only**

This playbook defines the exact sequence for the first immutable research release. It does not authorize publication while `RELEASE_STATUS.md` remains HOLD.

## 1. Close provider blockers

Required before freeze:

- Kling AI current first-party/provider-confirmed pricing state is resolved or explicitly represented as uncertainty.
- Hailuo AI first-party pricing conflict is resolved or explicitly scoped in the final dataset.
- No historical snapshot is overwritten by a current-state correction.

## 2. Freeze the release candidate

When the remaining blockers are closed:

- assign an immutable version using `vYYYY.MM.DD`;
- copy the final provider dataset to release-named CSV and JSON distributions;
- preserve the 2026-09-17 HOLD candidate as research history;
- freeze methodology, evidence manifest, relationship-disclosure manifest and changelog for that version;
- do not change Production V70.7.5.

## 3. Run all validators

The release must pass:

```bash
python reproducibility/validate_reconciliation.py
python reproducibility/validate_release_candidate.py
python reproducibility/validate_evidence_and_disclosures.py
python reproducibility/validate_metadata.py
python reproducibility/validate_release_guard.py
python reproducibility/derive_release_candidate_metrics.py
```

During HOLD, `validate_release_guard.py` must confirm that publication remains unauthorized. Before an actual release, that guard must be intentionally revised together with `RELEASE_STATUS.md` and the release manifest in one reviewed change.

## 4. Final metadata

Only after the immutable version exists:

- add the confirmed release version and release date to citation metadata;
- do not add an ORCID unless a real ORCID has been supplied and verified;
- do not invent a DOI;
- activate Zenodo metadata only after the custom rights statement has been entered and previewed correctly;
- ensure repository, website, citation metadata and Zenodo describe the same release.

## 5. Rights and reuse

Canonical public terms: `https://aivideosignal.com/dataset-license/`.

The first deposit must preserve those custom terms. Do not silently substitute CC BY, CC0, MIT or another standard license that grants broader reuse rights than the published AI Video Signal terms.

## 6. Immutable package contents

Minimum package:

- final provider dataset CSV;
- final provider dataset JSON;
- methodology snapshot;
- evidence/source manifest;
- relationship-disclosure manifest;
- changelog;
- citation metadata;
- rights/usage statement;
- reproducibility instructions and validators;
- release manifest;
- checksums.

CSV and JSON must represent the same provider states.

## 7. Create GitHub release

Only after all mandatory gates are green:

- tag the exact immutable commit;
- create a GitHub release from that tag;
- attach or expose the immutable research package;
- preserve earlier research states and tags.

## 8. Create Zenodo deposit

- connect/import the exact GitHub release or upload the exact frozen package;
- enter the custom AI Video Signal rights statement;
- verify creator, title, version, publication date and repository relationship;
- preview every metadata field;
- publish only after all metadata matches the immutable release.

Zenodo assigns the DOI. The DOI must be recorded only after Zenodo actually issues it.

## 9. Post-DOI update

After DOI issuance:

- update `CITATION.cff` with the real DOI and immutable version;
- update the release manifest with the real DOI;
- add the DOI to the canonical research page and structured Dataset metadata;
- do not rewrite the archived release itself;
- record the change in `CHANGELOG.md`.

## 10. External citation phase

Only after the DOI-backed release is live:

- provide the immutable citation to media, researchers and benchmark publishers;
- track independent citations/reuse separately from owned-domain mentions;
- do not describe AI Video Signal as globally authoritative solely because a DOI exists.

## Production firewall

Nothing in this playbook authorizes changes to Production, V70.7.5, DNS, Cloudflare, payment systems or the live application code.
