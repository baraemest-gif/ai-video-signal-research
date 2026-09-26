-- BELORIE · Paco import index-quality diagnostic
-- Prepared 2026-09-26
-- READ ONLY. No data changes.

SELECT
  COUNT(*) AS paco_import_products,
  SUM(CASE WHEN EXISTS (
    SELECT 1 FROM offers o
    WHERE o.product_id = p.id
      AND o.exact_match_status = 'verified'
      AND o.affiliate_verified = 1
  ) THEN 1 ELSE 0 END) AS with_verified_offer,
  SUM(CASE WHEN NOT EXISTS (
    SELECT 1 FROM offers o
    WHERE o.product_id = p.id
      AND o.exact_match_status = 'verified'
      AND o.affiliate_verified = 1
  ) THEN 1 ELSE 0 END) AS without_verified_offer
FROM products p
WHERE p.slug LIKE 'paco-%';

SELECT p.id,p.slug,p.brand,p.name,p.ean_gtin
FROM products p
WHERE p.slug LIKE 'paco-%'
  AND NOT EXISTS (
    SELECT 1 FROM offers o
    WHERE o.product_id=p.id
      AND o.exact_match_status='verified'
      AND o.affiliate_verified=1
  )
ORDER BY p.id
LIMIT 500;

SELECT p.id,p.slug,p.brand,p.name,r.name AS retailer,o.price,o.currency,o.last_verified_at
FROM products p
JOIN offers o ON o.product_id=p.id
JOIN retailers r ON r.id=o.retailer_id
WHERE p.slug LIKE 'paco-%'
  AND o.exact_match_status='verified'
  AND o.affiliate_verified=1
ORDER BY p.id
LIMIT 500;

SELECT id,slug,brand,name,ean_gtin
FROM products
WHERE slug IN ('paco-10572','carolina-herrera-good-girl-edp','paco-5','rabanne-1-million-edt')
ORDER BY brand,name,slug;

SELECT
  a.id AS imported_id,a.slug AS imported_slug,a.brand AS imported_brand,a.name AS imported_name,
  b.id AS curated_id,b.slug AS curated_slug,b.brand AS curated_brand,b.name AS curated_name
FROM products a
JOIN products b
  ON a.id<>b.id
 AND lower(trim(a.brand))=lower(trim(b.brand))
 AND lower(trim(a.name))=lower(trim(b.name))
WHERE a.slug LIKE 'paco-%'
  AND b.slug NOT LIKE 'paco-%'
ORDER BY a.brand,a.name
LIMIT 500;
