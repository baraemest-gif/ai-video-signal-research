INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  6,10,
  'https://www.notino.es/paco-rabanne/1-million-eau-de-toilette-para-hombre/p-10817/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Fpaco-rabanne%2F1-million-eau-de-toilette-para-hombre%2Fp-10817%2F',
  1,'verified','PAR0004',119.00,'EUR','in_stock',
  'Producto y formato exactos: Rabanne 1 Million Eau de Toilette 100 ml verificado en NOTINO',
  'manual','notino:exact:PAR0004:2026-09-25',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
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
  28,10,
  'https://www.notino.es/paco-rabanne/1-million-eau-de-toilette-para-hombre/p-65396/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Fpaco-rabanne%2F1-million-eau-de-toilette-para-hombre%2Fp-65396%2F',
  1,'verified','PAR0005',90.00,'EUR','in_stock',
  'Producto y formato exactos: Rabanne 1 Million Eau de Toilette 50 ml verificado en NOTINO',
  'manual','notino:exact:PAR0005:2026-09-25',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
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
  31,10,
  'https://www.notino.es/lancome/la-vie-est-belle-eau-de-parfum-para-mujer/p-432200/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Flancome%2Fla-vie-est-belle-eau-de-parfum-para-mujer%2Fp-432200%2F',
  1,'verified','LAM1787',93.50,'EUR','in_stock',
  'Producto y formato exactos: Lancôme La Vie Est Belle Eau de Parfum 100 ml verificado en NOTINO',
  'manual','notino:exact:LAM1787:2026-09-25',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP
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