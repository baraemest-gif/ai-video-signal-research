INSERT INTO offers (
  product_id, retailer_id, merchant_product_url, affiliate_url,
  affiliate_verified, exact_match_status, retailer_sku,
  price, currency, stock_status, shipping_text,
  source_type, source_ref, last_verified_at, updated_at
)
VALUES (
  52,
  10,
  'https://www.notino.es/la-roche-posay/pure-vitamin-c12-serum-iluminador-con-vitamina-c-antiarrugas/',
  (
    SELECT SUBSTR(affiliate_url,1,INSTR(affiliate_url,'url=')+3)
    FROM variant_offers
    WHERE retailer_id=10 AND affiliate_url IS NOT NULL
    ORDER BY id DESC
    LIMIT 1
  ) || 'https%3A%2F%2Fwww.notino.es%2Fla-roche-posay%2Fpure-vitamin-c12-serum-iluminador-con-vitamina-c-antiarrugas%2F',
  1,
  'verified',
  'LRP06821',
  54.00,
  'EUR',
  'in_stock',
  'Formato exacto La Roche-Posay Pure Vitamin C12 30 ml verificado en NOTINO',
  'manual',
  'notino:exact:LRP06821:2026-09-25',
  CURRENT_TIMESTAMP,
  CURRENT_TIMESTAMP
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
