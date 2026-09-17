# Release Status

## STATUS: HOLD — PRE-DOI RESEARCH HARDENING

The first DOI-backed release must not be published until every mandatory gate below passes.

## Resolved / evidenced validations

- [x] **Pictory pricing-source protocol confirmed.** Pictory's Affiliate Manager instructed AI Video Signal to use the current live Pictory Pricing page as the source of truth for monthly/annual pricing, allowances, AI credits and plan inclusions; published comparisons should record the verification date and link back to the live pricing page. Email-supplied figures must not be treated as permanent entitlements.
- [x] **Google Search Console discoverability verified.** For the finalized period 2026-08-18 through 2026-09-14, `https://aivideosignal.com/` recorded 9,142 impressions and 14 clicks. The research dataset page also recorded impressions. This demonstrates Google discovery/index presence for the property and research pages; it does not imply that every URL is indexed or ranking well.

## Mandatory release gates

- [ ] Provider count reconciled across all release files.
- [ ] Provider-change reconciliation completed.
- [ ] Unresolved pricing facts for providers other than already-verified cases resolved or represented explicitly as uncertainty.
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
