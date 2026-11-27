---
name: mining-pool-architecture
description: Designs and operates a cryptocurrency mining pool. Use when implementing the Stratum protocol, job distribution and share validation, variable difficulty, reward schemes such as PPLNS, PPS and proportional, payout batching and thresholds, orphan and stale share handling, or a pool admin dashboard. Covers multi-algorithm pools where each algorithm carries its own difficulty.
---

# Mining Pool Architecture

## Stratum
V1 methods: `mining.subscribe` · `mining.authorize` · `mining.notify` (job) · `mining.submit` (share) · `mining.set_difficulty` · `mining.set_extranonce`.
Line-delimited JSON-RPC over TCP. Stratum V2 adds encryption and job negotiation — worth targeting for new pools, but V1 compatibility is still required in practice.

## Job flow
1. Poll the node (`getblocktemplate`) or take a block-notify push.
2. Build the coinbase with the pool payout output plus extranonce placeholders.
3. Broadcast `mining.notify` with `clean_jobs=true` on a new block — **stale jobs cost miners money and reputation**; latency here is the pool's core quality metric.
4. Validate submitted shares: reconstruct the header, hash with the correct algorithm, compare against the miner's assigned difficulty.
5. If a share also meets **network** difficulty, submit the block immediately.

## Share validation — reject reasons to track separately
duplicate · stale (old job) · low difficulty · invalid job id · unauthorised worker · bad extranonce.
A rising rate in any one of these is a distinct fault; a single "rejected" counter hides all of them.

## Vardiff
Target a fixed share submission rate per worker (commonly ~1 share / 5–20s). Adjust gradually with a retarget window; clamp min/max. Too low floods the pool; too high makes small miners' income lumpy and unverifiable.

## Multi-algorithm
Each algorithm has its own difficulty, its own job stream, and usually its own port. Track hashrate, share rate and luck **per algorithm**. Do not average difficulty across algorithms in reporting — it is meaningless.

## Reward schemes
| Scheme | Pool risk | Miner variance | Notes |
|---|---|---|---|
| PROP | none | high | per-round proportional |
| PPLNS | low | medium | last N shares; **discourages pool hopping** |
| PPS | high | none | pool absorbs variance; needs a funded buffer |
| FPPS | high | none | PPS plus fee share |

Start with PPLNS unless you can fund a PPS buffer and model ruin risk.

## Payouts
- Batch on a threshold and/or a schedule; never one transaction per share.
- Mature coinbase outputs before paying (100 blocks on Bitcoin-derived chains).
- **Orphaned blocks must reverse the round** — pay from matured balances only.
- Keep an immutable payout ledger; miners will audit it and should be able to.

## Admin dashboard
Pool hashrate (per algo), active workers, share/reject rates by reason, block finds with luck %, orphan rate, pending vs paid balances, node health and height vs peers.
