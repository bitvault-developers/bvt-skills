---
name: matching-engine-design
description: Designs and reviews an order matching engine. Use when implementing price-time priority, the in-memory order book structure, order types such as limit, market, stop, post-only, immediate-or-cancel and fill-or-kill, self-trade prevention, deterministic sequencing and replay, partial fills, or throughput and latency tuning.
---

# Matching Engine Design

## Core model
**Price-time priority.** Best price first; within a price level, earliest first.

Data structure that works: two price-indexed maps (bids descending, asks ascending), each price level holding a **FIFO queue** of orders, plus an `orderId → node` index for O(1) cancel. Array-indexed price levels beat trees when the tick grid is bounded.

Operations: insert O(1) amortised at an existing level, cancel O(1), match walks levels from the top.

## Determinism — the property everything else depends on
- **Single writer.** One thread owns the book.
- **Sequence every input** before it reaches the engine; the sequence is the order of truth.
- **No wall-clock reads, no randomness, no map iteration order** inside matching. Timestamps come in as input fields.
- **Journal inputs, not outputs.** Replaying the input sequence must reproduce the book exactly. This is how you recover, test, and settle disputes.

## Order types
| Type | Behaviour |
|---|---|
| limit | rests if unmatched |
| market | matches until filled or book exhausted; **must have slippage protection or a price band** |
| IOC | match what's available, cancel remainder |
| FOK | match fully or cancel entirely |
| post-only | reject if it would take |
| stop / stop-limit | held **outside** the book, triggered by last-trade or mark price |
| iceberg | display quantity only, refill on fill |

## Self-trade prevention
Choose one and document it: cancel-newest, cancel-oldest, or cancel-both. Do not allow an account to trade with itself — it is a wash-trading and a reporting problem.

## Precision
Integers only. Fixed-point with an explicit scale per asset. Never floats anywhere in the path. Define tick size and lot size per market and validate at the gateway.

## Circuit breakers
Price bands relative to a reference price, per-market halt state, and a documented reopening procedure (auction, not just resume).

## Performance
The engine is CPU-bound and cache-sensitive. Batch the network I/O outside it, keep the hot loop allocation-free, and measure with a replayed journal rather than synthetic load. Correctness and determinism first — a fast engine that cannot replay is unusable.
