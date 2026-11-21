---
name: bvt-branding-and-docs
description: Applies naming, attribution and documentation conventions to any external deliverable of a crypto project. Use when writing a whitepaper, documentation page, listing application, announcement or investor material. Covers canonical facts, token identities, retired names that must never be referenced, attribution, document structure and claims discipline.
---

# Branding & Documentation Conventions

## Canonical facts (fill in once, then never vary them)
Keep a short facts block for the project and copy it, word for word, into every deliverable:
- **Domain** — the one official domain. Never mention look-alike or old domains.
- **Tokens** — each token's ticker, role (utility, reward, stablecoin, governance) and identity colour.
- **Plumbing is not a token** — wrapped or bridge representations (for example a `W`-prefixed bridge token) are infrastructure. Never present them as an extra asset.
- **Protocol or layer names are not assets** — never deploy a layer name as a token or describe it as one.

## Never reference
Keep a list of retired, merged or renamed tokens and products. None of them appears in new material. If one appears in an old document being revised, remove it rather than annotating it.

## Attribution
External deliverables carry the project or team name and role designations consistently across whitepapers, repositories, listing applications, announcements and support channels. If the team uses a pseudonym, use it everywhere.

## Whitepaper / docs structure
1. Problem and positioning
2. Architecture — chain(s), layer 2, the app suite
3. Token model — utility, supply identity, fixed cap, emission and burn
4. Stablecoins — backing model, oracle, redemption
5. Bridge and supply identity (custody-backed, WBTC-style)
6. Governance — multisig + timelock
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
