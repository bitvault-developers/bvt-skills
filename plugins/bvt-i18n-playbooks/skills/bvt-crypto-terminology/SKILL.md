---
name: bvt-crypto-terminology
description: Maintains your translation glossary and do not translate list for crypto terminology across all supported languages. Use when preparing strings for translation, configuring a term base in a translation management system, reviewing translated crypto copy, or deciding whether a term should be localized at all.
---

# Crypto Terminology & Glossary

## Never translate (do-not-translate list)
Ticker symbols: your own tokens and every listed or wrapped ticker (`BTC`, `ETH`, `USDT`, `WBTC`, `WETH`, …). A ticker is an identifier, not a word, even when a token factory adds a prefix.

Also literal, in every language:
- addresses, transaction hashes, block hashes, chain ids (`1`, `56`, `137`), derivation paths (`m/44'/60'/0'/0`)
- product and brand names: your company, app, token and network names, plus third-party ones (MetaMask, WalletConnect, Ethereum)
- units and standards: wei, gwei, ERC-20, BIP-39, BIP-32, TOTP, QR
- protocol words used as identifiers in the UI: `nonce`, `gas`, `mempool` where they name a field the user must match against a block explorer

**Rule of thumb: if the user will compare it character-for-character against another tool, it does not get translated.**

## Translate, but from the glossary — one target term per language
These have real translations and must be **consistent everywhere**, because a user who sees two different words for "wallet" in one app stops trusting it:
wallet · seed phrase / recovery phrase · private key · public key · address · send · receive · swap · stake · fee · network · confirmation · balance · order book · limit order · market order · maker · taker · deposit · withdraw · custody · non-custodial.

Ship these as a **term base** in the TMS with a definition and a forbidden-alternatives list per language. Score glossary adherence on every AI or vendor translation.

## Terms that are borrowed, not translated, in most markets
"blockchain", "token", "staking", "DeFi", "NFT" are commonly kept in Latin script or transliterated rather than calqued — including in Hindi and Arabic UI. **Ask a native reviewer per market rather than assuming**; getting this wrong reads as machine-translated and costs credibility instantly.

## Register
Financial, plain, non-promotional. Japanese needs a politeness level decided up front (です/ます for consumer finance) and held consistently — this is the most common Japanese UI translation defect. Hindi should be everyday Hindi, not Sanskritised officialese; over-formal Hindi reads as a government form, not a wallet.

## Never let terminology drift between surfaces
The glossary governs the app, the store listing, the docs, the support articles and the whitepaper. A term translated one way in the app and another in the risk disclosure is a compliance problem, not a style problem (see `bvt-regulatory-translation`).

## Maintenance
The glossary is versioned in the repo, exported to the TMS, and reviewed whenever a new product surface ships. A term added to the UI without a glossary entry is an incomplete change.
