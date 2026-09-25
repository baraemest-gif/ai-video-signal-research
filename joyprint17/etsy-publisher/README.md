# JoyPrint17 Etsy publisher

Safe GitHub Actions publisher for the JoyPrint17 HVAC digital product.

No OAuth credential or paid Canva template link is committed to the repository.

Required GitHub Actions secrets:
- ETSY_KEYSTRING
- ETSY_SHARED_SECRET
- ETSY_REFRESH_TOKEN
- ETSY_HVAC_CANVA_TEMPLATE_URL

The workflow refreshes Etsy OAuth, derives JoyPrint17 shop/taxonomy data from reference listing 4581730353, creates or resumes the HVAC listing, uploads the public cover image, generates the buyer PDF at runtime from the secret Canva template URL, uploads it to Etsy, and activates the listing.

The publisher checks for an exact-title existing listing to avoid accidental duplicates.
