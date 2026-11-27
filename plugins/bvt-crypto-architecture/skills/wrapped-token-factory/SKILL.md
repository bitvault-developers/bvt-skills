---
name: wrapped-token-factory
description: Deploys and registers wrapped ERC-20 tokens through a wrapped-token factory contract. Use when batch-deploying tokens, populating the token registry or backing registry, or preparing deployment manifests. The factory prepends its own prefix, so pass nativeTicker rather than symbol; registry entries restored from a genesis point at stale addresses and must be repointed after deployment.
---

# Wrapped Token Factory

## The prefix trap
**Pass `nativeTicker`, NOT `symbol`.** The factory prepends its own prefix itself (for example `W`). Passing an already-prefixed symbol yields a double prefix such as `WW…` — wrong on every token in the batch, and only visible after deployment.

## Source of truth
The deployment manifest (a `deployed.json`-style file) is authoritative for the token set. **Verify addresses have code** before trusting any "N of M done" figure — a manifest can claim progress for addresses that were never deployed.

Known metadata gaps: no `coingeckoId` and no `logoURI` in the manifest. `nativeTicker` stands in for the CoinGecko id; `logoURI` is empty and must be filled by the logo pipeline (see `token-listing-metadata`).

## Deployment
1. Build all `propose()` transactions up front; round-trip verify.
2. Batch ~20 tokens per proposal.
3. Run the governance flow per batch (see `bvt-governance-flow` in the bvt-chain-ops plugin).
4. After the eta, `timelock.execute(id)` per operation → `factory.batchDeploy` runs.
5. Record the deployed addresses.

## Registry repointing — do not skip
A registry restored from a genesis will report the right **count** while every entry points at a **stale address from the old chain**. `totalTokens()` reading the expected number proves nothing.

After deployment:
1. `batchRegister` the NEW addresses into the token registry (batches of ~30, through the same governance flow).
2. Populate the backing registry — if its owner is still the deployer, no timelock delay applies, so do it directly.
3. Call `setOwner(timelock)` on the backing registry **only after** population.
4. Spot-check by resolving several tickers end-to-end and confirming code exists at each address.

## Gas
Batch deploys are cheap on a private chain with `--min-gas-price=0`; do not let a gas estimate scare you off a correct batch size. Do confirm the block gas limit accommodates the batch.
