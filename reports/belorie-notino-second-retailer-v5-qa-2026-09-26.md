# BELORIE · NOTINO second-retailer batch V5 — QA — 2026-09-26

## Artifact
belorie_notino_second_retailer_V5_2026-09-26.sql

SHA-256:
861584c673a2c5c8d68b279e433ecdca20215dcb841c6e27acc257e06f6bae8a

## Scope
22 existing BELORIE product slugs receive or refresh an exact NOTINO.es retailer offer.

The batch includes:
- skincare
- haircare
- makeup
- fragrances

Latest added exact perfume variants:
- Lancôme La Vie Est Belle EDP 30 ml
- Lancôme La Vie Est Belle EDP 50 ml
- Lancôme La Vie Est Belle EDP 100 ml
- Carolina Herrera Good Girl EDP 30 ml
- Carolina Herrera Good Girl EDP 50 ml
- Carolina Herrera Good Girl EDP 80 ml
- Narciso Rodriguez For Her EDP 50 ml
- Rabanne 1 Million EDT 50 ml
- Rabanne 1 Million EDT 100 ml

All perfume entries use NOTINO variant-specific /p-... URLs so size-specific mapping does not rely on the default selected variant.

## Tracking
Uses the same CJ/VivNetworks tracking base already live on BELORIE:
anrdoezrs.net / publisher 101884441 / advertiser link 17353471

## Data safety
The batch does NOT change:
- GTIN/EAN
- product titles
- descriptions
- images
- canonical URLs
- sitemap
- categories
- product identity

Offers use:
ON CONFLICT(product_id, retailer_id) DO UPDATE

## QA
Executed successfully against a mock SQLite/D1-compatible schema with:
- products
- retailers
- offers
- UNIQUE(product_id, retailer_id)

Result:
- SQL execution: PASS
- unique target slugs: 22
- resulting offers: 22
- stock statuses: 21 in_stock, 1 unknown
- price range: EUR 9.80 to EUR 148.00

## Deployment
NOT deployed.
Apply only to the live BELORIE D1 after direct Cloudflare / authorized execution access is restored.
