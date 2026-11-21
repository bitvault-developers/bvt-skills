# BVT Chain Ops

Six operations skills from the BitVault team for running a blockchain project: contracts, governance, the node, the public edge, incidents and docs.

| Skill | What it covers |
|---|---|
| `bvt-branding-and-docs` | Applies BitVault naming, attribution and documentation conventions to any external deliverable. |
| `bvt-edge-ops` | Exposes and troubleshoots BitVault public endpoints through cloudflared tunnels and nginx. |
| `bvt-governance-flow` | Executes changes through BitVault's two-of-three multisig and 48-hour AdminTimelock. |
| `bvt-incident-runbooks` | Responds to BitVault production incidents. |
| `bvt-l1-pow-ops` | Operates the BitVault proof-of-work L1, a DigiByte and Bitcoin-derived chain with multi-algorithm consensus. |
| `bvt-solidity-standard` | Authors and reviews Solidity for the BitVault ecosystem using OpenZeppelin patterns. |

These are the playbooks the BitVault team uses for its own apps, so examples name BitVault's tokens and chains (BVT, BRUSD, BRINR, the BVM L2). The rules apply to any similar project.

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
