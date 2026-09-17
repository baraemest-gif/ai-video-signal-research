# AI Video Pricing Market Snapshot — v2026.09.17

**AI Video Signal Research Dataset 2026**  
Version: `v2026.09.17`  
Publication date: `2026-09-17`  
DOI: `10.5281/zenodo.22816605`  
Persistent link: https://doi.org/10.5281/zenodo.22816605

## Executive summary

This brief summarizes the frozen `v2026.09.17` AI Video Signal research release. The underlying dataset covers **14 AI-video providers** and preserves dated evidence for provider pricing, credits and allowances, plan entitlements, free-access states, commercial-use evidence, relationship disclosures and documented market changes.

The release is designed as a **citable market-intelligence dataset**, not a visual-quality leaderboard and not a recommendation ranking.

## Reproducible pricing snapshot

For the frozen release:

- **11 normalized USD paid references** are included in the comparable monthly/monthly-equivalent price statistic.
- Median normalized paid reference: **$19/month or monthly-equivalent**.
- Range: **$6–$29**.
- Kling AI is excluded from the USD statistic because its directly verified current web pricing state is CNY-scoped.
- Google Veo is excluded from monthly-plan normalization because its verified evidence is endpoint-priced rather than a directly comparable monthly provider plan.

These values describe the **dated 2026-09-17 release only**. Provider pricing, credits, allowances and promotional offers may change after the verification date.

## Why the normalization is conservative

AI Video Signal does not silently convert or combine provider states that are not directly comparable. The methodology keeps distinctions visible when providers differ by:

- currency;
- billing interval;
- monthly plan versus endpoint/API pricing;
- credits versus minutes versus other allowances;
- model/workflow scope;
- resolution or duration constraints;
- ambiguous or conflicting first-party evidence.

Missing values are not treated as zero, no, unlimited or equivalent.

## Evidence model

The research uses a documented evidence hierarchy:

1. **Tier A** — first-party pricing, legal, documentation, help-center and official announcement sources.
2. **Tier B** — direct provider factual confirmation.
3. **Tier C** — reputable external reporting when first-party evidence is unavailable, ambiguous or historical.
4. **Tier D** — community or secondary leads used for discovery only, never as the sole evidence for a material field.

Provider fact-checking is used to improve factual accuracy but does not grant editorial veto.

## Commercial-use evidence

Commercial Rights Evidence Status (CRES) is an evidence classification, not legal advice and not a provider-quality score.

States:

- `documented_clear`
- `documented_conditional`
- `unclear`
- `restricted`
- `not_checked`

Marketing language alone is not treated as sufficient evidence for commercial-rights conclusions.

## Approved Output Cost

AI Video Signal defines Approved Output Cost (AOC) as:

`AOC = nominal generation cost × expected attempts per approved output`

If the number of attempts is not empirically measured, the value must be presented as a scenario or assumption rather than an observed production result.

## Release controls

The DOI-backed package includes or is supported by:

- machine-readable CSV and JSON distributions;
- methodology;
- data dictionary;
- evidence/source manifest;
- relationship-disclosure manifest;
- reproducibility instructions;
- release manifest;
- change history;
- cryptographic checksums;
- automated validation of CSV/JSON parity, evidence coverage and release metadata.

The published source state is preserved through the stable GitHub freeze pointer `published-v2026.09.17-freeze` and the Zenodo archival record.

## Limitations

This release does **not** claim:

- that the 14 providers represent the entire AI-video market;
- that documentation research is equivalent to hands-on visual-quality testing;
- that all provider prices are directly comparable;
- that the dataset establishes a universal quality ranking;
- that a DOI by itself establishes independent authority;
- that historical values remain current after the release date.

## Citation

Mestetef Ennaji, Y. (2026). *AI Video Signal Research Dataset 2026* (Version v2026.09.17) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.22816605

## Verification links

- DOI: https://doi.org/10.5281/zenodo.22816605
- Zenodo: https://zenodo.org/records/22816605
- Repository: https://github.com/baraemest-gif/ai-video-signal-research
- External citation kit: https://github.com/baraemest-gif/ai-video-signal-research/blob/main/outreach/CITATION_KIT.md
- Rights: https://aivideosignal.com/dataset-license/

## Contact

Research, factual corrections and citation questions: `partners@aivideosignal.com`
