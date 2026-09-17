# Release Status

## STATUS: HOLD — PRE-DOI RESEARCH HARDENING

The first DOI-backed release must not be published until every mandatory gate below passes.

## Mandatory release gates

- [ ] Provider count reconciled across all release files.
- [ ] Provider-change reconciliation completed.
- [ ] Unresolved pricing facts resolved or represented explicitly as uncertainty.
- [ ] CSV and JSON distributions represent the same provider states.
- [ ] Public files agree on all material states.
- [ ] Every material quantitative field is sourced or clearly derived.
- [ ] Verification dates are present for material claims.
- [ ] Commercial-rights uncertainty is preserved rather than simplified.
- [ ] Source hierarchy is respected.
- [ ] Derived metrics are reproducible from released inputs.
- [ ] Relationship disclosures are current.
- [ ] Methodology is included.
- [ ] Citation metadata is valid.
- [ ] License or usage terms are explicitly resolved.
- [ ] Immutable package can be regenerated from a known source state.
- [ ] Prior releases remain retrievable.
- [ ] Public download is independent from the live buyer-facing site.

A failed gate means HOLD, not “publish now and fix later.”

## Production firewall

Production baseline **V70.7.5 remains frozen**. Repository, DOI, citation, methodology, research packaging and archival work do not authorize any production code change, deployment, DNS change, infrastructure change or live-data-model change.
