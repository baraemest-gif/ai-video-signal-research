# AI Video Signal Benchmark Methodology

## Purpose

This methodology defines how AI Video Signal records, normalizes, derives, verifies and releases market-intelligence data for AI-video providers and models.

## Scope

The current research baseline covers 14 AI-video providers. Expansion is allowed only when a provider can be represented under the same evidence, verification and normalization rules.

## Evidence hierarchy

### Tier A
First-party legal terms, pricing pages, official documentation, model documentation, official help centers and official announcements.

### Tier B
Direct provider fact-check response that identifies the factual field being confirmed.

### Tier C
Reputable external reporting used only when first-party evidence is absent, ambiguous or historically unavailable.

### Tier D
Community reports and secondary summaries used only as discovery leads, never as sole evidence for a material benchmark field.

Lower-tier evidence must not silently override higher-tier evidence. Conflicts remain visible until resolved.

## Verification rules

- Every material claim records a source and verification date.
- Historical first-party evidence may remain valid for an older immutable release even after the live provider page changes.
- Missing values are not interpreted as zero, no, unlimited or equivalent.
- Documentation review is not described as hands-on testing.
- Facts, calculations, assumptions, classifications, editorial interpretation and uncertainty remain distinct.

## Normalization states

Permitted states:

- `normalized`
- `not_normalized`
- `unclear`
- `caution`
- `unavailable`

Normalization is performed only when units are genuinely comparable. Incompatible pricing or credit systems must not be forced into a fabricated common metric.

## Approved Output Cost (AOC)

General form:

`AOC = nominal generation cost × expected attempts per approved output`

If expected attempts are not measured, the result must be labeled as a scenario or assumption, never as observed performance. Resolution, duration, model, workflow and generation mode must remain attached to the calculation.

## Pricing Volatility Index (PVI)

PVI is reserved for a future longitudinal metric based only on documented, date-stamped material pricing, credit, allowance or entitlement changes.

No PVI score should be published until sufficient historical observations exist. The eventual methodology must publish the observation window, material-change threshold, weighting logic and currency treatment before any score appears.

## Commercial Rights Evidence Status (CRES)

CRES is an evidence classification, not legal advice and not a provider quality score.

Allowed states:

- `documented_clear`
- `documented_conditional`
- `unclear`
- `restricted`
- `not_checked`

Each CRES state should retain its source, checked date, applicable plan/model/workflow and notes where needed.

## Derived calculations

Every derived value must identify:

- raw input fields
- formula
- assumptions
- unit
- applicable plan
- applicable model/workflow
- generation mode
- resolution and duration when relevant
- release identifier

If an independent reader cannot reproduce a derived value from released inputs, it is not citation-grade.

## Change control

Each material change should preserve:

- provider
- field changed
- old state
- new state
- evidence source
- evidence tier
- verification date
- reason for change
- release where the new state first appears

Historical releases are never silently overwritten.

## Provider fact-checking

Provider fact-checking improves factual accuracy but does not transfer editorial control. Providers may confirm pricing, credits, availability, entitlements or commercial-use language. They do not receive editorial veto over independently supported analysis.

## Independence

Affiliate or commercial relationships must not determine research states. The same evidence threshold applies to partner and non-partner providers, and material relationships should be disclosed where relevant.
