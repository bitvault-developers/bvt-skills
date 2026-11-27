---
name: exchange-ledger-accounting
description: Designs and audits an exchange internal balance ledger using double-entry accounting. Use when modelling balances, holds and available funds, recording trades, fees, deposits and withdrawals, handling rounding and precision, or building reconciliation between the internal ledger and on-chain balances. The ledger is the source of truth and must always balance.
---

# Exchange Ledger Accounting

## Model
**Double-entry. Every entry has a matching counter-entry. The sum of all entries per asset is zero, forever.**

```
entries(id, txn_id, account_id, asset, amount /*signed int*/, created_at)
transactions(id, type, ref, created_at)   -- atomic group
accounts(id, owner_id, kind, asset)       -- kind: user | fee_income | treasury |
                                          --       hot_wallet | cold_wallet | suspense
balances(account_id, asset, total, held)  -- derived, rebuildable from entries
```
`available = total - held`. **Never store `available`** — derive it, or it will drift.

## Rules
1. **Entries are append-only.** No updates, no deletes. A correction is a new reversing transaction.
2. **Every user movement has a system counterparty.** A deposit is not "balance += x"; it is debit `hot_wallet`, credit `user`.
3. **One database transaction per logical transaction.** Partial writes are the failure that destroys an exchange.
4. **Idempotency key on every mutating operation.** A retried deposit credit must be a no-op.
5. **Integers only**, fixed scale per asset. Rounding direction is chosen once, documented, and always favours the platform's solvency (round fees up, round user credits down) — with the residual posted to a rounding account, not discarded.

## Trade settlement (one transaction)
debit taker's sold asset · credit taker's bought asset · debit maker's sold asset · credit maker's bought asset · credit `fee_income` from each side. Release the corresponding holds in the same transaction.

## Invariants to test continuously
- `SUM(amount) == 0` per asset across all accounts
- no negative `available` on any user account
- `SUM(held)` equals the sum of open-order requirements
- `SUM(user total)` per asset ≤ on-chain custodied balance for that asset
- rebuilding `balances` from `entries` reproduces the stored values exactly

Run these as a scheduled job and as a property test in CI. **A failed invariant is a P1 incident: halt withdrawals first, investigate second.**

## Suspense account
Any amount you cannot yet attribute (unexpected deposit, dust, failed sweep) goes to `suspense` — never absorbed silently and never dropped. A growing suspense balance is a bug indicator.
