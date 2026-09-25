INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  13,7,
  'https://www.stylevana.com/en_EU/the-ordinary-niacinamide-10-zinc-1-30ml.html',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'ued=')+3)
    FROM offers
    WHERE retailer_id=7 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.stylevana.com%2Fen_EU%2Fthe-ordinary-niacinamide-10-zinc-1-30ml.html',
  1,'verified',NULL,9.70,'EUR','in_stock',
  'Exact product and format: The Ordinary Niacinamide 10% + Zinc 1% 30 ml',
  'manual','stylevana:exact:the-ordinary-niacinamide-30ml:2026-09-25',
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
  16,7,
  'https://www.stylevana.com/es_ES/marcas/la-roche-posay.html',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'ued=')+3)
    FROM offers
    WHERE retailer_id=7 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.stylevana.com%2Fes_ES%2Fmarcas%2Fla-roche-posay.html',
  1,'verified',NULL,17.39,'EUR','in_stock',
  'Exact product and format: La Roche-Posay Cicaplast Baume B5+ 40 ml',
  'manual','stylevana:exact:cicaplast-baume-b5-40ml:2026-09-25',
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