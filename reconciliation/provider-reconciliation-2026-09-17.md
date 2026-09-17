# Provider Reconciliation — 2026-09-17

Status: **HOLD support document — provider reconciliation complete; not a DOI release**

Baseline compared: **2026-08-29** 14-provider research snapshot.  
Current check date: **2026-09-17**.

This report separates historical baseline facts from current verification. Historical values are never overwritten merely because a provider changes its plans, billing cadence, free-access state or entitlements.

## Scope

The reconciliation covers exactly 14 providers:

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

## Current reconciliation status

| Provider | Current status | Current evidence / release treatment |
|---|---|---|
| Runway | `verified_no_material_change` | Standard $15/month, 625 credits/month; checked current. |
| Kling AI | `verified_current_cny_web_pricing` | Official public membership UI shows Gold Member at ¥58/month renewal, after ¥5.99/7-day new-customer trial and ¥46 first month; 660 Inspiration Credits/month. This is explicitly scoped as CNY web pricing and is not silently converted to USD. |
| HeyGen | `verified_no_material_change` | Creator $29/month and 600 credits/month remain current. |
| InVideo AI | `verified_material_change` | Current official structure differs from the Aug 29 baseline and Sep 7 event; current candidate carries the new checked state while preserving history. |
| Fliki | `verified_no_material_change` | Current paid pricing/free-entry state remains materially consistent with the checked baseline fields. |
| Pika | `verified_material_change` | Starter remains $10 but current allowance is 900 credits/month; historical 700-credit state remains historical. |
| Hailuo AI | `verified_current_monthly_and_annual_pricing` | Subscription terms list Standard $14.99/month with 1,000 credits. Current public pricing UI shows annual billing at $8.40/month equivalent, billed $100.80/year, with the same 1,000 credits/month. The apparent conflict is billing cadence, not one competing current monthly price. Older official $6.99/$9.99 marketing references are not promoted as current because they are absent from the live pricing UI. |
| Synthesia | `verified_no_material_change` | Basic $0; Starter $29/month; 1,200 credits/month. |
| ElevenLabs | `verified_no_material_change` | Free 10k credits/month; Starter $6/month with 30k credits/month; commercial-license distinction preserved. |
| OpusClip | `verified_no_material_change` | Free $0; Starter $15/month; Free remains 60 credits/month. |
| Vizard | `verified_no_material_change` | Live UI verifies Creator $29/month with 600 credits/month; yearly starting tier $14.50/month billed $174/year; Free $0/60 credits. |
| Submagic | `verified_no_material_change` | Starter $19/month, 45 credits / 15 videos; limited free entry is separately scoped and not treated as a recurring full free plan allowance. |
| Hypernatural | `verified_material_change` | Official plan-specific support states no free plan and no free trial. Generic “Start for free” wording is treated as onboarding language, not a free-plan entitlement. |
| Google Veo | `evidence_expanded_still_not_monthly_normalized` | Endpoint pricing is explicit and usable for model economics; no comparable monthly subscription is asserted. |

## Provider reconciliation decision

**Provider-change reconciliation is complete for the current HOLD candidate.**

There are no remaining provider-level blockers requiring a guessed current value. Where a global monthly comparison is not defensible, the record remains explicitly scoped instead of being force-normalized:

- Kling AI: exact current public CNY web membership pricing is retained as CNY and excluded from USD-normalized monthly-price statistics.
- Google Veo: endpoint economics are retained without inventing a monthly provider subscription.

## Material current changes versus the historical baseline

- **InVideo AI:** current official plan/credit structure changed materially.
- **Pika:** current monthly credits changed materially.
- **Hypernatural:** current official support establishes no free plan/trial.
- **Kling AI:** current public pricing is now captured directly in CNY with exact trial/first-month/renewal scope rather than relying on the earlier USD-style baseline representation.

## Billing-cadence clarification

### Hailuo AI

The previously recorded first-party pricing conflict is resolved by billing cadence:

- monthly billing reference: **$14.99/month**;
- current annual billing UI: **$8.40/month equivalent**, billed **$100.80/year**;
- allowance: **1,000 credits/month** in both contexts.

Older official marketing references to $6.99/$9.99 remain evidence of prior/unscoped published claims but are not current normalized prices because they are not present in the current live pricing UI.

## Current quantitative candidate scope

The release candidate now has **11 normalized USD monthly or monthly-equivalent paid references**. Kling AI remains outside that statistic because its directly verified current price is CNY-scoped. Google Veo remains endpoint-priced rather than monthly-plan normalized.

These figures remain HOLD-candidate research, not the final DOI-backed benchmark.

## First-party sources

Key current sources include:

- Runway: `https://runway.com/pricing`
- Kling AI membership: `https://klingai.com/app/membership/membership-plan`
- HeyGen: `https://www.heygen.com/pricing`
- InVideo AI: `https://invideo.io/pricing/`
- Fliki: `https://fliki.ai/pricing`
- Pika: `https://pika.art/pricing`
- Hailuo live pricing: `https://hailuoai.video/`
- Hailuo Subscription Service Terms: `https://hailuoai.video/doc/payment-policy.html`
- Synthesia: `https://www.synthesia.io/pricing`
- ElevenLabs: `https://elevenlabs.io/pricing`
- OpusClip: `https://www.opus.pro/pricing`
- Vizard: `https://vizard.ai/pricing`
- Submagic: `https://www.submagic.co/pricing`
- Hypernatural plan support: `https://app.hypernatural.ai/help/plans-billing-credits/16809715-can-i-use-hypernatural-for-free`
- Google Veo: `https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing`

The machine-readable source manifest remains authoritative for the complete source inventory.

## Release decision

The project remains **HOLD**, but no longer because of unresolved provider reconciliation. Remaining work is release engineering and publication governance: final freeze, final CSV/JSON distributions, checksums, final citation metadata, Zenodo custom-rights preview, and public-release consistency.

Production **V70.7.5 remains untouched**.
