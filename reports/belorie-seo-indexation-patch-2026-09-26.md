# BELORIE SEO Indexation Patch — 2026-09-26

## Finding
Source audited:
BELORIE_CLOUDFLARE_READY.js

The Worker has 20 product routes in CATALOG and VALID_PATHS, and prerendered HTML links to those routes from the home and category pages.

However, both internal storefront structures currently:
1. mark every /producto/<slug> page as noindex,follow;
2. omit all product routes from SITEMAP_PATHS;
3. output generic WebSite schema, but no page-level Product/Breadcrumb schema.

This prevents BELORIE from using its real product catalog as an organic-search acquisition layer.

## Safe patch prepared
File:
BELORIE_CLOUDFLARE_READY_SEO_INDEXABLE_V1.js

The production Worker was NOT modified or deployed.

### Changes applied to BOTH internal structures
- Add all CATALOG product paths to SITEMAP_PATHS.
- Change valid product pages from noindex:true to noindex:false.
- Improve product meta descriptions to include:
  product name + brand + volume + comparison intent.
- Add page-level JSON-LD:
  WebPage
  Product
  BreadcrumbList
- Do NOT add Offer/price schema because BELORIE is a multi-retailer comparator and no verified price is embedded in the static CATALOG. No price is invented.
- Keep invalid routes noindex.
- Keep current canonical URL behavior.

## QA
- JavaScript syntax: PASS (node --check).
- 2/2 internal structures include catalog product URLs in sitemap: PASS.
- 2/2 product pageInfo blocks are indexable: PASS.
- 2/2 structures emit product JSON-LD graph: PASS.
- 0 old product noindex:true rules remain: PASS.
- Existing VALID_PATHS product routing preserved: PASS.
- No deployment performed: PASS.

## Expected SEO effect
The 20 existing product pages become crawlable/indexable candidates instead of intentionally excluded pages.
Examples include:
- Yves Saint Laurent Libre Eau de Parfum
- Lancôme La Vie Est Belle Eau de Parfum
- Narciso Rodriguez For Her Eau de Parfum
- Carolina Herrera Good Girl Eau de Parfum
- Rabanne 1 Million Eau de Toilette
- Estée Lauder Advanced Night Repair
- The Ordinary Niacinamide 10% + Zinc 1%
- Olaplex No.3 Hair Perfector
- Moroccanoil Treatment
- Color Wow Dream Coat

## Next production step
When Worker deployment access is available:
1. deploy this patch to a preview/non-production route first;
2. fetch /robots.txt, /sitemap.xml and 3 representative product pages;
3. verify 200 response, self-canonical, index,follow and valid JSON-LD;
4. verify no UI/affiliate behavior changed;
5. then promote to production;
6. submit/refresh sitemap in Search Console if the connected free GSC route supports it.

## Important
Do not add fake retailer prices or Offer schema until live offer data is verified.
Do not create separate duplicate SEO landing pages for the same product slugs.
