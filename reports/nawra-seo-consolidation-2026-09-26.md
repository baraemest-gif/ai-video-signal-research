# NAWRA SEO Consolidation Plan — 2026-09-26

## Evidence
Current public root:
https://nawrastore.com/
- New GCC-focused storefront.
- Home navigation includes "COD Ready".
- Saudi Arabia / UAE / Qatar market model.
- Current home shows verified COD products and affiliate partner cards.

Search/GSC evidence still surfaces older/localized paths such as:
- /en-ae/collections/cod-gulf
- /en-qa/
- /ar-ae/
- /ar-sa/policies/privacy-policy
- other localized collection/product/policy routes

The public domain therefore exposes multiple URL families and materially different storefront experiences.

## Key conflict
Root navigation "COD Ready" resolves toward:
- /collections/featured-cod

But GSC ranks:
- /collections/cod-gulf
for queries such as "gulf cod" / "gulfcod" around positions 6–7.

This splits internal and external relevance signals across two COD collection URLs.

## Priority 1 — choose one COD canonical
Recommended canonical commercial destination:
- keep ONE of /collections/featured-cod or /collections/cod-gulf

Decision rule:
- choose the URL that exists in the current Cloudflare storefront and can be maintained long term.
- if /collections/featured-cod is the new Cloudflare route, keep it and 301 old /collections/cod-gulf variants to it.
- if /collections/cod-gulf is the maintained route, change root navigation to point there and retire /collections/featured-cod.

Do not keep both indexable for the same intent.

## Priority 2 — localized legacy URLs
Inventory indexed families:
- /en-ae/*
- /en-qa/*
- /ar-ae/*
- /ar-sa/*
- any other market/language paths from the prior storefront

For each old URL:
A. If a true equivalent exists in the active Cloudflare store:
   -> 301 to the closest 1:1 equivalent.
B. If content is intentionally still active and unique:
   -> keep 200, self-canonical, and configure hreflang correctly.
C. If obsolete and no equivalent exists:
   -> 410 or remove from index; do NOT mass-redirect unrelated products to home.

## Priority 3 — policy/legal indexation
GSC has surfaced policy URLs for irrelevant searches.
Actions:
- keep legal pages accessible to users.
- avoid including policy pages in commercial sitemaps when not needed.
- use noindex on redundant localized legal duplicates if the active legal page is elsewhere.
- preserve one canonical version per required policy/language.

## Priority 4 — sitemap
The active sitemap should contain only:
- canonical market/category/product URLs
- useful informational pages
- required indexable language/market versions

Exclude:
- redirected URLs
- noindex URLs
- duplicated old Shopify/localized collections
- obsolete product URLs

## Priority 5 — internal links
All root navigation, product cards, breadcrumbs and market pages must link to the chosen canonical URL family.
No internal links should point to URLs that immediately redirect.

## Priority 6 — market/language structure
If market pages remain intentional:
- define a stable URL pattern.
- add hreflang pairs only between genuinely equivalent pages.
- do not create language-market combinations with empty or duplicate content.

## Measurement
After deployment monitor in GSC:
- "nawra"
- "gulf cod"
- "gulfcod"
- clicks/impressions for chosen COD canonical
- number of impressions landing on policy pages
- old localized URLs losing impressions as redirects/noindex are processed

## Safety
NAWRA active platform is Cloudflare.
Do not edit the old Shopify admin as a shortcut.
Do not deploy redirects until the Cloudflare route map is confirmed.
