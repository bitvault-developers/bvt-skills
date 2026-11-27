# BVT Smart Contracts

Seven skills for writing, upgrading and auditing EVM smart contracts, and for connecting wallets to dapps.

| Skill | What it does |
|---|---|
| `contract-upgrade-safety` | Validates that a Solidity contract upgrade preserves storage layout. |
| `ethers-v6-conventions` | Writes correct ethers.js v6 code and diagnoses EVM transaction failures. |
| `evm-storage-surgery` | Computes and verifies EVM contract storage slots for genesis-alloc surgery and direct state edits. |
| `metamask-troubleshooting` | Diagnoses MetaMask failures when interacting with a custom EVM network. |
| `mv3-extension-constraints` | Builds Chrome and Edge Manifest V3 extensions, with emphasis on crypto wallet constraints. |
| `smart-contract-audit-checklist` | Runs a pre-audit security review of Solidity contracts and produces a severity-classified report. |
| `wallet-dapp-connectivity` | Implements wallet to dapp connectivity standards. |

Written for public use: replace the example chains, tokens and app names with your own. Made by the BitVault team.

## Install

```text
/plugin install bvt-smart-contracts --marketplace bitvault-developers/bvt-skills
```

Or, in your terminal:

```bash
claude plugin install bvt-smart-contracts --marketplace bitvault-developers/bvt-skills
```

For the Claude app, download single skills as zips from the [latest release](https://github.com/bitvault-developers/bvt-skills/releases/latest) or the [`dist`](../../dist) folder and upload them where you add skills in Claude's settings.

## Important

Engineering guidance, not a security audit. Have contracts that hold real value audited by professionals before mainnet.
