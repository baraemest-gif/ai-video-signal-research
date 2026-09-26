# OMI'S OVEN — Home Internal-Link SEO Finding — 2026-09-26

## Verified
Stable source:
OMIS_OVEN_V9_1_GSC_PRODUCT_SCHEMA_FIX.js

- Product pages are server-rendered with canonical, Product/ItemPage schema and BreadcrumbList.
- Collection pages are server-rendered with CollectionPage/ItemList and direct product links.
- Sitemap contains product and collection URLs.
- The root homepage INDEX_HTML contains empty JS-driven:
  - #collectionGrid
  - #productGrid
- Raw homepage HTML currently has 0 /producto/ links and 0 /coleccion/ links before JS runs.

## Conclusion
This is not an indexing blocker because sitemap + SSR product/collection routes exist.
It is an internal-authority/discovery weakness on the homepage.

## Safe future improvement
Only when explicitly working on a V9.1-derived SEO release:
- server-render a small set of real collection/product anchors into the existing home grids;
- let the client JS hydrate/replace them after load;
- preserve identical CSS/classes so there is no design change;
- do not touch D1 schema, R2, checkout, WhatsApp, admin, SSL or DNS.

## Do not do now
- no deployment
- no redesign
- no new Worker version just for this issue
- no hidden-link block
- no duplicated product content

Priority remains low until GSC volume grows beyond the current minimal level.
