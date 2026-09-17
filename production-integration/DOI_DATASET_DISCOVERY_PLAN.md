# AI Video Signal — DOI + Dataset Discovery Integration Plan

Status: **PREPARED — NOT DEPLOYED**

Production baseline: **V70.7.5 — FROZEN**

This document defines the minimum production-facing changes required to expose the DOI-backed research release to search engines, journalists and researchers. It does **not** authorize deployment or any modification to the live application.

## Release identity

- Dataset: **AI Video Signal Research Dataset 2026**
- Version: **v2026.09.17**
- DOI: **10.5281/zenodo.22816605**
- DOI URL: https://doi.org/10.5281/zenodo.22816605
- Zenodo record: https://zenodo.org/records/22816605
- Repository: https://github.com/baraemest-gif/ai-video-signal-research
- Creator: **Youssef Mestetef Ennaji**
- Publication date: **2026-09-17**
- Resource type: **Dataset**
- Rights: **AI Video Signal Dataset Rights & Reuse Terms**

## Minimum future production changes

Only after separate explicit authorization:

1. Add a visible DOI citation block to the canonical AI Video Signal research / Press & Data page.
2. Link the DOI using the persistent DOI URL, not only the mutable live-site URL.
3. Link the immutable Zenodo record as the archival download source.
4. Expose the prepared Dataset JSON-LD from `metadata/dataset.schema.jsonld` after validating every live URL and distribution reference.
5. Add links to the public GitHub research repository and citation kit.
6. Preserve the live commercial site and research dataset as separate roles; the DOI identifies the immutable research release.
7. Add the canonical research page to the sitemap only if that page is already an approved production route.
8. Validate structured data after deployment and record the exact deployment/version that introduced it.

## Required Dataset structured-data checks

Before any deployment, verify that the live JSON-LD contains only true, publicly resolvable values:

- `@type`: `Dataset`
- `name`
- `description`
- `creator`
- `publisher`
- `datePublished`
- `dateModified`
- `version`
- `identifier` / DOI
- `sameAs` or persistent archival reference where appropriate
- `license` or rights URL only when it accurately describes the published terms
- `distribution` only for genuinely public, stable downloads
- `citation`
- `keywords`
- temporal coverage only if explicitly supported

Do not claim distributions, licenses, identifiers or availability states that do not exist publicly.

## Research-page copy requirements

The future public research page should make these distinctions explicit:

- the dataset is versioned and date-scoped;
- current provider values may change after the release date;
- 14 providers are included in this release but do not represent the entire market;
- documentation research is not presented as hands-on quality testing;
- CRES is evidence classification, not legal advice or a quality score;
- provider fact-checks improve factual accuracy but do not confer editorial veto;
- affiliate/commercial relationships do not change evidence status;
- the DOI identifies an immutable archival release.

## Search Console verification after deployment

After an authorized deployment:

1. inspect the canonical research URL in Google Search Console;
2. verify canonical selection and crawl status;
3. validate Dataset structured data;
4. confirm sitemap discovery;
5. monitor query and page impressions without treating impressions as independent authority;
6. record the first indexed date and subsequent material search changes.

## Hard production firewall

This plan must **not** be interpreted as permission to:

- deploy new production code;
- alter V70.7.5;
- change Cloudflare DNS or SSL/TLS;
- change D1 or R2;
- alter payment or affiliate systems;
- modify live provider data;
- replace or rewrite the DOI-backed frozen release.

Any live-site implementation requires a separate explicit production authorization and a reversible deployment plan.
