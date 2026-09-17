# Release Status

## STATUS: HOLD — READY FOR FREEZE ENGINEERING

The current research candidate has passed provider reconciliation and pre-freeze technical validation. The first DOI-backed release must **not** be published until the remaining final-release and Zenodo gates pass.

## Resolved / evidenced validations

- [x] **Pictory pricing-source protocol confirmed.** Use Pictory's current live Pricing page as source of truth, record the verification date and do not treat email figures as permanent plan entitlements.
- [x] **Google Search Console discoverability verified.** Finalized period 2026-08-18 through 2026-09-14 recorded 9,142 impressions and 14 clicks for `https://aivideosignal.com/`; the research dataset page also received impressions.
- [x] **Provider identity set fixed at 14 providers.**
- [x] **Provider-change reconciliation completed at field level for the current HOLD candidate.** No provider requires a guessed current value.
- [x] **Reconciliation support CSV/JSON parity established.**
- [x] **14-provider HOLD release candidate created in CSV and JSON.** Candidate ID: `RC-2026-09-17-HOLD`.
- [x] **InVideo AI and Pika current changes propagated without overwriting historical snapshots.**
- [x] **Vizard current dynamic pricing resolved.** Creator is verified at $29/month with 600 credits/month; yearly starting tier $14.50/month billed $174/year with 7,200 credits/year; Free remains $0 with 60 credits/month.
- [x] **Submagic current free-entry state resolved.** Starter $19/month remains supported; official first-party material confirms limited free entry via one free video/post, no card, with trial watermarking.
- [x] **Hypernatural free-access state scoped.** Official plan-specific support explicitly states no free plan and no free trial. Generic `Start for free` CTA is not treated as evidence of a plan entitlement.
- [x] **Kling AI current public web pricing resolved.** Public first-party membership UI verifies Gold Member (黄金会员) at ¥58/month renewal, ¥46 first month after a ¥5.99/7-day new-customer trial, with 660 Inspiration Credits/month. The evidence is scoped to public CNY web pricing and is not silently converted to USD.
- [x] **Hailuo AI cadence discrepancy resolved.** Subscription Service Terms list Standard at $14.99/month with 1,000 credits. Current public pricing UI shows annual billing at $8.40/month equivalent, billed $100.80/year, with the same 1,000 credits/month. Older $6.99/$9.99 official marketing references are retained as historical/unscoped evidence and are not promoted as current pricing.
- [x] **Relationship disclosures populated from evidence-scoped connected-mail review.** Confirmed commercial relationships are disclosed; application/inquiry-only states are not promoted to confirmed relationships.
- [x] **Automated research validation enabled.** GitHub Actions validates provider reconciliation, release-candidate parity, source-manifest coverage, relationship disclosures, quantitative evidence coverage, metadata, pre-freeze readiness, HOLD safety, metrics and package reconstruction.
- [x] **Material quantitative coverage validated for the current candidate.** Populated price/credit/cost fields require source URL, evidence tier and check date; numeric paid prices require currency and billing context; any future AOC value must carry nominal cost plus retry/assumption inputs.
- [x] **Pre-freeze readiness validated.** The current 14-provider candidate is `READY_FOR_FREEZE_ENGINEERING` while publication remains unauthorized.
- [x] **Metadata preflight and release safety guard enabled.** CI validates `CITATION.cff`, the inert Zenodo custom-rights template, absence of an active `.zenodo.json`, manifest HOLD semantics, null DOI/ORCID and `publication_authorized=false` while status is HOLD.
- [x] **Candidate metric derivation reproducible.** The current HOLD candidate has 11 normalized USD paid references. Kling's CNY web price is intentionally excluded from the USD-only statistic rather than converted silently. The derived USD median is $19/month with a $6–$29 range.
- [x] **Reproducible HOLD package construction validated.** CI rebuilds the candidate package from repository source files, generates a machine-readable package manifest plus SHA-256 checksums, and independently validates every packaged file/hash. This proves candidate-package reconstruction; it is not yet the final immutable DOI release.
- [x] **Public Dataset License & Usage Terms verified.** Canonical terms: `https://aivideosignal.com/dataset-license/`, effective 2026-08-31.
- [x] **Zenodo rights path mapped.** Use a custom AI Video Signal rights statement rather than silently accepting a broader default license.
- [x] **Zenodo pre-publish worksheet prepared.** `release-candidate/ZENODO_DEPOSIT_FIELDS.md` contains the title, creator, description, keywords, related identifier, custom rights statement, file list and final publish checks without inventing DOI, ORCID, version or publication date.
- [x] **DOI release playbook prepared.** `release-candidate/RELEASE_PLAYBOOK.md` defines the exact freeze, validation, GitHub release, Zenodo and post-DOI sequence while preserving the Production firewall.
- [x] **Freeze-readiness record created.** `release-candidate/FREEZE_READINESS.md` records passed gates and explicitly keeps publication on HOLD.

## Provider reconciliation status

**No provider-level blocker remains open.**

Scoped but non-comparable states are intentional research decisions, not unresolved errors:

- **Kling AI:** exact current public CNY web pricing is retained as CNY and excluded from USD-normalized price statistics.
- **Google Veo:** endpoint economics are retained without inventing a comparable monthly subscription.

## Remaining release issues

- Create the **final frozen** release CSV/JSON distributions from the validated candidate.
- Generate final release-specific package manifest and SHA-256 checksums from the frozen state.
- Insert the final immutable version and publication date consistently into citation metadata only after the freeze.
- Enter and preview the verified custom reuse terms in the actual Zenodo draft before publication authorization.
- Reconcile final public-release files with the frozen package.
- Keep CI green on the exact frozen commit.
- Only then change publication authorization and publish through GitHub/Zenodo; record only the DOI actually assigned by Zenodo.

## Mandatory release gates

- [x] Current candidate provider count reconciled at 14/14.
- [x] Provider-change reconciliation completed at field level for the current candidate.
- [x] No current provider value is guessed; scope limitations are explicit.
- [x] Current candidate CSV/JSON parity exact and automated.
- [x] Material quantitative fields in the current candidate are sourced/date-scoped or explicitly derived.
- [x] Current candidate records carry verification/check dates.
- [x] Commercial-rights uncertainty is preserved.
- [x] Source hierarchy is enforced.
- [x] Current candidate metrics are reproducible from candidate inputs.
- [x] Relationship disclosures populated and evidence-scoped for the current candidate.
- [x] Methodology included.
- [x] Pre-release citation/Zenodo metadata validated while HOLD; final version/date/DOI remain intentionally absent.
- [x] Current HOLD package can be reconstructed and checksum-validated from a known repository state.
- [ ] **Final frozen** release CSV/JSON distributions created and parity-validated.
- [ ] **Final frozen** release package manifest/checksums generated and verified.
- [ ] Citation metadata final-release version/date valid.
- [ ] License/usage terms verified in the actual Zenodo draft preview.
- [ ] Public release files agree on all material final states.
- [ ] Prior releases remain retrievable after publication/versioning begins.
- [ ] Public download independent from the live buyer-facing site.

A failed final gate means HOLD, not “publish now and fix later.”

## Production firewall

Production baseline **V70.7.5 remains frozen**. Research packaging, DOI preparation, citation metadata and archival work do not authorize any production code, deployment, DNS, infrastructure or live-data-model change.
