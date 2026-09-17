# Datasets

This directory is reserved for citation-grade, versioned research distributions.

## Intended release assets

Each major research release may include:

- provider dataset in CSV
- provider dataset in JSON
- pricing benchmark distribution where applicable
- evidence/source manifest
- machine-readable release manifest
- checksums for immutable files when practical

## Release rules

- CSV and JSON for the same release must reconcile exactly.
- Every material quantitative field must be sourced or clearly derived.
- Verification dates must be present for material claims.
- Missing values must remain explicit and must not be converted to zero or false values.
- Commercial-rights uncertainty must remain visible.
- Historical distributions must remain retrievable after corrections.
- A live website is not a substitute for an immutable release asset.

## Current state

No citation-grade dataset release is asserted yet. The first DOI release remains on HOLD until the release gates in `../RELEASE_STATUS.md` pass.
