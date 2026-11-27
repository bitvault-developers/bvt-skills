---
name: block-explorer-architecture
description: Builds a block explorer for a proof-of-work UTXO chain and an EVM chain. Use when designing the ingestion pipeline, block, transaction, address and token pages, contract verification and source display, search, rich lists, or handling chain reorganisations in indexed data.
---

# Block Explorer Architecture

## Ingestion
Tip follower + backfill worker, both writing through the same idempotent upsert path.
- Store **block hash and parent hash**, not just height.
- Detect a reorg by parent-hash mismatch; roll back affected rows to the fork point, then re-ingest. Mark rows with the block hash so rollback is a delete-by-hash, not a heuristic.
- Checkpoint the backfill so an interrupted run resumes.
- Idempotent by `(block_hash, tx_hash, log_index)`.

## Schema (minimum)
`blocks` · `transactions` · `logs` · `addresses` · `token_transfers` · `contracts` · `balances_snapshot`.
Index on: block number, tx hash, address (from/to), token address + holder, log topic0.

## Pages
- **Block** — height, hash, timestamp, miner/validator, tx count, gas used, size, parent link
- **Transaction** — status, from/to, value, fee, gas, nonce, input decoded against the ABI, event logs decoded, internal transfers
- **Address** — balance, token balances, tx list paginated, contract tab if code exists
- **Token** — supply, holders, transfers, decimals, metadata
- **Contract** — verified source, ABI, read/write tabs
- Rich list, top tokens, search

## Search
One box resolving: block height · block hash · tx hash · address · ENS-style name · token symbol. Route by shape (length, prefix) before querying.

## Contract verification
Accept source + compiler version + optimisation settings + constructor args; compile and compare **full bytecode**, not a metadata-stripped prefix. Store the source, the ABI and the compiler settings together so the read/write tabs work.

## For a UTXO chain
Model inputs and outputs explicitly; address balance is derived from unspent outputs. Show the coinbase and its maturity. Multi-algorithm chains should display which algorithm sealed each block and per-algo difficulty.

## Operational
Track indexer lag (tip height − indexed height) and alert on it. An explorer silently 3,000 blocks behind is worse than one that is visibly down.
