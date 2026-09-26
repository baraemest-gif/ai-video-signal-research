# BELORIE — Production SEO audit 2026-09-26

## Live production verified
Domain: https://belorie.es
Build marker observed on live pages:
v4.9.6e-full-catalog-2026-09-25

## Sitemap
Live sitemap contains:
- 6,611 URLs total
- 6,593 product URLs
- 18 non-product/public SEO URLs

Product URL families:
- 4,657 paco-* product routes
- 1,838 lad-* product routes
- 14 loewe-* curated routes
- 84 other curated/descriptive product routes

The sitemap is below the 50,000-URL sitemap limit, so splitting is not technically required at the current size.

## Product-page indexability
Representative live pages tested:
- /producto/loewe-001-man-edp
- /producto/loewe-001-woman-edp
- /producto/loewe-7-cobalt-edp
- /producto/lad-309970039738
- /producto/lad-309970107925

All tested pages:
- return usable product content
- have self-canonical URLs
- are robots index,follow
- have unique product titles
- expose product/brand information
- include retailer information where a verified commercial match exists

Do NOT mass-delete lad-* or paco-* URLs just because their slug is numeric/source-derived. Samples are real product pages.

## Variant architecture
Tested:
Good Girl EDP 30/50/80 ml
La Vie Est Belle EDP 30/50/75/100 ml

Observed:
- each size has a distinct self-canonical
- titles include the exact size
- pages link to other verified sizes
- product images differ by variant where available

Recommendation:
Keep size variants indexable for now. Do not canonicalize all sizes to one master URL without evidence from search performance.

## Major SEO opportunity — brand hubs
Current /marcas page is indexable but there are no dedicated brand routes.
Verified 404:
- /marca/loewe
- /marcas/loewe
- /loewe

LOEWE already has 14 product routes and commercial matches, so a dedicated brand hub is a strong internal-linking and search-intent opportunity.

Proposed future route:
- /marca/loewe

Proposed title:
LOEWE Perfumes: hombre y mujer — Comparar productos | BELORIE

Proposed H1:
Perfumes LOEWE

Page should:
- list the 14 verified LOEWE products
- separate clearly masculine/feminine/unisex only when product data supports it
- link each card to the existing canonical product page
- explain that prices/availability are confirmed at retailer destination
- link to /perfumeria and /marcas
- be index,follow
- be added to sitemap
- have self-canonical
- avoid duplicating retailer descriptions verbatim

## Search visibility
Public-search spot checks on 2026-09-26 returned no BELORIE result for:
- site:belorie.es "001 Man Edp"
- site:belorie.es "Colorstay Full Cover Base 150 Buff"
- site:belorie.es "Libre Eau de Parfum" BELORIE
- site:belorie.es "La Vie Est Belle" BELORIE
- site:belorie.es "Cicaplast Baume B5+" BELORIE

Interpretation:
The catalog expansion is extremely recent (lastmod 2026-09-24/25). Absence in these spot checks is not proof of a technical indexing failure. It does show that publication and search visibility are not yet equivalent.

## Important risk
Thousands of pages were added in roughly 24-48 hours. The main risk is not sitemap size; it is thin/merchant-derived content and weak internal topical structure.

Do not:
- remove thousands of pages blindly
- add invented prices
- add fake availability
- create duplicate landing pages per retailer
- redirect size variants without performance evidence

## Next production changes when current Worker source is recovered
P1
1. Add dedicated brand hubs beginning with LOEWE.
2. Ensure all major brands are linked from /marcas rather than rendered as plain text only.
3. Add contextual internal links from category pages to brand hubs.
4. Preserve product self-canonicals and verified retailer matching.

P2
5. Expand unique on-page copy for high-value product families, especially where multiple size pages currently reuse one short description.
6. Add descriptive breadcrumbs and product-family navigation where not already present.
7. Verify Product/Breadcrumb structured data in the actual v4.9.6e source before changing schema.

P3
8. Monitor whether paco-* and lad-* pages begin receiving impressions; only prune/noindex low-value families after performance evidence.

## Access state
- Current v4.9.6e Worker source was not found in ChatGPT Library.
- Current v4.9.6e Worker source was not found in the connected GitHub repository.
- Remote Desktop device is currently offline.
- Opera Browser Connector is currently disconnected.
- No paid Ahrefs/API credits were used.
