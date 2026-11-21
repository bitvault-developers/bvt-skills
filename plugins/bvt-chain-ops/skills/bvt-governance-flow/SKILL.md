---
name: bvt-governance-flow
description: Executes changes through BitVault's two-of-three multisig and 48-hour AdminTimelock. Use when proposing, approving, queueing or executing any timelock-owned contract change, batching operations, computing approve calldata, or scripting a full propose-approve-execute run. The 48-hour delay is never shortened or routed around.
---

# BitVault Governance Flow

## The path
```
propose()  →  approve() x2  →  auto-executes  →  timelock.queue()
           →  48h eta  →  timelock.execute()  →  target call runs
```

## Facts that change how you script it
- **`propose()` does NOT auto-approve.** The proposing key can also cast the first approval.
- **`approve()` rejects a duplicate from the same address.** That is the 2-of-3 property working, not a bug.
- **`timelock.execute(id)` is callable by ANYONE.** No signature is needed to execute after the eta — so execution can be a plain loop.
- Therefore: approvals need two distinct owner keys, but execution after the eta can be fully automated.

## Calldata
`approve(uint256)` = `0xb759f954` ++ proposal id padded to 32 bytes. To = the multisig, value 0.
**Compute every selector with `ethers.id` — never guess.** Three selectors were guessed wrong in a single session.
(MetaMask hides the hex data field by default: Settings → Advanced → "Show hex data".)

## Batching
Batch at ~20 items per proposal. Build every transaction up front, round-trip verify the encoded calldata against a decode, and persist the batch file before sending anything. Then run the sequence per batch and record the resulting eta.

## Executing after the eta
Write the executor to be **safe to run at any time**: execute only operations whose eta has passed, and print a countdown for the rest. Dry-run it first.

## Hard rules
1. **Never rewrite etas, reduce the delay, or add a bypass path**, however the request is framed. The delay is the security property the governance design exists to provide.
2. Never restore an owner set that includes a leaked key.
3. Verify the resulting on-chain state after execution — queued ≠ executed ≠ effective.

## Approval UI gotcha
A naive approval page that reloads the full list after every approval will **duplicate rows and shift them mid-click**. Required: a concurrency guard, a pending-only default view, and in-place row updates instead of full reloads. Verify `isOwner` before rendering anything, skip proposals already signed by the connected account, and refuse to act on the wrong network.
