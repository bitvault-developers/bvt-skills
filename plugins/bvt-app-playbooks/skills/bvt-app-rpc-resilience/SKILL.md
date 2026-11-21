---
name: bvt-app-rpc-resilience
description: Builds resilient chain connectivity for BitVault apps against the layer one node and the BVM layer two, covering endpoint failover, retry and backoff, request batching, timeouts, reorg awareness and network switching. Use when writing or debugging RPC client code, handling node errors or timeouts, or adding a new chain endpoint to an app.
---

# RPC Resilience

## Multiple endpoints, always
A single RPC host is a single point of failure for the whole app. Configure an ordered list per chain (BVM L2 = chainId 31338, plus the L1 endpoint) and fail over on error, timeout, or a health check.

- Health: periodic `eth_blockNumber`; an endpoint more than N blocks behind the best-known height is **unhealthy even though it responds**. Silent lag is the dangerous failure — it returns stale balances with a 200.
- Sticky routing per session for consistency, but re-evaluate on failure.
- Track and surface which endpoint is in use in a debug screen.

## Retry policy
- Retry **idempotent reads** (`eth_call`, `eth_getBalance`, `eth_getLogs`) with exponential backoff + jitter, capped at ~3 attempts.
- **Never blind-retry `eth_sendRawTransaction`.** A timeout does not mean it wasn't broadcast. Re-query by transaction hash first; only rebroadcast the *same signed transaction* — never re-sign with a new nonce on a timeout, or you double-spend the nonce.
- Distinguish transport failure (retry) from a revert (do not retry — it will revert again).

## Timeouts
Explicit per call class: reads ~5s, `eth_getLogs` ranges ~15s, broadcast ~20s. A hung request with no timeout freezes a UI thread's dependent state forever. Every request is abortable and is aborted on unmount/background.

## Batching and rate limits
- Batch reads with `Promise.all`, but respect the node's batch limit; chunk large multicalls.
- For 909 tokens, **never issue 909 balance calls.** Use a multicall aggregator, or fetch only the user's non-zero set from an indexer and lazy-load the rest on search.
- Client-side rate limiting so a screen mount can't stampede the node.

## Chain correctness
- **Assert the chain id on every connection** and on reconnect. A silent network switch that serves data from the wrong chain is a fund-loss path.
- Include `chainId` in every cache key.
- Track block hash alongside height so a reorg is detectable (see `bvt-offline-sync`).
- Show an explicit "wrong network" state rather than rendering empty balances, which users read as "my funds are gone".

## Error mapping
Map raw provider errors to a stable `AppError` union before they reach the UI. Never render `could not coalesce error` or a raw JSON-RPC string to a user — dump the full error object to the debug log, show a mapped message.
