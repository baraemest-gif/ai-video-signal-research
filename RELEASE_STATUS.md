# Release Status

## STATUS: HOLD — PRE-DOI RESEARCH HARDENING

The first DOI-backed release must not be published until every mandatory gate below passes.

## Resolved / evidenced validations

- [x] **Pictory pricing-source protocol confirmed.** Use Pictory's current live Pricing page as source of truth, record the verification date and do not treat email figures as permanent plan entitlements.
- [x] **Google Search Console discoverability verified.** Finalized period 2026-08-18 through 2026-09-14 recorded 9,142 impressions and 14 clicks for `https://aivideosignal.com/`; the research dataset page also received impressions.
- [x] **Provider identity set fixed at 14 providers.**
- [x] **Reconciliation support CSV/JSON parity established.**
- [x] **14-provider HOLD release candidate created in CSV and JSON.** Candidate ID: `RC-2026-09-17-HOLD`.
- [x] **InVideo AI and Pika current changes propagated without overwriting historical snapshots.**
- [x] **Vizard current dynamic pricing resolved.** Creator is verified at $29/month with 600 credits/month; yearly starting tier $14.50/month billed $174/year with 7,200 credits/year; Free remains $0 with 60 credits/month.
- [x] **Submagic current free-entry state resolved.** Starter $19/month remains supported; official first-party material confirms limited free entry via one free video/post, no card, with trial watermarking.
- [x] **Hypernatural free-access state scoped.** Official plan-specific support explicitly states no free plan and no free trial. Generic `Start for free` CTA is not treated as evidence of a plan entitlement.
- [x] **Kling AI current public web pricing resolved.** Public first-party membership UI verifies Gold Member (黄金会员) at ¥58/month renewal, ¥46 first month after a ¥5.99/7-day new-customer trial, with 660 Inspiration Credits/month. The evidence is scoped to public CNY web pricing and is not silently converted to USD.
- [x] **Relationship disclosures populated from evidence-scoped connected-mail review.** Confirmed commercial relationships are disclosed; application/inquiry-only states are not promoted to confirmed relationships.
- [x] **Automated research validation enabled.** GitHub Actions validates reconciliation parity, release-candidate parity, source-manifest coverage, relationship-disclosure consistency and candidate metric derivation.
- [x] **Metadata preflight and release safety guard enabled.** CI validates `CITATION.cff`, the inert Zenodo custom-rights template, absence of an active `.zenodo.json`, manifest HOLD semantics, null DOI/ORCID and `publication_authorized=false` while status is HOLD.
- [x] **Full CI passes on the current pre-DOI state.** Reconciliation, release-candidate parity, evidence coverage, disclosures, citation/Zenodo metadata, HOLD guard and candidate metric derivation all complete successfully.
- [x] **Candidate metric derivation reproducible.** Current HOLD candidate has 10 normalized USD paid references, median $19.50/month or monthly-equivalent, range $6–$29. Kling's CNY web price is intentionally excluded from that USD-only statistic rather than converted silently.
- [x] **Public Dataset License & Usage Terms verified.** Canonical terms: `https://aivideosignal.com/dataset-license/`, effective 2026-08-31.
- [x] **Zenodo rights path mapped.** Use a custom AI Video Signal rights statement rather than silently accepting a broader default license.
- [x] **Zenodo pre-publish worksheet prepared.** `release-candidate/ZENODO_DEPOSIT_FIELDS.md` contains the title, creator, description, keywords, related identifier, custom rights statement, file list and final publish checks without inventing DOI, ORCID, version or publication date.
- [x] **DOI release playbook prepared.** `release-candidate/RELEASE_PLAYBOOK.md` defines the exact freeze, validation, GitHub release, Zenodo and post-DOI sequence while preserving the Production firewall.

## Open provider reconciliation issue

Only **one provider-level blocker** remains:

- **Hailuo AI:** current first-party pricing conflict. Subscription Service Terms list Standard at $14.99/month with 1,000 credits, while separate official Hailuo pages list Standard at $6.99 or $9.99. No single current normalized paid price is selected.

Google Veo is intentionally endpoint-priced and remains `not_normalized` as a monthly subscription; this is a modeling decision, not an unresolved provider error.

## Other open release issues

- Latest CI must remain green after any material candidate change.
- The custom reuse terms must be entered and previewed in the actual Zenodo draft before final publication authorization.
- Active `.zenodo.json` remains intentionally disabled while status is HOLD.
- Final citation metadata still needs final version, publication date and DOI only after the release is frozen.
- Final release manifest/checksums must be generated from the frozen final candidate.
- Public buyer-facing research files are not regenerated while Production **V70.7.5** remains frozen.

## Mandatory release gates

- [ ] Provider count reconciled across all **final** release files.
- [ ] Provider-change reconciliation completed at field level. (**Hailuo remains.**)
- [x] Unresolved pricing facts are explicitly represented rather than guessed.
- [ ] Final release CSV/JSON parity. (Current HOLD candidate parity is automated; final frozen files do not yet exist.)
- [ ] Public files agree on all material final states.
- [ ] Every material quantitative field is sourced or clearly derived in the final package.
- [x] Current candidate records carry verification/check dates.
- [x] Commercial-rights uncertainty is preserved.
- [x] Source hierarchy is enforced.
- [ ] Derived metrics reproducible from **final released inputs**. (Current candidate derivation is reproducible.)
- [x] Relationship disclosures populated and evidence-scoped for the current candidate.
- [x] Methodology included.
- [x] Pre-release citation/Zenodo metadata validated while HOLD; final version/date/DOI remain intentionally absent.
- [ ] Citation metadata final-release valid.
- [ ] License/usage terms final-deposit verified in Zenodo preview.
- [ ] Immutable package reproducible from a frozen final source state.
- [ ] Prior releases remain retrievable after publication/versioning begins.
- [ ] Public download independent from the live buyer-facing site.

A failed gate means HOLD, not “publish now and fix later.”

## Production firewall

Production baseline **V70.7.5 remains frozen**. Research packaging, DOI preparation, citation metadata and archival work do not authorize any production code, deployment, DNS, infrastructure or live-data-model change.
