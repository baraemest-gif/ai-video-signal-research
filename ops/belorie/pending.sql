INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  29,10,
  'https://www.notino.es/carolina-herrera/good-girl-eau-de-parfum-para-mujer/p-573739/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Fcarolina-herrera%2Fgood-girl-eau-de-parfum-para-mujer%2Fp-573739%2F',
  1,'verified','CHR0867',79.00,'EUR','in_stock',
  'Producto y formato exactos: Carolina Herrera Good Girl Eau de Parfum 30 ml verificado en NOTINO',
  'manual','notino:exact:CHR0867:2026-09-25',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
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
  21,10,
  'https://www.notino.es/color-wow/color-wow-dream-coat-supernatural-spray-spray-para-cabello-humedo-para-alisar-el-cabello/p-15960471/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Fcolor-wow%2Fcolor-wow-dream-coat-supernatural-spray-spray-para-cabello-humedo-para-alisar-el-cabello%2Fp-15960471%2F',
  1,'verified','CLW02351',27.50,'EUR','in_stock',
  'Producto y formato exactos: Color WOW Dream Coat Supernatural Spray 200 ml verificado en NOTINO',
  'manual','notino:exact:CLW02351:2026-09-25',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
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
  30,10,
  'https://www.notino.es/lancome/la-vie-est-belle-eau-de-parfum-para-mujer/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Flancome%2Fla-vie-est-belle-eau-de-parfum-para-mujer%2F',
  1,'verified',NULL,59.90,'EUR','in_stock',
  'Producto y formato exactos: Lancôme La Vie Est Belle Eau de Parfum 30 ml verificado en NOTINO',
  'manual','notino:exact:la-vie-est-belle-30ml:2026-09-25',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
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
  SELECT product_id, retailer_id
  FROM offers
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
  FROM exactas
  GROUP BY product_id
)
SELECT
  SUM(CASE WHEN tiendas>=2 THEN 1 ELSE 0 END) AS productos_2_o_mas,
  SUM(CASE WHEN tiendas>=3 THEN 1 ELSE 0 END) AS productos_3_o_mas,
  SUM(CASE WHEN tiendas>=4 THEN 1 ELSE 0 END) AS productos_4_o_mas,
  MAX(tiendas) AS maximo_tiendas
FROM resumen;