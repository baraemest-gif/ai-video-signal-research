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
  p.id,
  p.name,
  p.size_label,
  p.ean_gtin,
  GROUP_CONCAT(DISTINCT r.name) AS plataformas
FROM dos d
JOIN products p ON p.id=d.product_id
JOIN exactas e ON e.product_id=p.id
JOIN retailers r ON r.id=e.retailer_id
GROUP BY p.id,p.name,p.size_label,p.ean_gtin
ORDER BY p.name;
