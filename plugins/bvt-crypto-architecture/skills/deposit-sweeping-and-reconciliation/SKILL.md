---
name: deposit-sweeping-and-reconciliation
description: Implements deposit detection, crediting and sweeping for an exchange. Use when generating per-user deposit addresses, choosing confirmation depths, handling chain reorganisations, sweeping funds to a hot or cold wallet, covering gas for token sweeps, or running the worker that reconciles node balances against the internal ledger.
---

# Deposits, Sweeping & Reconciliation

## Address assignment
Derive per-user addresses from an HD path (`m/44'/60'/0'/0/i`), store the index, never the key. Keep an address→user map with a unique constraint. Reuse is a privacy and attribution problem; assign fresh where practical.

## Crediting
1. Watcher observes a transfer to a known deposit address.
2. Record it as **pending** with the transaction hash (unique constraint = idempotency).
3. Credit at **N confirmations**, chosen per asset and per amount; larger deposits wait longer.
4. Credit through the ledger (debit hot/deposit account, credit user) — never by mutating a balance.

## Reorgs
Track the block hash, not just the height. On reorg past a credited deposit: post a **reversing transaction**, never edit or delete the original. If the user has already traded or withdrawn, the shortfall goes to `suspense` and becomes an incident. Confirmation depth is the control that makes this rare — set it conservatively.

## Sweeping
- Trigger on a threshold, not on every deposit (fees).
- **Token sweeps need native gas at the deposit address.** Fund it, sweep, and account for the gas — a gas-funding transfer that isn't recorded shows up as an unexplained outflow.
- Sweep to warm/cold according to the tiering policy; keep the hot float within its band.
- Every sweep is a ledger transaction between system accounts.

## Non-standard arrivals
Handle explicitly: wrong asset to a deposit address, contract-initiated transfers, fee-on-transfer tokens (**credit the amount actually received, read from the event, not the amount sent**), rebasing tokens (avoid listing), dust below the credit threshold.

## Reconciliation worker
Runs continuously. For each asset: compare on-chain balance across all controlled addresses against `SUM(user total) + system accounts`.
- Difference of zero → healthy.
- Positive (chain > ledger) → uncredited deposit; investigate, post to suspense.
- **Negative (ledger > chain) → halt withdrawals immediately.** That is either an accounting bug or a loss, and both are P1.

Report the result on a fixed cadence and alert on any non-zero difference outside a documented tolerance for in-flight transactions.
