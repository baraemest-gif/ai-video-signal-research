-- BELORIE · Paco Perfumerías exact-match batch
-- Prepared: 2026-09-26
-- Safe/idempotent: resolves product + retailer by stable slug/domain.
-- No hard-coded D1 IDs. Does not alter catalogue cards or product copy.

BEGIN TRANSACTION;

-- 1) Carolina Herrera Good Girl EDP 80 ml
-- Paco product page verified 2026-09-26:
-- https://www.pacoperfumerias.com/good-girl-carolina-herrera-10572.html
-- Exact variant observed: Eau de Parfum para Mujer · 80 ml Vaporizador · EUR 94.95
INSERT INTO offers (
  product_id,
  retailer_id,
  merchant_product_url,
  affiliate_url,
  affiliate_verified,
  exact_match_status,
  price,
  currency,
  stock_status,
  shipping_text,
  source_type,
  source_ref,
  last_verified_at,
  updated_at
)
SELECT
  p.id,
  r.id,
  'https://www.pacoperfumerias.com/good-girl-carolina-herrera-10572.html',
  'https://www.awin1.com/cread.php?awinmid=21605&awinaffid=3005653&ued=https%3A%2F%2Fwww.pacoperfumerias.com%2Fgood-girl-carolina-herrera-10572.html',
  1,
  'verified',
  94.95,
  'EUR',
  'unknown',
  'Variante exacta verificada: Carolina Herrera Good Girl Eau de Parfum 80 ml. Precio observado 2026-09-26; disponibilidad final se confirma en Paco Perfumerías.',
  'paco_product_page',
  'paco_product_page:good-girl:80ml:2026-09-26',
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
FROM products p
JOIN retailers r ON lower(r.domain)=lower('pacoperfumerias.com')
WHERE p.slug='carolina-herrera-good-girl-edp'
LIMIT 1
ON CONFLICT(product_id,retailer_id) DO UPDATE SET
  merchant_product_url=excluded.merchant_product_url,
  affiliate_url=excluded.affiliate_url,
  affiliate_verified=1,
  exact_match_status='verified',
  price=excluded.price,
  currency=excluded.currency,
  stock_status=excluded.stock_status,
  shipping_text=excluded.shipping_text,
  source_type=excluded.source_type,
  source_ref=excluded.source_ref,
  last_verified_at=CURRENT_TIMESTAMP,
  updated_at=CURRENT_TIMESTAMP;

-- 2) Rabanne 1 Million EDT 100 ml
-- Paco product page verified 2026-09-26:
-- https://www.pacoperfumerias.com/one-million-paco-rabanne-5.html
-- Exact variant observed: Eau de Toilette para Hombre · 100 ml Vaporizador · EUR 72.95
INSERT INTO offers (
  product_id,
  retailer_id,
  merchant_product_url,
  affiliate_url,
  affiliate_verified,
  exact_match_status,
  price,
  currency,
  stock_status,
  shipping_text,
  source_type,
  source_ref,
  last_verified_at,
  updated_at
)
SELECT
  p.id,
  r.id,
  'https://www.pacoperfumerias.com/one-million-paco-rabanne-5.html',
  'https://www.awin1.com/cread.php?awinmid=21605&awinaffid=3005653&ued=https%3A%2F%2Fwww.pacoperfumerias.com%2Fone-million-paco-rabanne-5.html',
  1,
  'verified',
  72.95,
  'EUR',
  'unknown',
  'Variante exacta verificada: Rabanne 1 Million Eau de Toilette 100 ml. Precio observado 2026-09-26; disponibilidad final se confirma en Paco Perfumerías.',
  'paco_product_page',
  'paco_product_page:one-million:100ml:2026-09-26',
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
FROM products p
JOIN retailers r ON lower(r.domain)=lower('pacoperfumerias.com')
WHERE p.slug='rabanne-1-million-edt'
LIMIT 1
ON CONFLICT(product_id,retailer_id) DO UPDATE SET
  merchant_product_url=excluded.merchant_product_url,
  affiliate_url=excluded.affiliate_url,
  affiliate_verified=1,
  exact_match_status='verified',
  price=excluded.price,
  currency=excluded.currency,
  stock_status=excluded.stock_status,
  shipping_text=excluded.shipping_text,
  source_type=excluded.source_type,
  source_ref=excluded.source_ref,
  last_verified_at=CURRENT_TIMESTAMP,
  updated_at=CURRENT_TIMESTAMP;

COMMIT;

-- Post-run QA
SELECT p.slug, r.name AS retailer, o.price, o.currency, o.exact_match_status,
       o.affiliate_verified, o.merchant_product_url, o.affiliate_url,
       o.last_verified_at
FROM offers o
JOIN products p ON p.id=o.product_id
JOIN retailers r ON r.id=o.retailer_id
WHERE lower(r.domain)=lower('pacoperfumerias.com')
  AND p.slug IN ('carolina-herrera-good-girl-edp','rabanne-1-million-edt')
ORDER BY p.slug;
