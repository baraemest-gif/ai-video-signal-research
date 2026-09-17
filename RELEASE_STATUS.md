# Release Status

## STATUS: HOLD — PRE-DOI RESEARCH HARDENING

The first DOI-backed release must not be published until every mandatory gate below passes.

## Resolved / evidenced validations

- [x] **Pictory pricing-source protocol confirmed.** Pictory's Affiliate Manager instructed AI Video Signal to use the current live Pictory Pricing page as the source of truth for monthly/annual pricing, allowances, AI credits and plan inclusions; published comparisons should record the verification date and link back to the live pricing page. Email-supplied figures must not be treated as permanent entitlements.
- [x] **Google Search Console discoverability verified.** For the finalized period 2026-08-18 through 2026-09-14, `https://aivideosignal.com/` recorded 9,142 impressions and 14 clicks. The research dataset page also recorded impressions. This demonstrates Google discovery/index presence for the property and research pages; it does not imply that every URL is indexed or ranking well.
- [x] **Provider identity set fixed and reconciled at 14 providers.** The 2026-09-17 reconciliation explicitly covers Runway, Kling AI, HeyGen, InVideo AI, Fliki, Pika, Hailuo AI, Synthesia, ElevenLabs, OpusClip, Vizard, Submagic, Hypernatural and Google Veo.
- [x] **Reconciliation support CSV/JSON parity established.** The provider-status reconciliation is represented in matching CSV and JSON support files.
- [x] **14-provider release candidate created in CSV and JSON.** `datasets/release-candidate-2026-09-17.csv` and `.json` carry the same 14-provider candidate identity and remain explicitly `HOLD` / `RC-2026-09-17-HOLD`.
- [x] **Confirmed InVideo AI and Pika changes propagated into the release candidate without rewriting historical snapshots.** Historical Aug 29 / Sep 7 states remain historical evidence; the candidate carries the current checked state.
- [x] **Unresolved current facts are explicit rather than guessed.** Kling current pricing is unavailable pending recheck; Hailuo and Hypernatural retain first-party conflict/caution states; Vizard and Submagic retain partial verification states.
- [x] **Relationship disclosures populated for the current release candidate from connected-mail evidence.** Confirmed affiliate/partner relationships are explicitly disclosed for Synthesia, ElevenLabs, OpusClip, Vizard, Submagic and Hypernatural. Runway, Kling AI, HeyGen, InVideo AI, Fliki and Hailuo are recorded only as application/inquiry states where approval is not evidenced. Pika and Google Veo are explicitly described only as having no relationship evidenced in the connected mailbox as of 2026-09-17; absence of email evidence is not treated as proof that no relationship exists.
- [x] **Automated parity validator added and CI passing.** GitHub Actions `Validate research data` completed successfully on the current research-data state. The workflow runs reconciliation and release-candidate validators and preserves mandatory HOLD semantics.
- [x] **Candidate metric derivation is reproducible.** `reproducibility/derive_release_candidate_metrics.py` derives descriptive paid-price and status metrics directly from the candidate CSV. `reports/release-candidate-summary-2026-09-17.md` records the HOLD-only interpretation and explicitly prevents those candidate statistics from replacing the dated public baseline.
- [x] **Public reuse terms verified and Zenodo rights path mapped.** The canonical `https://aivideosignal.com/dataset-license/` terms were re-read on 2026-09-17. Their effective date is 2026-08-31. They permit citation and limited editorial/research excerpts with attribution but reserve full-file redistribution, mirroring, sale and substantial competing-dataset reuse without permission. Zenodo supports custom licenses/right statements, so the planned DOI deposit will use a custom AI Video Signal rights statement rather than silently accepting Zenodo's default CC BY 4.0.

## Open provider reconciliation issues

- **Kling AI:** current first-party pricing page still needs a directly accessible first-party recheck or provider confirmation.
- **Hailuo AI:** first-party pricing conflict. Subscription Service Terms list Standard at $14.99/mo with 1,000 credits, while separate official marketing/blog pages publish lower Standard prices. Do not collapse these into one current normalized value.
- **Vizard:** free-plan evidence is current, but a stable current normalized paid Creator price was not obtained from the dynamic pricing representation.
- **Submagic:** current Starter paid reference is supported; current free-tier state needs recheck before release.
- **Hypernatural:** official Help Center says no free plan/trial while the public pricing page uses a “Start for free” CTA; free-entry state remains unresolved.

## Other open release issues

- The verified custom reuse terms still need to be entered and previewed in the actual Zenodo draft before the final license gate is marked complete.
- Active `.zenodo.json` metadata remains intentionally disabled until final metadata and rights are verified in the draft.
- Final release manifest/checksums must be generated from the frozen final candidate, not from this mutable HOLD candidate.
- Public buyer-facing research files have not yet been regenerated from the new release-candidate state; Production V70.7.5 remains untouched by design.

## Mandatory release gates

- [ ] Provider count reconciled across all final release files.
- [ ] Provider-change reconciliation completed at field level.
- [x] Unresolved pricing facts are represented explicitly as uncertainty in the current release candidate rather than being guessed.
- [ ] Final release CSV and JSON distributions represent the same provider states. (Current HOLD candidate parity exists; final release files do not yet exist.)
- [ ] Public files agree on all material states.
- [ ] Every material quantitative field is sourced or clearly derived.
- [x] Verification/check dates are present on every current release-candidate record; this does not mean every field is verified.
- [x] Commercial-rights uncertainty is preserved rather than simplified in the current candidate.
- [x] Source hierarchy is defined and the current candidate uses Tier A where current first-party evidence was successfully obtained; unresolved rows remain explicit.
- [ ] Derived metrics are reproducible from final released inputs. (Current HOLD-candidate metric derivation is reproducible.)
- [x] Relationship disclosures are populated and evidence-scoped for the current release candidate.
- [x] Methodology is included.
- [ ] Citation metadata is final-release valid. (`CITATION.cff` is pre-release safe; DOI/version are intentionally absent.)
- [ ] License or usage terms are final-deposit resolved. (Public terms and custom-Zenodo mapping are verified; actual Zenodo draft preview remains pending.)
- [ ] Immutable package can be regenerated from a known final source state.
- [ ] Prior releases remain retrievable.
- [ ] Public download is independent from the live buyer-facing site.

A failed gate means HOLD, not “publish now and fix later.”

## Production firewall

Production baseline **V70.7.5 remains frozen**. Repository, DOI, citation, methodology, research packaging and archival work do not authorize any production code change, deployment, DNS change, infrastructure change or live-data-model change.
