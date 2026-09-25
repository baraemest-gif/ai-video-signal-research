INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  51,
  7,
  'https://www.stylevana.com/es_ES/la-roche-posay-retinol-b3-pure-retinol-serum-30ml108313.html',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'ued=')+3)
    FROM offers
    WHERE retailer_id=7 AND affiliate_url IS NOT NULL
    ORDER BY id DESC
    LIMIT 1
  ) || 'https%3A%2F%2Fwww.stylevana.com%2Fes_ES%2Fla-roche-posay-retinol-b3-pure-retinol-serum-30ml108313.html',
  1,'verified',NULL,44.69,'EUR','in_stock',
  'Producto y formato exactos: La Roche-Posay Retinol B3 Serum 30 ml verificado en Stylevana España',
  'manual',
  'stylevana:exact:la-roche-posay-retinol-b3-30ml:2026-09-25',
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
  51,
  10,
  'https://www.notino.es/la-roche-posay/retinol-serum-antiarrugas-regenerador-con-retinol/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC
    LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Fla-roche-posay%2Fretinol-serum-antiarrugas-regenerador-con-retinol%2F',
  1,'verified','LRP06618',49.00,'EUR','in_stock',
  'Producto y formato exactos: La Roche-Posay Retinol B3 Serum 30 ml verificado en NOTINO',
  'manual',
  'notino:exact:LRP06618:2026-09-25',
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

SELECT p.name AS producto,
       COUNT(DISTINCT e.retailer_id) AS tiendas,
       GROUP_CONCAT(DISTINCT r.name) AS plataformas
FROM (
  SELECT product_id, retailer_id
  FROM offers
  WHERE product_id=51
    AND exact_match_status='verified'
    AND source_type IN ('merchant_jsonld_gtin','lir_shopify_json','purebeauty_product_page','manual')
) e
JOIN products p ON p.id=e.product_id
JOIN retailers r ON r.id=e.retailer_id
GROUP BY p.id,p.name;