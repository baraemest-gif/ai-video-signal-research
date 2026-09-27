# AI Video Signal v33 — Sales/CTR Safe Patch Tools

Date: 2026-09-27

## Objective
Apply a small, reversible SEO/authority patch to the CURRENT AI Video Signal source tree, then deploy it only to a Cloudflare Pages preview branch.

## Why this is deliberately small
Current GSC data shows the acquisition bottleneck is severe: about 11.9k impressions but only 20 clicks. Pages around positions 8–20 should be improved before creating more content.

## Safety boundary
The patch does NOT modify _worker.js, assets/site.js, assets/styles.css, _headers, canonical tags, robots tags, checkout code, affiliate URLs, pricing facts, CSS, JS, D1/R2, or Cloudflare configuration.

It is fail-closed: if the current source title/description/canonical does not match the expected live state, it aborts before writing any file.

## Changes
- ElevenLabs cancellation/refund: stronger refund-intent title + description.
- Filmora Free vs Paid: stronger purchase-decision title + description.
- Compliance training: keep current title; enrich description with SCORM/LMS/completion/versioning intent.
- Filmora Free Trial: keep current title; improve standard meta description.
- Add one contextual authority link to /best-ai-video-generators/ from pricing benchmarks, annual-vs-monthly, and credits-usage comparison.

## Termux workflow
1. Use the CURRENT production source folder, not an old preview ZIP.
2. Dry run:
   python ~/aivs-v33-tools/patch_current_production.py /path/to/current/site
3. Apply only if every guard passes:
   python ~/aivs-v33-tools/patch_current_production.py /path/to/current/site --apply --manifest ~/aivs-v33-tools/qa-manifest.json
4. Preview only:
   cd /path/to/current/site
   npx wrangler@latest pages deploy . --project-name=ai-video-signal --branch=v33-sales-ctr-preview
5. STOP and validate desktop + mobile before any production promotion.

## Important
Do not run this against the 2026-09-19 snapshot contained in the v32 preview package. That older snapshot is intentionally expected to fail the safety guards because several live pages were updated later.