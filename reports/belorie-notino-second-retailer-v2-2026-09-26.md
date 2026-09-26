# BELORIE — NOTINO second-retailer expansion V2 — 2026-09-26

## Prepared exact second-retailer offers
1. Calvin Klein CK One EDT 100 ml
   - BELORIE: /producto/calvin-klein-ck-one-edt-100ml
   - NOTINO: 100 ml
   - €21.90
   - in stock
   - code CAK0286

2. Clinique Take The Day Off Cleansing Balm 125 ml
   - BELORIE: /producto/clinique-take-the-day-off-balm-125ml
   - NOTINO: 125 ml variant
   - €24.90
   - stock kept unknown because visible stock state is tied to selected 200 ml variant

3. DKNY Women EDP 100 ml
   - BELORIE: /producto/dkny-women-edp-100ml
   - NOTINO: DKNY Original Women Energizing EDP 100 ml
   - €30.90
   - in stock
   - code DKN0268

4. Urban Decay All Nighter Matte 118 ml
   - BELORIE: /producto/urban-decay-all-nighter-matte-118ml
   - NOTINO: All Nighter Matte Finish 118 ml
   - €31.50
   - in stock
   - code URD01079

5. L'Oréal Telescopic Extensionist Mascara Black
   - BELORIE: /producto/loreal-telescopic-extensionist-mascara-black
   - NOTINO: Telescopic Extensionist black 9.9 ml
   - €16.50
   - in stock
   - code LOR10759

6. Payot N°2 CC Crème Anti-Rougeurs SPF50 40 ml
   - BELORIE: /producto/payot-cc-creme-anti-rougeurs-spf50-40ml
   - NOTINO: 40 ml
   - €17.70
   - in stock
   - code PAY01248

## Tracking
Uses the same CJ/VivNetworks tracking base already verified live in BELORIE:
https://www.anrdoezrs.net/click-101884441-17353471?url=<encoded-destination>

## Excluded candidates
- Clinique High Impact Mascara: NOTINO current page selected Black Honey, not BELORIE Black.
- Urban Decay Perversion Mascara: exact product found but currently out of stock.
- Urban Decay Eyeshadow Primer Potion: product matches, but BELORIE master page does not encode size; held to avoid ambiguous variant mapping.
- Clarins Multi-Intensive Noche: naming/reformulation ambiguity vs NOTINO Super Restorative listing; held.
- Shiseido Future Solution LX Eye & Lip Cream Estuche: product-vs-set ambiguity; held.
- CeraVe Blemish Control Cleanser: Pure Beauty current size is 236 ml, BELORIE is 473 ml.
- CeraVe Purifying Micellar Water: Pure Beauty current size is 295 ml, BELORIE is 400 ml.
- CeraVe Brightening Vitamin C Cleanser: no exact Pure Beauty match found.
- Redken Acidic Bonding Concentrate Shampoo 300 ml: no exact Paco result found.
- Color Wow Dream Coat 200 ml: no exact LIR result found.

## Safety
- No GTIN/EAN changes.
- No product-master changes.
- No sitemap/canonical changes.
- Idempotent UPSERT by product_id + retailer_id.
- Retailer resolved by name NOTINO.es.
- No deployment performed.
