---
name: bvt-offline-sync
description: Implements offline-first encrypted local data and chain state cache invalidation for BitVault apps using SQLite. Use when caching balances, token lists, transaction history or order data on device, when the app must work without connectivity, or when reconciling cached state against the layer one and BVM layer two chains.
---

# Offline-First Data & Cache Invalidation

## Storage
- **op-sqlite** (JSI, fast) or `expo-sqlite`. **Encrypted at rest** — SQLCipher-backed, key from secure storage.
- MMKV for small non-secret key-values (settings, flags). Never for secrets.
- No secrets in the SQLite DB at all, encrypted or not: the seed lives in the keystore, full stop.

## Schema principles
Every cached row carries provenance:
```sql
CREATE TABLE balances (
  account TEXT, token TEXT, amount TEXT,      -- bigint as TEXT, never REAL
  chain_id INTEGER, block_number INTEGER, block_hash TEXT,
  fetched_at INTEGER, PRIMARY KEY (account, token, chain_id)
);
```
- **Amounts as TEXT** holding the decimal bigint. `REAL` silently destroys wei precision.
- `chain_id` in every primary key — 31338 data must never bleed into another network's view.
- `block_hash` is what makes reorg handling possible.

## Invalidation against chain state
- Cached values are stamped with the block they were read at, and the UI shows staleness once it exceeds a threshold.
- **Reorg on the PoW L1:** detect via parent-hash mismatch, then delete every cached row whose `block_hash` is on the orphaned branch and refetch. Do not patch rows in place.
- Confirmations gate display: below the threshold a transaction renders as pending, never as confirmed.
- On a chain switch or account switch, scope queries by the new key — never reuse a cached row across accounts.

## Offline behaviour
- Read paths work fully offline from cache, with a visible "last updated" marker.
- Write paths (send, subscribe, trade) are **disabled offline**, not queued — a queued signed transaction with a stale nonce broadcasts into a different world when connectivity returns. Queue the *intent* and re-derive at send time if you must.
- Sync on foreground, on network regain, and on a modest interval — not a tight poll that drains battery.

## Migrations
Versioned, forward-only, tested on a populated database. A failed migration on a wallet must fall back to **rebuilding the cache from chain**, never to data loss — the cache is derived data and should be safe to drop entirely.
