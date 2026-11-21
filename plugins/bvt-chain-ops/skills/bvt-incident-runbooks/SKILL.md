---
name: bvt-incident-runbooks
description: Responds to production incidents on a blockchain project. Use when the chain halts or stops sealing, the public RPC returns errors, a tunnel drops, a wallet or exchange withdrawal path fails, funds move unexpectedly, or a key is suspected compromised. Provides triage order, diagnostic commands, containment steps and a postmortem template.
---

# Incident Runbooks

## Universal triage order
1. **Contain** — halt what can still cause loss (withdrawals, bridge, minting) before diagnosing.
2. **Establish the layer** — contract, node, network, or client. The `provider.call` + `estimateGas` split answers this in one step: both succeed → not the contract.
3. **Diagnose with the real error**, not a wrapper. Dump full error objects.
4. **Fix, verify on a test path, then apply.**
5. **Postmortem** — blameless, with the defect class named.

---

## Chain not sealing
- Confirm: is `eth_blockNumber` advancing? Peers? Node process alive?
- **Clique deadlock** — with 2 signers, a lost key halts the chain permanently (EIP-225). Fix: relaunch with 1 signer.
- Check disk space and the data path first; a full disk presents as a mystery halt.
- Do **not** wipe the data path before folding live balances into the genesis.

## Public RPC failing while node is healthy
- Count `Registered tunnel connection` in the cloudflared journal — expect 4. `is-active` is not a health check.
- Restart pattern: `stop`, wait 5s, `start`, allow 45s.
- If QUIC errors appear, set `protocol: http2`.
- Bypass test: does `http://localhost:<port>` work? If yes, the fault is the edge, not the chain.

## Transactions failing from a wallet
- Simulate server-side. Both succeed → fee, nonce, transport, or the wallet extension itself.
- Check the node's `--min-gas-price` against the wallet's computed `maxFeePerGas`.
- If MetaMask itself errors (for example a networkController crash), remove and re-add the network before debugging anything else.

## Suspected key compromise
1. **Revoke on-chain authority immediately** — every role, every fee destination.
2. Rotate.
3. Purge the key from git history (for example with `git filter-repo`) and from every backup, log and CI secret where it appeared.
4. Audit what the key could have done while exposed; assume it did.
5. Do not restore any owner set containing the compromised key.

## Ledger/backing divergence (exchange or bridge)
**Halt withdrawals first.** Then: is it in-flight timing, an uncredited deposit, or a real shortfall? Post unexplained amounts to `suspense` — never absorb, never delete. A negative divergence (ledger > chain) is P1.

## Postmortem template
Timeline (UTC) · impact · detection (how, and how long it took) · root cause · **defect class** · contributing factors · what was ruled out and why · fix applied · verification · prevention items with owners · lessons that belong in a skill file.

**Record wrong theories.** Two wrong theories were pursued in one incident before the real error object was dumped; recording that is what stops the next repetition.
