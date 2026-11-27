---
name: smart-contract-audit-checklist
description: Runs a pre-audit security review of Solidity contracts and produces a severity-classified report. Use when hardening contracts before deployment or before an external audit, covering SWC classes, reentrancy, access control, oracle manipulation, integer and rounding issues, proxy risks, and running Slither, Mythril, Echidna and Foundry invariant tests. This is not a substitute for a human audit.
---

# Pre-Audit Checklist

**Scope note:** for general methodology, defer to Trail of Bits' `secure-workflow-guide` and `token-integration-analyzer` if installed. This skill covers protocol-specific scope and tool invocation.

## Order of operations
1. `slither . --checklist` — triage every high/medium
2. Special features review — upgradeability, ERC conformance, token integration
3. Visual inspection — inheritance and call graphs (`slither . --print inheritance-graph,call-graph`)
4. Property definition → fuzzing (Echidna / Foundry invariants)
5. Manual review of the areas tools cannot reach

## Protocol-specific scope (typical crypto protocol)
- **Governance:** can any path reach a timelock-owned function without the timelock? Is there any way to shorten or bypass the delay?
- **Bridge:** wrapped supply vs custodied backing — can they diverge? Replay protection on every proof.
- **Stablecoins:** who can mint, verified **on-chain** not from the repo layout. Redemption under a stale oracle.
- **Factory:** can a caller deploy a token that shadows an existing ticker?
- **Registries:** can an entry be repointed at an arbitrary address?

## Always-check list
Reentrancy (incl. cross-function and read-only) · access control on every mutating function · unchecked external call returns · oracle staleness · rounding direction and division-before-multiplication · unbounded loops · `delegatecall` targets · uninitialised proxies · storage collisions on upgrade · signature replay (chainId + nonce + deadline) · front-running / MEV on price-sensitive functions · pausability where funds move · event coverage of every authority change

## Report format
Per finding: **severity** (critical/high/medium/low/informational), location, description, impact, proof-of-concept or trigger condition, recommendation. Sort by severity. State explicitly what was **not** reviewed.

## Standing limitation
Automated analysis is incomplete and produces false negatives. Anything touching custody or stablecoin supply requires a human audit before mainnet. Say so in the report.
