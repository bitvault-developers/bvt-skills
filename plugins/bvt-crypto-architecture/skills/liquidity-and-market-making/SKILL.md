---
name: liquidity-and-market-making
description: Plans liquidity for a new exchange or token pair. Use when designing market maker incentive programmes, internal quoting bots, automated market maker pool seeding and ratio setting, spread and depth targets, or assessing wash trading and manipulation risk.
---

# Liquidity & Market Making

## AMM seeding — the fact that governs pricing
**Price is set by the pool ratio, not the pool size.** Seeding 10 TOKEN + 100 USDC and 10,000 TOKEN + 100,000 USDC give the same starting price; only depth and slippage differ.

Consequences: choose the ratio to set the price you intend, and the size to set the slippage you can tolerate. A thin pool at the right ratio prices correctly and is trivially manipulable — which is exactly why an AMM spot price must not be used as an oracle (see `oracle-integration`).

## Depth and spread targets
Define per pair, then measure continuously:
- spread in bps at the top of book
- depth within ±0.5% and ±2% of mid
- uptime: percentage of the session with two-sided quotes inside the target spread

These are the terms a market-maker agreement should be written against — not "provide liquidity".

## Market maker programmes
- Maker rebate tiers based on measured uptime and depth, not volume alone
- Obligations stated as spread/depth/uptime with a measurement method
- Separate API keys and a distinct account kind so MM flow is identifiable in reporting
- Volume-based incentives without depth obligations reliably produce wash trading — do not ship them that way

## Internal quoting
If quoting your own book: quote around an **external reference price**, never around your own last trade (a feedback loop). Inventory limits, a maximum position per asset, and a hard kill switch. Log every quote decision — an internal MM is an operational risk and must be auditable.

## Manipulation surveillance
Detect and alert on: self-trading (blocked at the engine by STP), matched orders between related accounts, layering/spoofing (repeated placement and cancellation away from touch), momentum ignition, and wash volume concentrated in incentive windows. Retain the data — this is also a regulatory expectation, not just hygiene.
