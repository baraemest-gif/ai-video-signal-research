# Zenodo / DOI Readiness

Status: **HOLD**

Checked against current Zenodo guidance on 2026-09-17.

## Confirmed behavior

- Zenodo can archive GitHub releases once a repository is enabled in the Zenodo GitHub integration.
- A published Zenodo record receives a DOI; a DOI can also be reserved before publication when needed for final files.
- When both `.zenodo.json` and `CITATION.cff` exist, Zenodo uses `.zenodo.json` for GitHub release archiving and ignores `CITATION.cff` for that ingestion path.
- Zenodo deposit metadata requires a license when access is open or embargoed under the documented deposit metadata rules.
- `CITATION.cff` remains useful for GitHub citation display even when Zenodo later uses `.zenodo.json`.

## Repository safety decision

The active `.zenodo.json` file has been removed during pre-DOI hardening. An inactive `.zenodo.json.template` is retained instead.

Reason: AI Video Signal has not yet finalized the file license/usage-rights mapping for the archival dataset. Activating open Zenodo metadata before resolving that policy could create an unintended or inconsistent rights statement.

## Activation gate

Before renaming `.zenodo.json.template` to `.zenodo.json`:

1. Resolve the exact archival license/usage-rights policy.
2. Select a valid Zenodo license identifier if the record will be open or embargoed.
3. Remove template-control fields.
4. Validate the resulting JSON against Zenodo's accepted metadata structure.
5. Ensure title, creators, upload type and related identifiers match the immutable release.
6. Add version/date only when the actual release exists.
7. Add DOI only after it has been reserved or assigned.
8. Add ORCID only if supplied and verified by the creator.

## Publication sequence

Release gates pass -> build immutable package -> validate CSV/JSON and metadata -> choose/confirm archival license -> activate Zenodo metadata -> create immutable GitHub release -> archive/publish in Zenodo -> obtain DOI -> add DOI to subsequent citation surfaces without rewriting the already archived files unless the DOI was reserved in advance.

No step in this document authorizes a production deployment or modification of V70.7.5.
