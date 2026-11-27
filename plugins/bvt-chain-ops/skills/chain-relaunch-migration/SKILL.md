---
name: chain-relaunch-migration
description: Migrates an EVM chain's full state into a new genesis for a relaunch or security remediation. Use when exporting storage from a live or dead chain, translating export keys into genesis alloc positions, measuring recovery completeness, restoring dynamic-array contents, or stripping authority from a compromised key. Verify every change on a booted test node before cutover.
---

# Chain Relaunch / State Migration

Companion to `evm-storage-surgery` (slot math) and `besu-clique-ops` (cutover).

## Pipeline
1. **Export** all storage from the source chain.
2. **Classify** every key: logical (`hex64(n)`) vs hashed. See `evm-storage-surgery` — this is where migrations fail.
3. **Translate** to raw logical positions for the alloc.
4. **Strip authority** (below) before writing, not after.
5. **Fold in live balances** since the last snapshot.
6. **Boot a test node**, verify by `eth_call`.
7. **Cut over** with a fresh data path.

## Authority-stripping checklist
After any key compromise, every one of these must be repointed at the timelock/multisig, and each one verified individually on the test node:
- token `minter` on every mintable token
- factory `minter` / deployer roles
- every oracle updater
- security-module `isAdmin` sets
- KYC/registry `admin`
- **every fee destination and emission destination**
- proposer/guardian on the timelock

**Never restore an original owner set verbatim** if the compromised key was in it.

## Governance bricking — the trap
If `timelock.queue()` is `onlyProposer` and the proposer **is** the multisig, then a multisig whose owners read zero makes every timelock-owned contract permanently ungovernable — `setProposer` is itself `onlyProposer`. There is no on-chain recovery. This is only fixable by genesis rewrite, which is why array restoration is not optional.

## Completeness
Report coverage as SET membership across both keying conventions. Residual unrecoverable slots are usually **string-keyed mappings** whose key strings were never recorded — these are not derivable and should be listed explicitly as known gaps rather than papered over.

## After cutover
- Back the genesis up **off-machine**. A 27MB single-copy genesis on the host it runs on is not a backup.
- Record sha256 and keep a gzipped copy.
- Commit recovery tooling with a README documenting the defect class; exclude the genesis itself (regenerable).
