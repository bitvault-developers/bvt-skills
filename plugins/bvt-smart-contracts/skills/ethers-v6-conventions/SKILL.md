---
name: ethers-v6-conventions
description: Writes correct ethers.js v6 code and diagnoses EVM transaction failures. Use when computing function selectors, distinguishing provider.call from estimateGas for revert diagnosis, building EIP-1559 type-2 transactions, decoding custom-error reverts, or fixing version 5 to version 6 migration issues. Encodes that a coalesce error is a wrapper rather than a diagnosis and that the full error object must be dumped before theorising.
---

# ethers.js v6 Conventions

## Selectors — never guess
```js
const sel = ethers.id("approve(uint256)").slice(0, 10);
```
Three selectors were guessed wrong in a single session and each cost hours. Compute, then verify by decoding a known-good transaction.

## The diagnosis split (use this first, every time)
```js
await provider.call({ from, to, data });   // does the contract revert?
await provider.estimateGas({ from, to, data });
```
- Both **succeed** → the contract is fine. The problem is **fee, nonce, transport, or the wallet itself**. Stop reading Solidity.
- `call` **reverts** → decode the revert data; the problem is contract state or arguments.

This split eliminates most of the guessing on a failed wallet transaction.

## "could not coalesce error" means nothing
It is ethers saying the RPC error could not be normalised. It is a **wrapper, not a diagnosis**. Before forming any theory, dump:
```js
console.dir({ code: e.code, info: e.info, error: e.error, data: e.data, shortMessage: e.shortMessage }, { depth: 8 });
```
A real case: the wrapper hid `code -32603` containing a `TypeError` thrown **inside the MetaMask extension** — the node had logged nothing because no transaction was ever built. See `metamask-troubleshooting`.

## v5 → v6 changes that bite
| v5 | v6 |
|---|---|
| `BigNumber` | native `bigint` — no `.add()`, use `+` |
| `ethers.utils.parseEther` | `ethers.parseEther` (namespace flattened) |
| `ethers.providers.JsonRpcProvider` | `ethers.JsonRpcProvider` |
| `contract.functions.foo()` | `contract.foo()` |
| `await contract.deployed()` | `await contract.waitForDeployment()` |
| `contract.address` | `await contract.getAddress()` |
| `provider.getGasPrice()` | `(await provider.getFeeData()).gasPrice` |

`Result` objects are array-like and frozen — spread before mutating.

## Fees on a private chain
Type-2 transactions compute `maxFeePerGas` from `baseFeePerGas`. On an idle chain the base fee decays toward 7 wei, which can fall **below the node's `--min-gas-price`**, and the node rejects before mining with no log. Either set `--min-gas-price=0` on the node or pin explicit fee fields client-side.

## Misc
- `await tx.wait()` returns `null` on a replaced transaction — check for it.
- Decode custom errors with the contract interface: `iface.parseError(e.data)`.
- Batch reads with `Promise.all`, but respect the RPC's batch limit.
