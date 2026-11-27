# BVT Crypto Architecture

19 Claude skills with the architecture rules the BitVault team builds by: exchange, wallet, trading, custody, fiat, stablecoins, oracles, bridges, tokens, mining pools, explorers and indexing.

| Skill | Use it for |
|---|---|
| `block-explorer-architecture` | Builds a block explorer for a proof-of-work UTXO chain and an EVM chain. |
| `blockchain-indexing` | Indexes on-chain data for applications. |
| `bridge-architecture` | Designs and audits a custody-backed bridge between a layer one chain and a layer two chain. |
| `bvtex-exchange-architecture` | Designs a centralized crypto exchange. |
| `bvtwallet-architecture` | Builds self-custody wallet features across web, mobile and browser extension builds. |
| `custody-and-key-management` | Designs custody for exchange and treasury funds. |
| `deposit-sweeping-and-reconciliation` | Implements deposit detection, crediting and sweeping for an exchange. |
| `exchange-ledger-accounting` | Designs and audits an exchange internal balance ledger using double-entry accounting. |
| `fiat-ramp-and-card` | Integrates fiat on-ramp and off-ramp providers and crypto card issuing. |
| `india-vasp-compliance` | Translates India virtual digital asset regulatory obligations into engineering requirements. |
| `liquidity-and-market-making` | Plans liquidity for a new exchange or token pair. |
| `market-data-feeds` | Builds exchange market data distribution. |
| `matching-engine-design` | Designs and reviews an order matching engine. |
| `mining-pool-architecture` | Designs and operates a cryptocurrency mining pool. |
| `oracle-integration` | Integrates and hardens price and foreign exchange oracles for crypto protocols. |
| `stablecoin-mechanics` | Designs and maintains fiat-pegged stablecoins: a USD stablecoin backed one to one by USDC or USDT, and a local-currency stablecoin (for example INR) backed by USDC with a USD to INR foreign exchange oracle. |
| `token-listing-metadata` | Prepares token metadata and listing submissions. |
| `trading-api-design` | Designs an exchange public and private trading API. |
| `wrapped-token-factory` | Deploys and registers wrapped ERC-20 tokens through a wrapped-token factory contract. |

## Install

```text
/plugin install bvt-crypto-architecture --marketplace bitvault-developers/bvt-skills
```

Or download single skills as zips from the [latest release](https://github.com/bitvault-developers/bvt-skills/releases/latest) or the [`dist`](../../dist) folder and upload them where you add skills in Claude's settings.

## Important

These playbooks are engineering guidance, not a security audit and not legal advice. Have any exchange or wallet that holds real money audited by professionals, and check the law in every country you serve.
