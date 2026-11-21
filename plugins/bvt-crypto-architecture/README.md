# BVT Crypto Architecture

Two Claude skills with the architecture rules the BitVault team builds by.

| Skill | Use it for |
|---|---|
| `bvtex-exchange-architecture` | Planning a centralized crypto exchange: component map, order lifecycle, accounts and balances, fees, and a safe build order (ledger and custody before the matching engine). |
| `bvtwallet-architecture` | Building a self-custody wallet for web, mobile and browser extensions: BIP-39 seed and derivation, encrypted storage per platform, auto-lock, TOTP 2FA, the send flow and the security copy that must not be softened. |

## Install

```text
/plugin install bvt-crypto-architecture --marketplace bitvault-developers/bvt-skills
```

Or download `bvtex-exchange-architecture.zip` and `bvtwallet-architecture.zip` from the [`dist`](../../dist) folder and upload them where you add skills in Claude's settings.

## Important

These playbooks are engineering guidance, not a security audit and not legal advice. Have any exchange or wallet that holds real money audited by professionals, and check the law in every country you serve.
