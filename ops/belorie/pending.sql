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
dos AS (
  SELECT product_id
  FROM exactas
  GROUP BY product_id
  HAVING COUNT(DISTINCT retailer_id)=2
)
SELECT
  target.id AS target_id,
  target.name AS target_name,
  target.size_label AS target_size,
  target.ean_gtin AS gtin,
  lad.id AS lad_id,
  lad.name AS lad_name,
  lad.size_label AS lad_size,
  o.price AS lad_price,
  o.currency AS lad_currency,
  o.merchant_product_url,
  o.affiliate_url,
  o.stock_status,
  o.shipping_text,
  o.source_type,
  o.source_ref
FROM dos d
JOIN products target ON target.id=d.product_id
JOIN products lad
  ON lad.id<>target.id
 AND lad.slug LIKE 'lad-%'
 AND lad.ean_gtin=target.ean_gtin
JOIN offers o
  ON o.product_id=lad.id
 AND o.retailer_id=4
 AND o.exact_match_status='verified'
WHERE target.ean_gtin IS NOT NULL
ORDER BY target.name;