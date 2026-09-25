UPDATE offers
SET shipping_text='Producto y formato exactos: Narciso Rodriguez For Her Eau de Parfum 50 ml. Precio promocional mostrado por NOTINO con código sale.',
    updated_at=CURRENT_TIMESTAMP
WHERE product_id=27
  AND retailer_id=10
  AND source_ref='notino:exact:p-69404:2026-09-25';

SELECT p.name AS producto, o.price, o.currency, o.shipping_text
FROM offers o
JOIN products p ON p.id=o.product_id
WHERE o.product_id=27 AND o.retailer_id=10;