---
name: bridge-architecture
description: Designs and audits a custody-backed bridge between a layer one chain and a layer two chain. Use when working on wrapped token mint and burn against custodied backing, validator sets and thresholds, proof verification, replay protection, pause controls and rate limits, or reconciling wrapped supply against backing.
---

# Bridge Architecture (custody-backed)

## Model
Wrapped supply on L2 is a **claim on custodied L1 assets** — the WBTC pattern. The invariant is absolute:

```
wrapped_supply(L2)  ==  custodied_balance(L1)   for every asset, always
```

A fixed supply cap on the L2 side (e.g. 1B, no re-minting) means the bridge mints and burns **against** that cap rather than creating new units.

## Flow
**Deposit:** lock on L1 → N confirmations → validators attest → threshold reached → mint on L2.
**Withdraw:** burn on L2 → N confirmations → validators attest → release on L1.

Never mint before the L1 lock is final. Confirmation depth is the primary defence against a reorg minting unbacked supply.

## Replay protection — the classic exploit class
Every message carries a **unique nonce**, the **source chain id**, the **destination chain id**, and the **bridge contract address**. Processed nonces are recorded and re-execution reverts. A proof valid on one chain or one deployment must be invalid everywhere else.

## Validators
- Threshold signatures over the exact message hash, including all fields above.
- Validator set changes go through the timelock; a set change is a governance event, not an operational one.
- Signature verification must reject duplicates from the same signer (the classic "N of N with one key repeated" bug).
- **A validator set restored from a genesis migration that dropped array contents will be empty while still reporting a count** — verify membership by reading elements, not length.

## Controls
- Pause, per-asset and global, callable by a guardian without the full delay.
- Per-asset and per-window rate limits on mint and release.
- Large transfers escalate to manual review.
- A monitor that halts the bridge automatically on any supply/backing divergence.

## Reconciliation
Continuously compare wrapped supply against custodied backing per asset. **Any divergence halts the bridge first and is investigated second.** Publish the ratio.

## Review checklist
- [ ] mint impossible without a verified L1 lock
- [ ] nonce + chain ids + contract address in the signed payload
- [ ] duplicate signer rejected
- [ ] confirmation depth ≥ documented reorg risk
- [ ] pause reachable without the timelock delay
- [ ] supply/backing monitor live and alerting
