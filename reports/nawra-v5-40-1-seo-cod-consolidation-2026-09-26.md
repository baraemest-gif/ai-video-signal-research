# NAWRA v5.40.1 SEO COD Consolidation — 2026-09-26

## Source
User backup:
- nawra-store-backup.txt
- live/source health version found: v5.40.0-orderability-merchandising

Clean extracted baseline SHA-256:
- 77662bad6d38e863ba2bae903c5ae2900d9c93897d43aae220ec2926f9bf0084

Prepared patch:
- NAWRA_v5.40.1_SEO_COD_CONSOLIDATION_CLEAN.js
- SHA-256: 604b02ed60dd10809db5e7ce744407f67b14cb36b2fdac226ba482f7f9d064c4

## Evidence
GSC:
- /collections/cod-gulf: query "gulf cod", 3 impressions, avg position ~6.67
- /collections/cod-deals: 1 click / 5 impressions
- /collections/cod-network: no comparable GSC signal found
Source:
- cod-network and cod-deals contain the exact same four product handles.
- cod-gulf is the broad Gulf COD collection.

## Patch
1. Main "COD Ready" navigation now points to /collections/cod-gulf.
2. /collections page includes cod-gulf prominently while keeping featured-cod and cod-deals.
3. /collections/cod-network -> 301 /collections/cod-deals, preserving market/lang query state.
4. Legacy locale cod-network is consolidated one-hop to cod-deals.
5. cod-network is excluded from sitemap.
6. Health version bumped to 5.40.1-seo-cod-consolidation.
7. Market/language product variants remain in sitemap because the Worker intentionally varies product eligibility, local currency/pricing, language and hreflang by SA/AE/QA.

## Explicitly untouched
- D1 schema/data
- R2/images
- prices
- supplier offers
- checkout/order API
- checkout security/session controls
- product inventory
- affiliate links
- legal/privacy content
- market/lang canonical architecture
- DNS/SSL/Cloudflare settings

## QA
- node --check: PASS
- /health mocked request: PASS, version 5.40.1-seo-cod-consolidation
- /collections/cod-network?market=AE&lang=ar: PASS -> 301 https://nawrastore.com/collections/cod-deals?market=AE&lang=ar
- sitemap mock: PASS
  - cod-network absent
  - cod-gulf present
  - regional product variants retained

## Deployment
NOT deployed.
Wait for direct Cloudflare/authorized computer access.
Deploy only the file with SHA-256:
604b02ed60dd10809db5e7ce744407f67b14cb36b2fdac226ba482f7f9d064c4
