SELECT p.id,p.name,p.size_label,p.ean_gtin,
       GROUP_CONCAT(DISTINCT r.name) AS plataformas,
       COUNT(DISTINCT o.retailer_id) AS tiendas
FROM products p
LEFT JOIN offers o
  ON o.product_id=p.id
 AND o.exact_match_status='verified'
 AND o.source_type IN ('merchant_jsonld_gtin','lir_shopify_json','purebeauty_product_page','manual')
LEFT JOIN retailers r ON r.id=o.retailer_id
WHERE lower(p.name) LIKE '%retinol%b3%'
GROUP BY p.id,p.name,p.size_label,p.ean_gtin
ORDER BY p.id;