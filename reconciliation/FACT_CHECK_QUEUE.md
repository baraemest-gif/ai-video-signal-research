# Provider Fact-Check Queue

Status date: **2026-09-17**

Purpose: document material provider ambiguities and their resolution before the first DOI-backed release. Provider replies may clarify factual fields but never grant editorial veto.

## Current state

**No provider-level pricing blocker remains open.**

| Provider | Issue | Evidence route | State |
|---|---|---|---|
| Pictory | Pricing-source protocol / current allowances | Direct Affiliate Manager correspondence | **resolved** — use live Pricing page as source of truth and date-stamp checks |
| Vizard | Dynamic Creator price and free allowance | Live first-party pricing UI | **resolved** — Creator $29/mo / 600 credits; yearly starting tier $14.50/mo billed $174/year; Free $0 / 60 credits |
| Submagic | Paid Starter state and free-entry scope | Official pricing + free-scheduler page | **resolved** — Starter $19/mo; limited one-post/video free access, no card, trial watermark |
| Hypernatural | Free-plan/trial status | Plan-specific official Support article | **resolved** — paid-only; no free plan or free trial. Generic `Start for free` CTA is not treated as a plan entitlement. |
| Kling AI | Current paid plan price and credits | Public first-party membership UI | **resolved** — Gold Member (黄金会员), ¥58/mo renewal, ¥46 first month after ¥5.99/7-day new-customer trial, 660 Inspiration Credits/month; CNY web scope preserved |
| Hailuo AI | Monthly-vs-annual Standard pricing discrepancy | Live public pricing UI + Subscription Service Terms | **resolved** — $14.99/month on monthly billing; $8.40/month equivalent billed $100.80/year on annual billing; 1,000 credits/month in both contexts |

## Hailuo resolution scope

The live public Hailuo pricing UI and the Subscription Service Terms were checked on 2026-09-17.

Current Standard state:

- Monthly billing: **$14.99/month**
- Annual billing: **$100.80/year**, displayed as **$8.40/month equivalent**
- Credits: **1,000 credits/month**
- Currency: **USD**
- Free tier: public pricing UI shows **$0/month** with **0 recurring monthly credits**

The lower current live value is therefore an **annual-equivalent rate**, not a contradictory monthly price.

Older official marketing references to `$6.99` and `$9.99` are retained as dated evidence but are **not promoted as current pricing** because they do not appear in the current live pricing UI and their exact historical/promotional scope is not established by the current public pages.

## Kling resolution scope

The public first-party membership UI at `https://klingai.com/app/membership/membership-plan` was verified on 2026-09-17 without login.

Current public web state:

- Plan: **Gold Member (黄金会员)**
- New-customer trial: **¥5.99 / 7 days**
- First month after trial: **¥46**
- Subsequent monthly renewal: **¥58/month**
- Allowance: **660 Inspiration Credits/month**
- Currency: **CNY**
- Free non-member access exists with daily free Inspiration Credits; exact daily amount is not normalized in the release candidate.

This CNY web price is not silently converted to USD and is not treated as globally universal pricing.

## Governance

- Direct provider replies may be stored as Tier B fact-check evidence.
- Canonical Tier A public sources remain preferred when their scope is clear.
- Provider clarifications never silently rewrite the 2026-08-29 historical baseline.
- Material changes become new dated events.
- Scope differences such as monthly vs annual billing or regional currency are represented explicitly rather than collapsed.
