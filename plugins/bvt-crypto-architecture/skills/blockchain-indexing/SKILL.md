---
name: blockchain-indexing
description: Indexes on-chain data for applications. Use when backfilling event logs, batching RPC calls, choosing between a custom indexer and a hosted indexing service, designing the indexed schema, handling reorganisations with idempotent upserts, or tracking indexer lag.
---

# Blockchain Indexing

## Backfill
Chunk by block range (start ~2,000 blocks, adapt down on provider errors). Checkpoint after every chunk so a crash resumes rather than restarts. Run backfill and tip-following as separate workers writing through the same upsert path.

`eth_getLogs` limits vary by provider — handle "too many results" by halving the range and retrying, not by failing the job.

## Idempotency
Primary key `(block_hash, tx_hash, log_index)`. Every write is an upsert. Then a replay of any range is harmless, which is what makes reorg recovery and backfill restarts safe.

## Reorgs
Store `block_hash` on every derived row. On a parent-hash mismatch at the tip: delete rows for the orphaned block hashes, reset the checkpoint to the fork point, re-ingest. Wait N confirmations before treating derived aggregates as final.

## RPC efficiency
- Batch JSON-RPC requests; respect the node's batch size limit.
- Filter server-side by topic and address — never fetch all logs and filter in the client.
- Cache immutable data (blocks below the reorg horizon, contract ABIs, token metadata) aggressively.
- On a self-hosted node, indexing load competes with user RPC traffic — run a dedicated node for the indexer if it matters.

## Custom indexer vs hosted (The Graph)
Custom when: you control the chain, need arbitrary schema, or need sub-second freshness.
Hosted when: standard EVM patterns, you want to avoid running infrastructure, and a subgraph's latency is acceptable. A custom chain generally needs a custom indexer — a hosted service must support the chain at all.

## Monitoring
Expose: indexed height, tip height, **lag**, rows written per minute, error rate by type, last checkpoint age. Alert on lag and on a stalled checkpoint. These two catch nearly every indexer failure.
