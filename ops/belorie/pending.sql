INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  66,10,
  'https://www.notino.es/loewe/7-cobalt-eau-de-parfum-para-hombre/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Floewe%2F7-cobalt-eau-de-parfum-para-hombre%2F',
  1,'verified','LOW00965',126.00,'EUR','in_stock',
  'Exact product and format: LOEWE 7 Cobalt Eau de Parfum 100 ml',
  'manual','notino:exact:LOW00965:2026-09-25',
  CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
)
ON CONFLICT(product_id,retailer_id) DO UPDATE SET
  merchant_product_url=excluded.merchant_product_url,
  affiliate_url=excluded.affiliate_url,
  affiliate_verified=1,
  exact_match_status='verified',
  retailer_sku=excluded.retailer_sku,
  price=excluded.price,
  currency=excluded.currency,
  stock_status=excluded.stock_status,
  shipping_text=excluded.shipping_text,
  source_type=excluded.source_type,
  source_ref=excluded.source_ref,
  last_verified_at=CURRENT_TIMESTAMP,
  updated_at=CURRENT_TIMESTAMP;

INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  71,10,
  'https://www.notino.es/loewe/loewe-7-for-men-eau-de-toilette-para-hombre/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Floewe%2Floewe-7-for-men-eau-de-toilette-para-hombre%2F',
  1,'verified','LOW0172',126.00,'EUR','in_stock',
  'Exact product and format: LOEWE 7 Eau de Toilette 100 ml',
  'manual','notino:exact:LOW0172:2026-09-25',
  CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
)
ON CONFLICT(product_id,retailer_id) DO UPDATE SET
  merchant_product_url=excluded.merchant_product_url,
  affiliate_url=excluded.affiliate_url,
  affiliate_verified=1,
  exact_match_status='verified',
  retailer_sku=excluded.retailer_sku,
  price=excluded.price,
  currency=excluded.currency,
  stock_status=excluded.stock_status,
  shipping_text=excluded.shipping_text,
  source_type=excluded.source_type,
  source_ref=excluded.source_ref,
  last_verified_at=CURRENT_TIMESTAMP,
  updated_at=CURRENT_TIMESTAMP;

INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  68,10,
  'https://www.notino.es/loewe/agua-drop-eau-de-parfum-para-mujer/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Floewe%2Fagua-drop-eau-de-parfum-para-mujer%2F',
  1,'verified','LOW01112',164.00,'EUR','in_stock',
  'Exact product and format: LOEWE Agua Drop Eau de Parfum 100 ml',
  'manual','notino:exact:LOW01112:2026-09-25',
  CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
)
ON CONFLICT(product_id,retailer_id) DO UPDATE SET
  merchant_product_url=excluded.merchant_product_url,
  affiliate_url=excluded.affiliate_url,
  affiliate_verified=1,
  exact_match_status='verified',
  retailer_sku=excluded.retailer_sku,
  price=excluded.price,
  currency=excluded.currency,
  stock_status=excluded.stock_status,
  shipping_text=excluded.shipping_text,
  source_type=excluded.source_type,
  source_ref=excluded.source_ref,
  last_verified_at=CURRENT_TIMESTAMP,
  updated_at=CURRENT_TIMESTAMP;

INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  67,10,
  'https://www.notino.es/loewe/aire-loewe-eau-de-toilette-para-mujer/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Floewe%2Faire-loewe-eau-de-toilette-para-mujer%2F',
  1,'verified','LOW0316',114.30,'EUR','in_stock',
  'Exact product and format: LOEWE Aire Eau de Toilette 100 ml',
  'manual','notino:exact:LOW0316:2026-09-25',
  CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
)
ON CONFLICT(product_id,retailer_id) DO UPDATE SET
  merchant_product_url=excluded.merchant_product_url,
  affiliate_url=excluded.affiliate_url,
  affiliate_verified=1,
  exact_match_status='verified',
  retailer_sku=excluded.retailer_sku,
  price=excluded.price,
  currency=excluded.currency,
  stock_status=excluded.stock_status,
  shipping_text=excluded.shipping_text,
  source_type=excluded.source_type,
  source_ref=excluded.source_ref,
  last_verified_at=CURRENT_TIMESTAMP,
  updated_at=CURRENT_TIMESTAMP;

INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  64,10,
  'https://www.notino.es/loewe/esencia-eau-de-parfum-para-hombre/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Floewe%2Fesencia-eau-de-parfum-para-hombre%2F',
  1,'verified','LOW00864',142.00,'EUR','in_stock',
  'Exact product and format: LOEWE Esencia Eau de Parfum 100 ml',
  'manual','notino:exact:LOW00864:2026-09-25',
  CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
)
ON CONFLICT(product_id,retailer_id) DO UPDATE SET
  merchant_product_url=excluded.merchant_product_url,
  affiliate_url=excluded.affiliate_url,
  affiliate_verified=1,
  exact_match_status='verified',
  retailer_sku=excluded.retailer_sku,
  price=excluded.price,
  currency=excluded.currency,
  stock_status=excluded.stock_status,
  shipping_text=excluded.shipping_text,
  source_type=excluded.source_type,
  source_ref=excluded.source_ref,
  last_verified_at=CURRENT_TIMESTAMP,
  updated_at=CURRENT_TIMESTAMP;

INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  74,10,
  'https://www.notino.es/loewe/esencia-loewe-eau-de-toilette-para-hombre/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Floewe%2Fesencia-loewe-eau-de-toilette-para-hombre%2F',
  1,'verified','LOW0003',112.00,'EUR','in_stock',
  'Exact product and format: LOEWE Esencia Eau de Toilette 100 ml',
  'manual','notino:exact:LOW0003:2026-09-25',
  CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
)
ON CONFLICT(product_id,retailer_id) DO UPDATE SET
  merchant_product_url=excluded.merchant_product_url,
  affiliate_url=excluded.affiliate_url,
  affiliate_verified=1,
  exact_match_status='verified',
  retailer_sku=excluded.retailer_sku,
  price=excluded.price,
  currency=excluded.currency,
  stock_status=excluded.stock_status,
  shipping_text=excluded.shipping_text,
  source_type=excluded.source_type,
  source_ref=excluded.source_ref,
  last_verified_at=CURRENT_TIMESTAMP,
  updated_at=CURRENT_TIMESTAMP;

WITH exactas AS (
  SELECT product_id, retailer_id FROM offers
  WHERE exact_match_status='verified'
    AND source_type IN ('merchant_jsonld_gtin','lir_shopify_json','purebeauty_product_page','manual')
  UNION
  SELECT v.product_id, vo.retailer_id
  FROM variant_offers vo
  JOIN product_variants v ON v.id=vo.variant_id
  WHERE vo.exact_match_status='verified'
),
resumen AS (
  SELECT product_id, COUNT(DISTINCT retailer_id) AS tiendas
  FROM exactas GROUP BY product_id
)
SELECT
  SUM(CASE WHEN tiendas>=2 THEN 1 ELSE 0 END) AS productos_2_o_mas,
  SUM(CASE WHEN tiendas>=3 THEN 1 ELSE 0 END) AS productos_3_o_mas,
  SUM(CASE WHEN tiendas>=4 THEN 1 ELSE 0 END) AS productos_4_o_mas,
  MAX(tiendas) AS maximo_tiendas
FROM resumen;