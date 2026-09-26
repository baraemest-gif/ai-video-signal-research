# Store Growth Execution — 2026-09-26

## Objective
Increase qualified traffic, conversion and sales across active stores without paid spend unless explicitly approved.

## Current priority order
1. AI Video Signal
2. Yontorix
3. NAWRA
4. JoyPrint17
5. OMI'S OVEN
6. Other active projects

## AI Video Signal
Search Console range: 2026-08-27 to 2026-09-23.
- 11,895 impressions / 20 clicks.
- /best-ai-video-generators/ has 2,148 impressions and low CTR overall, but the global average position is ~55.5.
- Query "ai video generator price comparison" is the useful exception at ~position 4.5.
- Compliance page is already more advanced in production than the earlier patch plan: LMS, lifecycle, audit-readiness, versioning and internal links are live.
- Do not rewrite pages from an older package.
- Minimal price-comparison internal-link patch is documented at reports/aivs-price-comparison-internal-links-2026-09-26.md.

## Yontorix
Search Console range: 2026-08-27 to 2026-09-23.
- 5,346 impressions / 76 clicks.
- Several product pages already rank around positions 6–11.

### Channel evidence
Facebook historical posts (Sep 11–16):
- only ~1–4 impressions per post
- 0 link clicks
Conclusion: Facebook text/link distribution is currently weak.

Instagram historical posts:
- roughly 3–8 views/reach per post
- 0 meaningful interactions
Conclusion: Instagram distribution is currently weak.

TikTok historical posts:
- 268 to 809 views per post
- 250 to 752 reach
- almost all views from For You
- 0 likes/comments/shares in the sample
Conclusion: TikTok is the only connected social channel currently providing meaningful organic distribution, but creative quality/engagement must improve.

### Facebook organic tests already scheduled
1. 2026-09-28 10:00 — Varsity Pop handbag
2. 2026-09-30 12:00 — Paekole Open Ear 80H / ENC / IPX7
3. 2026-10-02 10:00 — Citizen FRA59-2432
4. 2026-10-05 10:00 — Batana Oil 100 ml
5. 2026-10-07 12:00 — OFRA Bellini Blush

All:
- organic
- UTM tagged
- no paid boost
- affiliate disclosure included

### TikTok visual tests scheduled
1. 2026-10-07 10:00 — Batana Oil 100 ml
   - real Yontorix/eBay product image
   - UTM source=tiktok
   - commercial content disclosures enabled
2. 2026-10-08 10:00 — OFRA Cosmetics Bellini Blush
   - real Yontorix/eBay product image
   - UTM source=tiktok
   - commercial content disclosures enabled

Do not add many more social tests until these produce comparative data.

## NAWRA
Live sitemap audit:
- 122 URLs
- 70 parameterized market/language URLs
- 30 duplicated base URLs
- some product bases appear up to 6 times
- /collections/cod-gulf has 23 products and current search visibility
- /collections/featured-cod has 4 products and can remain a curated subset
- cod-deals and cod-network overlap heavily

Minimal consolidation plan:
reports/nawra-minimal-seo-consolidation-2026-09-26.md

Active platform is Cloudflare. Do not modify old Shopify.

## BELORIE
Live build verified:
- v4.9.6e-full-catalog-2026-09-25
- 6,611 sitemap URLs
- 6,593 product URLs
- 79 unique product pages currently have at least one verified commercial retailer match on /ofertas

Index-quality rule documented:
reports/belorie-index-quality-gate-2026-09-26.md

Do not delete imported products.
Prioritize indexation/sitemap inclusion for pages with verified comparator value.

## JoyPrint17 / Etsy
Five live listings confirmed:
- Window Cleaning Business Forms Bundle — 4581934116
- Junk Removal Business Forms Bundle — 4581923768
- Handyman Business Forms Bundle — 4581841815
- Lawn Care Business Forms Bundle — 4581829241
- Pressure Washing Ultimate Business Bundle — 4572422453

Safe SEO optimizer created:
joyprint17/etsy-publisher/optimize_live_listings.py

Scope:
- existing active IDs only
- title + 13 tags only
- no price/image/file/state/quantity changes
- no listing creation

Execution result:
- workflow triggered correctly
- Etsy OAuth refresh failed with invalid_grant
- public Etsy verification showed titles remained unchanged
- therefore no accidental listing modifications occurred

Next requirement:
renew Etsy OAuth authorization before rerunning.

## OMI'S OVEN
- product and collection pages are indexable
- V9.1 source has Product/ItemPage, BreadcrumbList, CollectionPage/ItemList, clean canonical and dynamic sitemap
- public search already discovers some individual product/category pages
- do not disturb stable V9.x infrastructure without a justified change

## Measurement rules
- Every social test uses UTM parameters.
- Separate brands by channel.
- Prefer pages already ranking positions 6–20 before creating large volumes of new content.
- Track impressions -> clicks -> product/affiliate click -> sale where possible.
- Do not pay for ads or marketplace publication fees without explicit approval.
- Do not continue scaling a channel that shows no distribution without changing creative or format first.
