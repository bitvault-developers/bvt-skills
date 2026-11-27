---
name: contract-upgrade-safety
description: Validates that a Solidity contract upgrade preserves storage layout. Use when modifying an already-deployed contract, adding state variables, reordering or removing fields, changing struct packing, or choosing between UUPS, transparent and non-upgradeable patterns. Deployed bytecode is often an older build than the current source, so layouts must be confirmed against the chain rather than the repository.
---

# Contract Upgrade Safety

## The rule
An upgrade may **append** state variables. It may not reorder, remove, retype, or repack existing ones.

## Illegal without a migration
- inserting a variable before an existing one
- deleting a variable (leaves the slot occupied; the next append collides)
- changing a type's size (`uint128` → `uint256` breaks packing of its neighbours)
- changing inheritance order (changes base-contract slot ordering)
- adding a variable to a base contract without a reserved gap

## Storage gaps
Every upgradeable base contract gets `uint256[50] private __gap;`. When adding a variable to that base, **decrement the gap by the number of slots consumed** in the same change.

## Verify against the chain, not the repo
`all-layouts.json` reflects current SOURCE. The deployed contract may be an older build.
1. Fetch deployed bytecode; compare **FULL keccak hashes**, never metadata-stripped prefixes — a stripped prefix once falsely matched two different 2074-byte contracts.
2. If the hash does not match any build, locate fields empirically (scan slots for known values) and confirm by `eth_call`.
3. Prefer `contracts/` over any `_unused_contracts/` when resolving source.

## Pattern choice
- **Non-upgradeable** — default for anything that can be redeployed and re-pointed.
- **UUPS** — cheaper; upgrade logic lives in the implementation, so a bad implementation can brick upgradeability. Always keep an authorised upgrade path tested.
- **Transparent** — heavier, upgrade logic in the proxy, harder to brick.
- **Diamond** — only with a strong reason; the complexity cost is real.

## Pre-upgrade checklist
- [ ] Layout diffed old vs new, appends only
- [ ] Gaps decremented
- [ ] Initialiser cannot be re-run (`reinitializer` version bumped)
- [ ] Implementation constructor `_disableInitializers()`
- [ ] Upgrade goes through the timelock
- [ ] Upgrade rehearsed against a fork before mainnet
