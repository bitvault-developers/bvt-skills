---
name: evm-storage-surgery
description: Computes and verifies EVM contract storage slots for genesis-alloc surgery and direct state edits. Use when writing genesis.json storage overrides, computing slots for mappings, dynamic arrays, nested structs or packed variables, reading solc storage-layout JSON, or verifying slots empirically via eth_getStorageAt and eth_call on a Besu node. Encodes that storage layouts are only a hint and every slot must be confirmed against a booted test node before committing.
---

# EVM Storage Surgery

## The one rule
**Look up by hash, write by logical position.** Export files and `eth_getStorageAt` give you HASHED keys. Genesis `alloc` storage keys must be RAW LOGICAL positions — Besu hashes whatever it is given. Mixing these up silently drops data.

## Slot computation

| Kind | Position |
|---|---|
| simple var #n | `n` |
| `mapping(k => v)` value | `keccak256(pad32(key) ++ pad32(slot))` |
| dynamic array element `i` | `keccak256(pad32(slot)) + i` — **one hash, not two** |
| struct member at offset M of a mapping value | `keccak256(logical_base + M)` — a **fresh hash per member** |
| mapping of arrays | `mapPos = keccak256(pad32(key) ++ pad32(slot))` holds the **LENGTH**; elements at `keccak256(pad32(mapPos)) + i` |

`slotsPerElement = numberOfBytes(elementType) / 32`, read from the `types` map in solc's `all-layouts.json`.

## Non-negotiables
1. **Layouts are only a hint.** `all-layouts.json` comes from current SOURCE; deployed bytecode is often an older build. Locate a field empirically: scan slots 0..30 for a known value, then confirm with `eth_call` on a booted test node. (A real case: `minter` was at slot 5 on-chain while the layout said slot 8 — the most severe exposure in a remediation went unfixed until a test node exposed it.)
2. **Check `offset` for packed structs.** Two fields can share one word. A whole-word overwrite silently disabled 16 live fee configs in one incident.
3. **Zero values are never stored.** An absent slot correctly reads zero. Do not "fix" a missing slot that should be zero.
4. **Never truncate values when dumping storage.**
5. **Skipping an array element requires zeroing the length**, or a phantom entry remains.
6. **Compute selectors with `ethers.id`, never by hand.**

## Mixed keying — the defect class to watch for
State export files use **two keying conventions at once**: simple slots under LOGICAL keys `hex64(n)`, array and mapping data under HASHED keys. A migration that copies logical keys straight through is correct for simple slots and **silently skips everything hashed**. Symptom: contracts load but every array is empty — bridges with no validators, registries with no entries, multisigs with owners that read zero.

## Layout-free audit (works with no source mapping)
For any contract: treat each low slot's value as a candidate array length, compute the element positions, hash them, and check whether the export contains them. Real arrays hit. False positives (`86400`, `ReentrancyGuard._status == 1`, bps values) do not.

## Measuring completeness
Measure by **SET membership across BOTH keying conventions**. Count-based and hashed-only metrics have each produced wildly wrong answers on the same data (one reported 37.99% when the truth was 99.85%). **Trust `eth_call` over any derived statistic.** Treat a metric that contradicts a documented prior result as suspect until re-derived.

## Workflow
1. Dump storage; classify every key as logical or hashed.
2. Build the logical→value map (recovery rule above).
3. Write the alloc with logical keys.
4. Boot a **test node on a spare port with `--p2p-enabled=false`** and a temp data dir.
5. Verify each changed field by `eth_call`, not by inspection.
6. Only then cut over production.
