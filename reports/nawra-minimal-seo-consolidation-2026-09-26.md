# NAWRA — Minimal SEO Consolidation Patch — 2026-09-26

## Live production facts
Sitemap:
- 122 total URLs
- 52 clean/plain URLs
- 70 parameterized URLs
- 46 URLs with ?market=
- 47 URLs with ?lang=
- 23 URLs carrying both market and lang
- 30 base URLs duplicated by parameter variants
- some product bases appear up to 6 times

## COD collection audit
### /collections/cod-gulf
- 23 product links
- broad COD Gulf intent
- already the collection receiving Google visibility for "gulf cod" / "gulfcod"
- KEEP as primary broad COD collection

### /collections/featured-cod
- 4 verified COD products
- distinct curated subset
- KEEP, but position as a curated/featured subset rather than the main COD landing page

### /collections/cod-deals
- 1 product
- generic copy
- currently overlaps heavily with cod-network

### /collections/cod-network
- 1 product
- same product and effectively the same generic copy as cod-deals
- no meaningful unique search intent today

## Minimal production changes
1. Main navigation "COD Ready"
   -> link to /collections/cod-gulf

2. Keep /collections/featured-cod
   -> retain as a curated internal page
   -> title/H1 should stay focused on Featured COD Picks, not broad "Gulf COD"

3. /collections/cod-network
   -> 301 to /collections/cod-gulf unless a distinct future purpose is defined

4. /collections/cod-deals
   Short-term:
   -> noindex,follow and remove from sitemap while it contains only one product / duplicate copy
   OR 301 to /collections/cod-gulf if there is no planned deals-specific experience.
   Do not keep both cod-deals and cod-network indexable with the same content.

## Parameterized product URLs
Current sitemap publishes many combinations such as:
- ?market=AE
- ?market=AE&lang=ar
- other market/language combinations

Short-term safe fix:
- remove ALL query-parameter variants from sitemap
- sitemap should contain only clean canonical URLs
- keep parameters available for user-facing market/language state

Canonical rule:
- market-only variants that do not represent a separate SEO landing page -> canonical to clean product base
- do not self-canonicalize every market parameter

Arabic:
- Do NOT create thousands of query-parameter Arabic canonicals.
- If Arabic organic SEO is required, later create a stable clean locale structure (for example /ar/... or an equivalent maintained architecture) with hreflang.
- Until then, avoid putting ?lang=ar variants in the sitemap.

## Sitemap target
Current: 122 URLs
Immediate cleaned target: approximately the 52 clean URLs, minus any duplicate/thin collections that are noindexed/redirected.
Exact final count depends on whether cod-deals remains indexable.

## Why this is high impact
- concentrates link/relevance signals on clean URLs
- stops Google crawling multiple market/lang copies of the same product
- preserves market/language UX
- strengthens /collections/cod-gulf, which already has search visibility
- removes duplicate collection intent without deleting products

## Safety
- Active platform is Cloudflare.
- Do not modify old Shopify.
- Do not mass-redirect localized legacy URLs without 1:1 mapping.
- Do not alter product prices, D1/R2 or checkout/COD logic as part of this SEO patch.
