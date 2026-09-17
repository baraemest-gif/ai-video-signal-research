# Provider Reconciliation — 2026-09-17

Status: **HOLD support document — not a DOI release**

Baseline compared: **2026-08-29** 14-provider research snapshot.  
Current check date: **2026-09-17**.

This report separates baseline facts from current verification. Historical values are not overwritten by later changes. Material changes are recorded as new evidence events. Where current first-party evidence remains conflicting or inaccessible, the provider stays unresolved rather than being guessed.

## Scope

1. Runway
2. Kling AI
3. HeyGen
4. InVideo AI
5. Fliki
6. Pika
7. Hailuo AI
8. Synthesia
9. ElevenLabs
10. OpusClip
11. Vizard
12. Submagic
13. Hypernatural
14. Google Veo

## Reconciliation status

| Provider | Current status | Current evidence summary | Release action |
|---|---|---|---|
| Runway | `verified_no_material_change` | Standard $15/mo, 625 credits/mo; Gen-4.5 12 credits/s remains supported. | Keep current checked state. |
| Kling AI | `pending_first_party_access` | Public homepage is reachable but current plan pricing was not exposed in the retrieved representation. | Keep current price/allowance blank pending direct first-party check/provider response. |
| HeyGen | `verified_no_material_change` | Creator $29/mo and 600 credits/mo supported by current first-party pricing/help. | Keep current checked state. |
| InVideo AI | `verified_material_change` | Current official pricing shows Starter $20/seat/mo billed annually with 400 credits/seat/mo and Plus $50/seat/mo billed annually with 2,000 credits/seat/mo. | Preserve Aug 29 / Sep 7 history; append current state. |
| Fliki | `verified_no_material_change` | Current Standard $28/mo / Premium $88/mo and paid commercial-rights context materially consistent. | Keep current checked state. |
| Pika | `verified_material_change` | Starter remains $10/mo but now shows 900 credits/mo; Creator $35/mo with 3,150 credits/mo; Free has 0 recurring monthly credits. | Preserve old 700-credit state as historical; use current dated state. |
| Hailuo AI | `first_party_pricing_conflict` | Subscription Service Terms list Standard $14.99/mo with 1,000 credits, while separate official Hailuo pages list Standard at $6.99 or $9.99. | Do not publish one current normalized Standard price until scoped/clarified. |
| Synthesia | `verified_no_material_change` | Basic $0; Starter $29/mo and 1,200 credits/mo. | Keep current checked state. |
| ElevenLabs | `verified_no_material_change` | Free 10k credits/mo; Starter $6/mo with 30k; commercial license begins on Starter. | Keep current checked state. |
| OpusClip | `verified_no_material_change` | Free $0, Starter $15/mo, Free 60 credits/mo remain supported. | Keep current checked state. |
| Vizard | `verified_no_material_change` | Live dynamic pricing UI verified Creator $29/mo with 600 credits/mo; yearly starting tier $14.50/mo billed $174/year with 7,200 credits/year; Free $0 with 60 credits/mo. | Normalize current Creator monthly price at $29 and preserve annual context. |
| Submagic | `verified_no_material_change` | Starter $19/mo, 45 credits and 15 videos. Official free-scheduler page confirms one free video/post, no card, with trial watermarking. | Scope free entry as limited one-post/trial access; keep $19 paid reference. |
| Hypernatural | `verified_material_change` | Plan-specific official support states paid-only, no free plan and no free trial. Generic “Start for free” CTA does not state a plan entitlement. | Record current no-free-plan/no-trial state; preserve earlier free-entry interpretation as historical/corrected context. |
| Google Veo | `evidence_expanded_still_not_monthly_normalized` | Explicit current endpoint pricing exists for Veo 3.1 variants, but no comparable monthly provider subscription price is asserted. | Keep monthly paid reference `not_normalized`; retain endpoint economics. |

## Current material changes

- **InVideo AI:** plan structure/credits differ materially from earlier dated states.
- **Pika:** current monthly credit allocation differs from the Aug 29 baseline.
- **Hypernatural:** explicit current support establishes no free plan/trial; prior free-entry interpretation is not promoted as current.

## Current first-party conflict

- **Hailuo AI:** explicit official sources publish incompatible Standard-plan prices. The conflict remains visible; no current normalized paid price is selected.

## Resolved during this reconciliation pass

- **Vizard:** dynamic pricing was verified through the live pricing UI; Creator can now be normalized at $29/mo for the current candidate.
- **Submagic:** current paid plan and limited free-entry state are now both first-party evidenced.
- **Hypernatural:** plan-specific support is treated as the scoped source for free-plan/trial status; generic CTA language is not treated as plan evidence.
- **InVideo AI / Pika:** confirmed current changes are already propagated into the release-candidate CSV/JSON.

## Still blocking field-level completion

- **Kling AI:** current direct plan-price/credit verification.
- **Hailuo AI:** conflicting first-party Standard prices need provider clarification or a defensible scope distinction.

Google Veo remains intentionally non-monthly-normalized by design rather than as a missing-data error.

## First-party sources

- Runway pricing: https://runway.com/pricing
- Runway Gen-4.5: https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5
- HeyGen pricing: https://www.heygen.com/pricing
- HeyGen credits: https://help.heygen.com/en/articles/15126059-how-to-use-credits-on-heygen
- InVideo pricing: https://invideo.io/pricing/
- Fliki pricing: https://fliki.ai/pricing
- Pika pricing: https://pika.art/pricing
- Hailuo Subscription Service Terms: https://hailuoai.video/doc/payment-policy.html
- Hailuo official $6.99 marketing evidence: https://blog.hailuoai.video/blog/create-stunning-visuals-ai-image-generator
- Hailuo official $9.99 marketing evidence: https://blog.hailuoai.video/blog/paid-vs-free-ai-video-generators
- Hailuo 2.3 unit economics: https://blog.hailuoai.video/blog/introducing-hailuo-2-3-ai-video-generator
- Synthesia pricing: https://www.synthesia.io/pricing
- ElevenLabs pricing: https://elevenlabs.io/pricing
- OpusClip pricing: https://www.opus.pro/pricing
- Vizard pricing: https://vizard.ai/pricing
- Submagic pricing: https://www.submagic.co/pricing
- Submagic limited free entry: https://www.submagic.co/free-social-media-scheduler
- Hypernatural plan/free-access support: https://app.hypernatural.ai/help/plans-billing-credits/16809715-can-i-use-hypernatural-for-free
- Google Cloud Veo pricing: https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing

## Release decision

**HOLD remains correct.** The current provider blockers have been reduced to Kling AI current pricing verification and the Hailuo first-party pricing conflict. Other release gates — final metadata, custom Zenodo rights preview, final freeze/checksums, public-file consistency and immutable package reconstruction — also remain before DOI publication.
