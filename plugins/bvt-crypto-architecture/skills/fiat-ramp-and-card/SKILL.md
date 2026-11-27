---
name: fiat-ramp-and-card
description: Integrates fiat on-ramp and off-ramp providers and crypto card issuing. Use when evaluating ramp aggregators, integrating payment rails, handling settlement, chargebacks and refunds, mapping know-your-customer handoff between provider and platform, or scoping a card programme. Provider selection is constrained by jurisdiction and licensing rather than by API quality.
---

# Fiat Ramp & Card Programme

## Choose on licensing first
Rank candidates by: **jurisdictions covered · licences held · supported rails · settlement asset and timing · KYC model · fees · chargeback liability**. API quality is the last tiebreak, not the first filter. A superior API from a provider not licensed in your users' jurisdiction is unusable.

**Aggregator vs direct:** an aggregator (Onramper-style) gives many providers through one integration with fallback routing and faster launch, at a fee premium and less control. Direct integration is cheaper at volume and gives better support paths. Start with an aggregator; move high-volume corridors direct later.

## KYC handoff — decide this explicitly
Either the provider owns KYC (they verify, you receive a verified-user signal) or you do (you verify, they rely on it). **Ambiguity here is a compliance failure**, not an integration detail. Document who holds the records, who files reports, and what data crosses the boundary. For India, see `india-vasp-compliance` — your own VASP obligations do not disappear because a provider also performs KYC.

## Order lifecycle
`quote → user authorises → payment initiated → payment confirmed → crypto delivered → settled`
- Quotes expire; hold the rate for a bounded window and show the expiry.
- Webhooks are the source of truth for state. **Verify signatures, and treat every webhook as idempotent** — providers redeliver.
- Reconcile provider-reported settlements against your ledger daily.

## Rails (India context)
UPI, IMPS/NEFT/RTGS, cards. UPI is instant and low-cost but has per-transaction caps and a high dispute rate on some categories. Card payments carry **chargeback risk on an irreversible crypto delivery** — either delay delivery past the chargeback window, or accept and price the loss. Decide deliberately.

## Off-ramp
Payouts to a **bank account verified as belonging to the KYC'd user**. Name matching is mandatory. Off-ramp is where AML scrutiny concentrates; apply source-of-funds checks above thresholds and screen the destination.

## Card programme
You will need a BIN sponsor and an issuer processor. Scope: authorisation flow (real-time balance/crypto conversion at auth time), settlement funding, decline handling, disputes, PCI scope (aim to stay out of it via the processor), and a spend-control ruleset. This is a licensed-partner project with a long lead time — start the partner conversation before the engineering.
