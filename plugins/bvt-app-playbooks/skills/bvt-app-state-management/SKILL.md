---
name: bvt-app-state-management
description: Structures client state for crypto apps — server and chain state via a query cache, ephemeral UI state locally, and persisted user state in encrypted storage. Use when adding stores, caching chain reads, handling loading and error states, or deciding where a piece of state belongs across the mobile, desktop, web and extension shells.
---

# App State Management

## Three buckets, three tools
| Bucket | Examples | Tool | Persisted? |
|---|---|---|---|
| **Server / chain state** | balances, token list, tx history, order book | TanStack Query | cache only, revalidated |
| **Client state** | selected account, theme, filters, lock status | Zustand | some, non-secret only |
| **Secret state** | seed, keys, session unlock | `SecureStore` port | encrypted, never in a store |

**Secrets never enter a state store.** Not Zustand, not Query cache, not Redux devtools, not a persisted atom. A store is serialized, logged, and dev-inspected — all three leak.

## Chain state rules
- Key every query by `[chainId, account, block-relevant-input]`. The chain id in the key prevents cross-network bleed after a switch.
- Balances are `staleTime: 0` with a block-height watermark; a cached balance shown as current after a reorg is a correctness bug, not a UX one.
- Pending transactions live in their own store with an explicit state machine: `building → signed → broadcast → pending → confirmed | replaced | failed`. `tx.wait()` returning `null` means **replaced** — handle it, don't treat it as failure.
- Optimistic updates are allowed for UI affordances, **never for a balance**.

## Cross-shell portability
Stores live in `packages/business` and are platform-free. Persistence is injected by the shell (MMKV/op-sqlite on mobile, Tauri store on desktop, `chrome.storage` in the extension). Core defines the interface, shells supply it.

## Lock behaviour
On lock, background, or timeout: clear the unlocked key, clear any query cache holding account-scoped data, and reset navigation to the lock screen. **Clearing the UI without clearing the cache leaves balances and addresses readable after lock.**

## Anti-patterns
- One global store holding everything — becomes an untestable god object.
- Deriving balance in a selector from multiple caches — race conditions on refetch.
- Storing a formatted string in state and parsing it back.
- Persisting the whole store blindly; enumerate exactly what persists.
