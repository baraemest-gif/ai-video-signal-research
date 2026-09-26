# AI Video Signal — Sitemap Freshness Audit — 2026-09-26

## Live production checked
Domain: https://aivideosignal.com/

robots.txt:
- Allow: /
- Disallow: /api/
- Sitemap: https://aivideosignal.com/sitemap.xml

## Sitemap index freshness issue
The live sitemap index currently reports these child sitemap lastmod values:
- sitemap-core.xml — 2026-09-08
- sitemap-filmora.xml — 2026-09-08
- sitemap-flexclip.xml — 2026-09-02
- sitemap-commercial.xml — 2026-09-08
- sitemap-editorial.xml — 2026-09-08

But the child sitemaps contain newer URL-level lastmods:
- sitemap-core.xml — up to 2026-09-19
- sitemap-commercial.xml — up to 2026-09-22
- sitemap-editorial.xml — up to 2026-09-19

Therefore the sitemap index freshness metadata is stale relative to its children.

## Priority commercial URLs with stale URL-level lastmod
Observed live:
- /best-ai-video-tools-for-marketing-agencies/ — sitemap-core.xml — 2026-08-31
- /best-ai-explainer-video-generators/ — sitemap-commercial.xml — 2026-09-01
- /synthesia-alternatives/ — sitemap-commercial.xml — 2026-08-31
- /creatify-review/ — sitemap-commercial.xml — 2026-09-02
- /heygen-alternatives/ — sitemap-commercial.xml — 2026-08-31
- /invideo-alternatives/ — sitemap-commercial.xml — 2026-09-02
- /hailuo-ai-review/ — sitemap-editorial.xml — 2026-09-08

Recent stored QA confirms at least some of these pages were edited after the sitemap dates. Example: the Revenue Sprint v9 QA dated 2026-09-18 explicitly lists best-ai-video-tools-for-marketing-agencies/index.html among the three modified HTML files.

## Safe correction boundary
When the exact production source package is recovered:
1. Update each URL lastmod only to the date of a real content modification/deployment.
2. Update sitemap-index child lastmod to the newest real URL modification represented by that child sitemap.
3. Do not change canonical URLs.
4. Do not change affiliate URLs/clickrefs.
5. Do not change page copy solely to force a fresh date.
6. Do not set every URL to today's date.
7. Regenerate sitemap hashes/QA after the XML-only patch.

## Current access limitation
The connected GitHub repository contains research, QA, release documentation and integration material, but not the complete deployed site package.
ChatGPT Library contains V70/V71 QA and hold ZIPs, not the complete current production package.
No production deployment was attempted.

## Commercial priority
Fix first when source becomes available:
1. Hailuo pricing/review
2. Marketing agencies
3. Explainer video generators
4. Synthesia alternatives
5. HeyGen alternatives
6. InVideo alternatives
7. Creatify review

Reason: these pages map to recent buyer-intent work and should receive accurate recrawl signals.
