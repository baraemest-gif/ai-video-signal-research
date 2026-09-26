# BELORIE — Paco OLAPLEX second-retailer batch — 2026-09-26

## Live BELORIE baseline
Build observed:
- v4.9.6e-full-catalog-2026-09-25

## Exact second-retailer matches verified

### OLAPLEX No.3 Hair Perfector — 100 ml
BELORIE:
- /producto/olaplex-no3-hair-perfector
- current retailer before patch: Pure Beauty

Paco Perfumerías:
- https://www.pacoperfumerias.com/olaplex-n-3-hair-perfector-2-24732.html
- exact product family and 100 ml variant present
- observed price: €19.95
- Paco program: Awin MID 21605 / affiliate 3005653

### OLAPLEX No.5 Bond Maintenance Conditioner — 250 ml
BELORIE:
- /producto/olaplex-no-5-bond-maintenance-conditioner-250ml
- current retailer before patch: Lir Pharmacy

Paco Perfumerías:
- https://www.pacoperfumerias.com/olaplex-n-5-bond-maintenance-conditioner-2-24734.html
- exact product and 250 ml variant present
- observed price: €19.95
- Paco program: Awin MID 21605 / affiliate 3005653

## Stock handling
Paco's rendered product pages contain both availability and out-of-stock text associated with multiple variants.
Therefore:
- do NOT set in_stock
- store stock_status='unknown'
- destination page remains source of truth

## Identifier handling
Do NOT update GTIN/EAN for either product in this batch.
This avoids contaminating BELORIE's master identifier layer with retailer-specific or ambiguous identifiers.

## Prepared SQL
belorie_paco_olaplex_second_retailer_2026-09-26.sql

Properties:
- product resolved by exact BELORIE slug
- Paco retailer resolved by exact name, not hard-coded numeric ID
- idempotent ON CONFLICT(product_id,retailer_id)
- only offer fields updated
- includes post-apply verification SELECT

## Deployment status
NOT deployed.
Production write access to BELORIE D1 is not currently available from connected tools.
