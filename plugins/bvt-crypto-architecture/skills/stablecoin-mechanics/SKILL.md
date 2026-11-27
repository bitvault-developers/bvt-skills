---
name: stablecoin-mechanics
description: Designs and maintains fiat-pegged stablecoins: a USD stablecoin backed one to one by USDC or USDT, and a local-currency stablecoin (for example INR) backed by USDC with a USD to INR foreign exchange oracle. Use when working on mint and burn paths, collateral accounting, reserve attestation, peg defence, redemption flows, or supply and exposure audits.
---

# Stablecoin Mechanics

## Model
- **USD stablecoin** — USDC- or USDT-backed 1:1. Supply may only increase against verified collateral received.
- **Local-currency stablecoin** (for example INR) — USDC-backed with a USD/INR FX oracle determining the peg. Two risks stack: collateral risk *and* oracle risk.
- **Retire old units cleanly.** When a stablecoin is merged into another, say so publicly and stop referencing the old one.

## Invariants to enforce in code and monitor off-chain
1. `totalSupply <= collateral_value_at_current_rate` at all times.
2. Mint requires proof of collateral receipt; burn releases collateral. No path mints without a corresponding deposit.
3. `minter` is a single, timelock-controlled address. **Verify on-chain where `minter` actually lives** — the storage layout in the repo may not match deployed bytecode.
4. Pause must halt minting without halting redemption.

## Redemption
Redemption is the peg. Design it first, not last:
- fixed, published redemption fee (or zero)
- redemption queue with a bounded worst-case delay
- per-address and global daily caps
- a documented behaviour when the oracle is stale (halt redemption at the last good rate rather than execute at a bad one)

## FX oracle handling for the local-currency stablecoin
See `oracle-integration`. Minimum: reject stale rounds, reject non-positive answers, bound the per-update move, and fall back to the last good rate with an explicit halt rather than a silent stale read.

## Exposure audit
Periodically report: supply, holder distribution, and how much sits in deployer/protocol contracts vs external accounts. A supply concentrated in protocol-controlled addresses is a **distribution** fact, not automatically a solvency problem — state it as such, and report the collateral ratio separately.

## Attestation
Publish, on a fixed cadence: supply, collateral held, custodian, ratio, and the block/timestamp of measurement. Reserve attestation is a product feature; treat a missed cadence as an incident.
