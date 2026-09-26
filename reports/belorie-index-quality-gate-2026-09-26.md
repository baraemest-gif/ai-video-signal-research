# BELORIE — Index Quality / Monetization Gate — 2026-09-26

## Production facts verified
Live build:
- v4.9.6e-full-catalog-2026-09-25
- Domain: https://belorie.es

Live sitemap:
- Total URLs: 6,611
- Product URLs: 6,593
- Non-product URLs: 18
- Product source families:
  - Paco imports: 4,657
  - La Droguería imports: 1,838
  - Loewe named products: 14
  - Other curated/named products: 84

Verified commercial coverage:
- /ofertas currently links to 79 unique product pages with at least one verified retailer match.
- 96 retailer/product match rows are shown because some products have more than one verified retailer.

## Critical conclusion
The sitemap exposes thousands of product pages before they have comparator value.
Most imported product pages are real products, but many do not yet show a verified retailer/offer block.

For BELORIE's business model, this is a quality and monetization mismatch:
- indexable inventory is far larger than monetizable inventory;
- pages without verified offers add crawl/index load without giving the user the core comparison value;
- merchant-sourced descriptions may be relatively thin/duplicative when no BELORIE comparison data is present.

## Production rule to implement
### Tier A — indexable + sitemap
A product page should be indexable when it has at least one verified commercial match:
- verified retailer identity
- exact product/variant match
- affiliate/tracking URL when approved and available
- product title/brand/variant metadata
- canonical self URL

Tier A pages:
- meta robots: index,follow
- included in sitemap
- linked from relevant category/brand pages

### Tier B — accessible but not indexable yet
Products imported into the catalog but without a verified retailer match:
- remain browsable inside BELORIE
- meta robots: noindex,follow
- excluded from sitemap
- can still be linked internally so discovery/UX is preserved
- automatically promoted to Tier A when a verified offer is added

Do NOT delete these products and do NOT mass-redirect them.

## Sitemap logic
Instead of:
CATALOG.map(product => product URL)

Use a monetization/indexability predicate, conceptually:
indexableProducts = CATALOG.filter(product => hasVerifiedCommercialMatch(product))

SITEMAP_PATHS = editorial/category URLs + indexableProducts URLs

## Product page logic
For /producto/<slug>:
- if product exists AND hasVerifiedCommercialMatch(product):
  index,follow
- if product exists BUT has no verified commercial match:
  noindex,follow
- invalid product:
  404 + noindex

## Why this is safer
This keeps the full catalog for users and matching automation while limiting Google's first crawl/index wave to pages where BELORIE already provides differentiated comparator value.

## Current priority set
Start with the 79 verified products already exposed by /ofertas.
These should receive:
1. clean self-canonical
2. product/variant-specific title
3. useful meta description
4. Product + Breadcrumb structured data when technically present/validated
5. category and brand internal links
6. at least one verified retailer CTA
7. affiliate disclosure

## Do not do
- Do not delete the 6,500+ unmatched products.
- Do not redirect unmatched products to category/home.
- Do not invent prices or stock.
- Do not add fake Offer schema.
- Do not submit all 6,593 products for aggressive indexing until comparator coverage increases.

## Next growth loop
Imported product
-> exact retailer matching
-> affiliate URL verification
-> offer becomes active
-> product becomes Tier A
-> sitemap inclusion
-> index,follow
-> internal links
-> Search Console monitoring
