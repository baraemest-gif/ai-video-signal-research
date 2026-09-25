INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  59,10,
  'https://www.notino.es/calvin-klein/ck-one-eau-de-toilette-unisex/p-60116/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Fcalvin-klein%2Fck-one-eau-de-toilette-unisex%2Fp-60116%2F',
  1,'verified','CAK0286',21.90,'EUR','in_stock',
  'Exact product and format: Calvin Klein CK One Eau de Toilette 100 ml',
  'manual','notino:exact:CAK0286:2026-09-25',
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
  60,10,
  'https://www.notino.es/rochas/eau-de-rochas-eau-de-toilette-para-mujer/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Frochas%2Feau-de-rochas-eau-de-toilette-para-mujer%2F',
  1,'verified','ROS0020',37.00,'EUR','in_stock',
  'Exact product and format: Rochas Eau de Rochas Eau de Toilette 100 ml',
  'manual','notino:exact:ROS0020:2026-09-25',
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
  61,10,
  'https://www.notino.es/loewe/001-woman-eau-de-parfum-para-mujer/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Floewe%2F001-woman-eau-de-parfum-para-mujer%2F',
  1,'verified','LOW0261',126.00,'EUR','in_stock',
  'Exact product and format: LOEWE 001 Woman Eau de Parfum 100 ml',
  'manual','notino:exact:LOW0261:2026-09-25',
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