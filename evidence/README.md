# Evidence Manifest

AI Video Signal stores source provenance separately from normalized provider conclusions.

`source-manifest.csv` is a working pre-DOI registry of first-party and direct-verification sources used during the 2026-09-17 reconciliation pass.

## Evidence rules

- Tier A: first-party pricing, legal terms, product/help documentation, model documentation and official announcements.
- Tier B: direct provider fact-check responses tied to a specific factual field.
- Tier C: reputable external reporting only when first-party evidence is absent, ambiguous or needed for historical context.
- Tier D: community or secondary summaries only as discovery leads, never as the sole basis for a material benchmark field.

A source manifest entry does not mean every claim on the source is normalized. `state` records whether the evidence was verified, partial, contradictory, or associated with a material change.

Conflicting first-party evidence must remain visible until resolved or explicitly scoped. It must not be collapsed into a single convenient number.

The final DOI release should include a release-specific evidence manifest that is immutable with that release.
