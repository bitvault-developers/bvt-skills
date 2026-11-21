---
name: bvt-branding-and-docs
description: Applies BitVault naming, attribution and documentation conventions to any external deliverable. Use when writing a whitepaper, documentation page, listing application, announcement or investor material. Encodes the canonical domain, token identities, removed and renamed tokens that must never be referenced, and the external attribution convention.
---

# BitVault Branding & Documentation Conventions

## Canonical facts
- Domain is **bitvault.club**. Never `.io`, never any other TLD.
- Tokens: **BVT** (utility/reward, blue) · **BRUSD** (USD-backed stablecoin, silver) · **BRINR** (INR-tracking stablecoin, green).
- **BVTW** is wrapped-BVT bridge plumbing — **not a fourth token**. Never present it as one.
- **BVLT / BVLN** is a payment-protocol *layer name only*. **Never deploy it as a token or a contract**, and never describe it as an asset.

## Never reference
- **USDV** — permanently merged into BRUSD.
- **BVTC** — removed. **BRV** was its former name. Neither appears in new material.

If either appears in an old document being revised, remove it rather than annotating it.

## Attribution
External deliverables carry the project pseudonym and role designations — never a personal legal name. Apply this consistently across whitepapers, repositories, listing applications, announcements and support channels.

## Whitepaper / docs structure
1. Problem and positioning
2. Architecture — L1 (PoW, multi-algo), BVM L2 (Clique PoA), the app suite
3. Token model — utility, supply identity, fixed cap, emission and burn
4. Stablecoins — backing model, oracle, redemption
5. Bridge and supply identity (custody-backed, WBTC-style)
6. Governance — multisig + 48h timelock
7. Security posture — audits, key management, incident history
8. Roadmap
9. Risk factors and disclaimers

## Claims discipline
- State supply mechanics precisely: fixed cap, custody-backed identity, mint/burn against backing.
- Describe price mechanics factually — AMM ratio sets price, subscription flows create recurring demand, burns offset emissions — **without projecting a price or implying a return**.
- Never describe an unaudited contract as audited, or a planned control as live.
- Distinguish clearly: shipped · in progress · planned. A roadmap item written in the present tense is a misrepresentation.
- Publish reserve/backing figures with the block or timestamp of measurement.

## Tone
Technical, specific, unhyped. Numbers with sources. No superlatives that cannot be evidenced.
