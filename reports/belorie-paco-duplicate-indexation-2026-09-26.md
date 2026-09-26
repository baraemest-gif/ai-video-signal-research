# BELORIE — Paco duplicate/indexation findings — 2026-09-26

## Confirmed live duplicates in sitemap
Both imported Paco routes and curated BELORIE routes are present and indexable:

### Carolina Herrera Good Girl
- Imported: /producto/paco-10572
  - title: GOOD GIRL — CAROLINA HERRERA — BELORIE
  - generic description
  - no verified retailer section
  - robots: index,follow
- Curated: /producto/carolina-herrera-good-girl-edp
  - exact 80 ml variant
  - verified retailer section
  - stronger commercial metadata
  - robots: index,follow

### Rabanne 1 Million
- Imported: /producto/paco-5
  - title: 1 MILLION — RABANNE — BELORIE
  - generic description
  - no verified retailer section
  - robots: index,follow
- Curated: /producto/rabanne-1-million-edt
  - exact 100 ml variant
  - verified retailer section
  - stronger commercial metadata
  - robots: index,follow

Both duplicate pairs are currently listed in the live sitemap.

## Paco route health sample
10 representative Paco-imported sitemap routes sampled across the catalog.
Result:
- 10/10 valid current build
- 10/10 robots index,follow
- 10/10 build v4.9.6e-full-catalog-2026-09-25
- no sampled 404s

Conclusion:
Do NOT mass-remove Paco routes. The issue is duplicate intent / low comparator value, not a generally broken catalog.

## Safe consolidation rule
For an imported /producto/paco-* page:
1. If there is a curated BELORIE page for the same product/variant with verified retailer data:
   - imported route -> noindex,follow
   - remove imported route from sitemap
   - keep page accessible for internal catalog operations
   - optionally canonical to the curated URL only when the variant truly matches 1:1
2. If imported route is a real product with no curated equivalent:
   - keep accessible
   - index only after it gains verified comparator value under the monetization gate
3. Never mass-redirect imported pages to home/category.

## Two exact Paco matches verified today
### Good Girl EDP 80 ml
- Paco product: https://www.pacoperfumerias.com/good-girl-carolina-herrera-10572.html
- observed price: €94.95
- exact brand/product/type/size match

### Rabanne 1 Million EDT 100 ml
- Paco product: https://www.pacoperfumerias.com/one-million-paco-rabanne-5.html
- observed price: €72.95
- exact brand/product/type/size match

A safe SQL UPSERT file was prepared separately using retailer lookup by name rather than a hard-coded retailer_id.

## Deployment status
No production changes applied.
No separate BELORIE GitHub repository or Cloudflare workflow is connected.
Only repository currently available through GitHub connector:
- baraemest-gif/ai-video-signal-research

Therefore live BELORIE changes remain blocked until Cloudflare/remote/browser access returns or the current BELORIE source is connected.
