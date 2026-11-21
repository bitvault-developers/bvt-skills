---
name: bvt-solidity-standard
description: Authors and reviews Solidity for the BitVault ecosystem using OpenZeppelin patterns. Use when writing or modifying contracts such as wrapped ERC-20s, the token factory, the BRUSD and BRINR stablecoins, oracle consumers or registries, or when enforcing access control, reentrancy guards, checks-effects-interactions, SafeERC20 usage, and the two-of-three multisig plus 48-hour timelock governance convention.
---

# BitVault Solidity Standard

## Defaults
- Solidity: pin an exact version, never a caret range, in production contracts.
- Use **OpenZeppelin** implementations rather than hand-rolled ones. Prefer generating via the OpenZeppelin Contracts MCP over writing from memory.
- `AccessControl` with named roles for anything multi-actor; `Ownable2Step` only for single-owner contracts.
- `SafeERC20` for every external token call. Never trust a bare `transfer` return.
- `ReentrancyGuard` on any function that makes an external call before finalising state.
- **Checks → Effects → Interactions**, always, even where a guard exists.
- Custom errors over revert strings.
- Emit an event for every state change that off-chain systems track.

## Governance convention
Ownership of production contracts belongs to the **AdminTimelock** (48h delay, 14d grace), whose proposer and guardian is the **2-of-3 multisig**. See `bvt-governance-flow` for the execution path.

Deliberate exceptions must be documented in the contract's NatSpec with the reason — e.g. a registry whose owner is still the deployer because it must be populated before handover. Call `setOwner(timelock)` only **after** population.

## Review checklist
- [ ] No unbounded loop over user-controlled length
- [ ] No `delegatecall` to a non-constant target
- [ ] Every external call's return value handled
- [ ] Oracle reads have staleness + round-completeness checks
- [ ] Division before multiplication eliminated; rounding direction chosen deliberately and documented
- [ ] Access control on every state-mutating external function
- [ ] Pausability where funds move
- [ ] Upgrade path checked: storage layout unchanged or append-only, initializers protected, no selector clashes
- [ ] Events cover every balance/authority change

## Naming and constants
Token colours and identity are fixed: BVT (utility), BRUSD (USD-backed), BRINR (INR-tracking). BVTW is bridge plumbing, **not** a fourth token. USDV and BVTC are removed — never reference them in new code or docs.
