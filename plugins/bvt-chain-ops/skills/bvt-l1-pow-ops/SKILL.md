---
name: bvt-l1-pow-ops
description: Operates a proof-of-work L1 forked from Bitcoin or DigiByte, including multi-algorithm consensus. Use when configuring chainparams, per-algorithm difficulty retargeting, block reward and halving schedules, seed nodes and DNS seeders, wallet RPC, UTXO handling, or building and deploying the node daemon. Covers fork maintenance when rebasing on upstream Bitcoin Core.
---

# L1 (PoW, multi-algo) Operations

## Chainparams checklist
When forking or changing params, every one of these must be deliberate and consistent across mainnet/testnet/regtest:
- magic bytes / message start, default P2P and RPC ports
- genesis block (timestamp, nonce, bits, merkle root) — regenerate, never copy
- address prefixes (`PUBKEY_ADDRESS`, `SCRIPT_ADDRESS`, `SECRET_KEY`), bech32 HRP
- BIP32 ext key prefixes, BIP44 coin type
- `nSubsidyHalvingInterval`, block target spacing, difficulty retarget window
- checkpoints, `chainTxData`, assumed-valid block
- seed nodes and DNS seeders

## Multi-algorithm consensus
Each algorithm carries its **own difficulty** and its own retarget. Common design: per-algo target spacing = overall spacing × number of algos, so total block rate stays constant regardless of how hashrate distributes.

Watch for:
- **Algo hopping** — miners jumping to whichever algo is momentarily easiest. Mitigate with fast per-algo retargeting (DigiShield/MultiShield-style).
- **Reward parity** — if one algo is far cheaper per hash, it captures disproportionate reward unless difficulty adjusts sharply.
- **Version-bit encoding** — the algorithm is signalled in the block version; a mistake here forks the chain.

## Rebasing on upstream
Keep the fork's changes isolated to `chainparams.cpp`, the pow/difficulty files, and the algo dispatch. Anything smeared across the codebase makes upstream merges unmaintainable. Maintain a documented diff list.

## Ops
- Never run two daemons against one datadir.
- `-reindex` after any consensus-affecting change.
- Back up `wallet.dat` before every upgrade.
- Monitor: block height vs peers, per-algo hashrate share, mempool size, reorg depth.
