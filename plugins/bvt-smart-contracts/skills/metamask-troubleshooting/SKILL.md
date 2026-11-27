---
name: metamask-troubleshooting
description: Diagnoses MetaMask failures when interacting with a custom EVM network. Use when a transaction fails in the wallet but simulates fine server side, when errors appear that the node never logged, or after repeated edits to a network configuration. Encodes the network controller crash caused by a dangling network client id and the correct recovery path.
---

# MetaMask Troubleshooting (custom networks)

## Step 1 — establish where the failure is
```js
await provider.call({ from, to, data });
await provider.estimateGas({ from, to, data });
```
Both succeed → the contract is fine. The failure is in the wallet, the fee, the nonce, or transport. **The node logging nothing is a strong signal the transaction was never built.**

## Step 2 — dump the real error
`shortMessage` and "could not coalesce error" tell you nothing. Dump `e.code`, `e.info.error`, `e.error`, `e.data` with full depth.

## Known failure: dangling networkClientId
**Signature:** `code -32603` wrapping
`TypeError: Cannot destructure property 'chainId' of 'this.networkController.getNetworkConfigurationByNetworkClientId(...)' as it is undefined`, thrown at `getAddTransactionRequest`.

**Cause:** the extension crashes **before building the transaction**. Repeated network editing (delete, re-add, change RPC URL) leaves the `networkController` holding a client id that no longer resolves.

**Recovery, in order:**
1. Toggle the extension off/on at `chrome://extensions` to reinitialise the controller.
2. Full Chrome restart.
3. **Delete and re-add the network once** — network selector → Manage networks → ⋮ next to the network → **Delete** → then **Add a custom network** fresh with ONE RPC URL. Then stop editing it.

Note that the Edit screen greys out chain ID, so "editing" never clears the stale id — deletion is the only path.

## Known failure: fee below the node floor
Type-2 fees derived from a collapsed `baseFeePerGas` can land below the node's `--min-gas-price`, so the node rejects before mining and logs nothing. Set `--min-gas-price=0` on a private chain, or pin fee fields client-side. (This is a real failure mode, but confirm it with the error dump rather than assuming it — it has been misdiagnosed as the cause when the real fault was the controller crash above.)

## Hygiene
- Change a network's config as rarely as possible.
- Chain ID is immutable on an existing network; RPC URL is not.
- Hex data field is hidden by default: Settings → Advanced → "Show hex data".
