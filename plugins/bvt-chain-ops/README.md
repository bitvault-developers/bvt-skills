# BVT Chain Ops

Nine operations skills for running a blockchain project: contracts, governance, PoW and Besu Clique nodes, chain relaunches, the public edge, incidents, repo hygiene and docs.

| Skill | What it covers |
|---|---|
| `besu-clique-ops` | Operates Hyperledger Besu nodes running Clique proof-of-authority consensus. |
| `bvt-branding-and-docs` | Applies naming, attribution and documentation conventions to any external deliverable of a crypto project. |
| `bvt-edge-ops` | Exposes and troubleshoots public endpoints (RPC, APIs, websites) through cloudflared tunnels and nginx. |
| `bvt-governance-flow` | Executes changes through a two-of-three multisig and a 48-hour timelock. |
| `bvt-incident-runbooks` | Responds to production incidents on a blockchain project. |
| `bvt-l1-pow-ops` | Operates a proof-of-work L1 forked from Bitcoin or DigiByte, including multi-algorithm consensus. |
| `bvt-solidity-standard` | Authors and reviews Solidity for a token ecosystem using OpenZeppelin patterns. |
| `chain-relaunch-migration` | Migrates an EVM chain's full state into a new genesis for a relaunch or security remediation. |
| `repo-ops-hygiene` | Keeps repositories free of secrets and safe to publish. |

Written for public use: replace the example tokens, chains and app names with your own. Made by the BitVault team.

## Install

```text
/plugin install bvt-chain-ops --marketplace bitvault-developers/bvt-skills
```

Or, in your terminal:

```bash
claude plugin install bvt-chain-ops --marketplace bitvault-developers/bvt-skills
```

For the Claude app, download single skills as zips from the [latest release](https://github.com/bitvault-developers/bvt-skills/releases/latest) or the [`dist`](../../dist) folder and upload them where you add skills in Claude's settings.

## Important

Engineering guidance, not a security audit and not legal advice. Have contracts and infrastructure that hold real value audited by professionals.
