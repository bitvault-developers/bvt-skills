---
name: bvt-solidity-standard
description: Authors and reviews Solidity for a token ecosystem using OpenZeppelin patterns. Use when writing or modifying contracts such as wrapped ERC-20s, a token factory, stablecoins, oracle consumers or registries, or when enforcing access control, reentrancy guards, checks-effects-interactions, SafeERC20 usage, and a two-of-three multisig plus 48-hour timelock governance convention.
---

# Solidity Standard

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
Token identity is fixed and documented: one name, ticker and role per token. Bridge or wrapper contracts are plumbing, **not** extra tokens. Retired or merged tokens are never referenced in new code or docs.
