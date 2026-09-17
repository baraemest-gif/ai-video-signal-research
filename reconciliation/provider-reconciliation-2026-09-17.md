# Provider Reconciliation — 2026-09-17

Status: **HOLD support document — not a DOI release**

Baseline compared: **2026-08-29** 14-provider research snapshot.
Current check date: **2026-09-17**.

This report separates baseline facts from current verification. A baseline value is never overwritten merely because a current page changed. Material changes are recorded as new evidence events. Where first-party evidence could not be rechecked cleanly, the provider remains pending or partial rather than being guessed.

## Scope

The baseline provider set is fixed at 14 for this reconciliation:

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

| Provider | Baseline reference | Current status | Current evidence summary | Release action |
|---|---|---|---|---|
| Runway | Standard $15/mo; 625 credits/mo; Gen-4.5 12 credits/s | verified_no_material_change | Official current pricing still shows Standard $15 monthly / $12 annualized, 625 credits/mo; Gen-4.5 remains 12 credits/s. | Keep baseline; record current verification date. |
| Kling AI | Standard $6.99 intro; $8.80 renewal; 660 credits/mo | pending_first_party_access | Current first-party page could not be independently re-read through the available research channel. Historical baseline must not be promoted to a current claim without a fresh provider check. | HOLD field-level current verification. |
| HeyGen | Creator $29/mo or $24 annualized; 600 credits/mo | verified_no_material_change | Official current pricing and Help Center show Creator $29/mo and 600 credits/mo. | Keep baseline; record current verification date. |
| InVideo AI | Baseline $17 annual-equivalent Plus; later 2026-09-07 event recorded 750 credits/mo | verified_material_change | Official current pricing now shows Starter $20/seat/mo billed annually with 400 credits/seat/mo and Plus $50/seat/mo billed annually with 2,000 credits/seat/mo. | Append a new dated change event; do not overwrite Aug 29 or Sep 7 history. |
| Fliki | Standard $28/mo; Premium $88/mo; free entry | verified_no_material_change | Official current pricing/feature pages still show free access and Standard $28/mo / Premium $88/mo with commercial rights on paid production plans. | Keep baseline; refresh checked date where fields match. |
| Pika | Standard $10/mo; 700 credits/mo | verified_material_change | Official current pricing now uses Free / Starter / Creator / Fancy. Starter is $10/mo with 900 credits/mo; Creator $35/mo with 3,150 credits/mo. Free is 0 monthly credits with packs only and no commercial license. | Append a new dated change event; current plan naming/allowance differs materially from baseline. |
| Hailuo AI | Standard $14.99/mo; 1,000 credits/mo; Hailuo 2.3 unit economics | pending_first_party_access | No sufficiently reliable current first-party pricing snapshot was obtained in this reconciliation pass. | HOLD field-level current verification. |
| Synthesia | Basic $0; Starter $29/mo; 1,200 credits/mo | verified_no_material_change | Official current pricing shows Basic $0, Starter $29/mo and 1,200 credits/mo; Basic up to 10 video minutes/month. | Keep baseline; record current verification date. |
| ElevenLabs | Free $0; Starter $6/mo; Free 10,000 credits | verified_no_material_change | Official current pricing shows Free 10k credits/mo and Starter $6/mo with 30k credits/mo; commercial license is included from Starter, not Free. | Keep baseline; current detail may enrich paid allowance fields. |
| OpusClip | Free; Starter $15/mo; Free 60 credits/mo | verified_no_material_change | Official current pricing still lists Free $0, Starter $15/mo, Pro $29/mo; Free remains 60 credits/mo. | Keep baseline; record current verification date. |
| Vizard | Free $0; 60 credits/mo; paid Creator available | partial_verified | Official pricing confirms Free $0 and 60 credits/mo; the dynamic Creator price was not stable enough in the retrieved representation for a clean normalized current paid reference. | Preserve unnormalized paid price; keep current free-access evidence. |
| Submagic | Starter $19/mo; free entry; plan/video limits | partial_verified | Official current pricing confirms Starter $19/mo, 45 credits and 15 videos on Starter. Current free-tier details were not sufficiently clear in the retrieved pricing representation to reassert the baseline free allowance. | Keep $19 paid reference; recheck free-tier state before release. |
| Hypernatural | Paid plans/credits unstable; baseline carried free-entry/caution context | needs_correction_or_change_event | Official Help Center currently states there is **no free plan and no free trial**, while the public pricing page uses a “Start for free” CTA. This is a material contradiction requiring a provider-level clarification or a clearly scoped interpretation. | HOLD free-entry field; do not count Hypernatural as free-entry until resolved. |
| Google Veo | Paid monthly reference not normalized; endpoint-dependent access/metering | evidence_expanded_still_not_monthly_normalized | Current Google Cloud Agent Platform pricing exposes explicit Veo 3.1 / Fast / Lite endpoint prices by output class and resolution. This improves model-level economics evidence but does not create a comparable monthly subscription price. | Add endpoint pricing evidence; retain monthly paid reference as not_normalized. |

## Material findings

### Confirmed material changes

- **InVideo AI**: current official plan structure and included credits differ materially from both the Aug 29 baseline and the Sep 7 event already recorded in AI Video Signal's ledger.
- **Pika**: plan naming and monthly credit allocations changed materially; the old `Standard $10 / 700 credits` state is historical, not current.
- **Hypernatural**: current official support says no free plan/trial, which conflicts with the earlier free-entry interpretation and with current “Start for free” marketing language. This must be resolved rather than normalized away.

### Evidence expansion

- **Google Veo** now has explicit current endpoint pricing visible for Veo 3.1 variants on a Google Cloud pricing surface. This supports model/endpoint economics but not a comparable monthly provider-plan price.

### Stable or substantially consistent

Runway, HeyGen, Fliki, Synthesia, ElevenLabs and OpusClip are materially consistent with the baseline fields checked in this pass.

### Still blocking a citation-grade release

- Kling AI current first-party recheck.
- Hailuo AI current first-party recheck.
- Vizard normalized paid-price decision.
- Submagic free-tier state recheck.
- Hypernatural free-entry contradiction resolution.
- Propagation of the confirmed InVideo and Pika changes into release-candidate CSV/JSON and any derived benchmark metrics.

## First-party sources used in this pass

- Runway pricing: https://runway.com/pricing
- Runway Gen-4.5: https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5
- HeyGen pricing: https://www.heygen.com/pricing
- HeyGen credits: https://help.heygen.com/en/articles/15126059-how-to-use-credits-on-heygen
- InVideo pricing: https://invideo.io/pricing/
- Fliki pricing: https://fliki.ai/pricing
- Pika pricing: https://pika.art/pricing
- Synthesia pricing: https://www.synthesia.io/pricing
- ElevenLabs pricing: https://elevenlabs.io/pricing
- OpusClip pricing: https://www.opus.pro/pricing
- Vizard pricing: https://vizard.ai/pricing
- Submagic pricing: https://www.submagic.co/pricing
- Hypernatural pricing: https://hypernatural.ai/pricing
- Hypernatural free-plan support note: https://app.hypernatural.ai/help/plans-billing-credits/16809715-can-i-use-hypernatural-for-free
- Google Cloud Veo pricing: https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing

## Release decision

**HOLD remains correct.** The provider set is now explicitly reconciled at the status level, but the first DOI release must not be generated until the unresolved provider fields are closed or explicitly represented as uncertainty and the release-candidate CSV/JSON are regenerated from the reconciled state.