---
name: bvtex-exchange-architecture
description: Designs a centralized crypto exchange. Use when planning or building spot trading, service boundaries, order lifecycle, account and sub-account models, fee tiers, listing workflow, or the overall data flow between matching engine, ledger, custody and market data. Start here before designing any single component.
---

# Crypto Exchange Architecture

## Component map
```
client ──▶ API gateway ──▶ risk/limit check ──▶ matching engine (single writer)
                │                                      │
                ▼                                      ▼
            ledger  ◀───────── trade events ──────  sequencer/journal
                │                                      │
                ▼                                      ▼
        custody / wallet svc                    market data fanout
                │
                ▼
        deposit watcher, sweeper, withdrawal approver
```

## Non-negotiable properties
1. **The ledger is the source of truth**, not the chain and not the engine's memory.
2. **The engine is a single writer and deterministic** — same input sequence, same output, replayable from the journal.
3. **Every order is checked against available balance before it reaches the engine.** The engine must never need to reject for funds.
4. **On-chain movement is a consequence of a confirmed ledger entry**, never its cause.

## Order lifecycle
`new → risk check → hold placed on ledger → accepted → resting | partially filled | filled | cancelled | expired`
Each transition emits an event. Fills settle atomically: debit taker asset, credit maker asset, both sides, plus fee entries, in one ledger transaction.

## Accounts
- user → sub-accounts (spot, and later margin/futures)
- balance = `total`, `available`, `held`; `available = total - held` always
- internal system accounts: fee income, insurance, treasury, and a **suspense** account so an unexplained difference is recorded rather than absorbed

## Fees
Maker/taker basis points by 30-day volume tier. Charge in the received asset by default. Store fee entries as separate ledger lines — never net them into the trade line, or reporting becomes impossible.

## Build order
1. Ledger + accounts (with invariant tests)
2. Deposit watcher (credit only, no trading)
3. Withdrawal with manual approval
4. Matching engine + order API
5. Market data feeds
6. Fee tiers, sub-accounts, advanced order types

Ship 1–3 and run them with real funds in a small circle before 4 exists. An exchange that cannot custody correctly does not need a matching engine yet.

## Compliance is structural
KYC state, tax withholding (for example India's 1% TDS on crypto transfers) and Travel Rule data must be in the schema from the first migration. Check the rules of every country you serve with a qualified lawyer. Retrofitting them into a live ledger is far worse than designing for them.
