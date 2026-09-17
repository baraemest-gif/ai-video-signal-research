# Provider Fact-Check Queue

Status date: **2026-09-17**

Purpose: close material provider ambiguities before the first DOI-backed release. Provider replies may clarify factual fields but do not grant editorial veto.

| Provider | Issue | Contact route | State |
|---|---|---|---|
| Pictory | Pricing-source protocol / current allowances | Direct Affiliate Manager correspondence | **confirmed** — use live Pricing page as source of truth and date-stamp checks |
| Vizard | Dynamic Creator price and free allowance | Live first-party pricing UI | **resolved** — Creator $29/mo / 600 credits; yearly starting tier $14.50/mo billed $174/year; Free $0 / 60 credits |
| Submagic | Paid Starter state and free-entry scope | Official pricing + free-scheduler page | **resolved** — Starter $19/mo; limited one-post/video free access, no card, trial watermark |
| Hypernatural | Free-plan/trial status | Plan-specific official Support article | **resolved** — paid-only; no free plan or free trial. Generic `Start for free` CTA is not treated as a plan entitlement. |
| Hailuo AI | Conflicting first-party Standard prices | service@hailuoai.com | **open** — draft prepared; awaiting manual send from `partners@aivideosignal.com` |
| Kling AI | Current Standard plan price and credits | support@kling.ai | **open** — draft prepared; awaiting manual send from `partners@aivideosignal.com` |

## Remaining questions

### Hailuo AI
- What is the current canonical monthly Standard price?
- Why do official sources simultaneously show `$14.99`, `$9.99` and `$6.99` for Standard?
- Are the lower values annual-equivalent, promotional, regional, campaign-specific or stale?
- Is `1,000 credits/month` still the current Standard allowance?
- Which public pricing/terms URL should be cited as the current source of truth?

### Kling AI
- What is the current Standard monthly web price?
- Do intro and renewal prices still differ?
- What is the current Standard monthly credit allowance?
- What is the canonical official pricing URL for citation?
- Do web, mobile-store or regional prices differ materially?

## Resolved-source rule used for Hypernatural

When two Tier A pages appear inconsistent but one source is explicitly scoped to the disputed field and the other is generic marketing language, the specifically scoped source may control that field if the scopes can be distinguished without inference.

Applied here:

- Specific support article: **no free plan / no free trial**.
- Generic CTA: **Start for free**.

The CTA does not state a plan, trial, credits or generation entitlement, so it is not treated as contradictory plan evidence. If Hypernatural later provides different plan-specific evidence, a new dated change event will be recorded.

## Governance

- Store direct replies as Tier B provider fact-check evidence.
- Prefer canonical Tier A public sources where the provider identifies one.
- Provider replies never silently rewrite the 2026-08-29 historical baseline.
- Material changes become new dated events.
- If a reply conflicts with public documentation, preserve both and document the conflict.
