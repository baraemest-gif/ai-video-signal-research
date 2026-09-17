# Release Status

## STATUS: HOLD — PRE-DOI RESEARCH HARDENING

The first DOI-backed release must not be published until every mandatory gate below passes.

## Resolved / evidenced validations

- [x] **Pictory pricing-source protocol confirmed.** Pictory's Affiliate Manager instructed AI Video Signal to use the current live Pictory Pricing page as the source of truth for monthly/annual pricing, allowances, AI credits and plan inclusions; published comparisons should record the verification date and link back to the live pricing page. Email-supplied figures must not be treated as permanent entitlements.
- [x] **Google Search Console discoverability verified.** For the finalized period 2026-08-18 through 2026-09-14, `https://aivideosignal.com/` recorded 9,142 impressions and 14 clicks. The research dataset page also recorded impressions. This demonstrates Google discovery/index presence for the property and research pages; it does not imply that every URL is indexed or ranking well.
- [x] **Provider identity set fixed and reconciled at 14 providers.** The 2026-09-17 reconciliation explicitly covers Runway, Kling AI, HeyGen, InVideo AI, Fliki, Pika, Hailuo AI, Synthesia, ElevenLabs, OpusClip, Vizard, Submagic, Hypernatural and Google Veo.
- [x] **Reconciliation support CSV/JSON parity established.** The provider-status reconciliation is represented in matching CSV and JSON support files. This does not yet satisfy the final release-dataset parity gate.

## Open provider reconciliation issues

- **Kling AI:** current first-party pricing page still needs a directly accessible first-party recheck or provider confirmation.
- **Hailuo AI:** first-party pricing conflict. Subscription Service Terms list Standard at $14.99/mo with 1,000 credits, while separate official marketing/blog pages publish lower Standard prices. Do not collapse these into one current normalized value.
- **Vizard:** free-plan evidence is current, but a stable current normalized paid Creator price was not obtained from the dynamic pricing representation.
- **Submagic:** current Starter paid reference is supported; current free-tier state needs recheck before release.
- **Hypernatural:** official Help Center says no free plan/trial while the public pricing page uses a “Start for free” CTA; free-entry state remains unresolved.
- **InVideo AI and Pika:** material current changes are confirmed and must be propagated into the release-candidate dataset and any derived benchmark metrics without rewriting historical snapshots.

## Mandatory release gates

- [ ] Provider count reconciled across all final release files.
- [ ] Provider-change reconciliation completed at field level.
- [ ] Unresolved pricing facts resolved or represented explicitly as uncertainty in the release candidate.
- [ ] Final release CSV and JSON distributions represent the same provider states.
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
