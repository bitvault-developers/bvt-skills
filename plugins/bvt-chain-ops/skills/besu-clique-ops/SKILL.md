---
name: besu-clique-ops
description: Operates Hyperledger Besu nodes running Clique proof-of-authority consensus. Use when editing genesis.json including extraData signer sets, chainId and config, managing signers via clique_propose, setting min-gas-price, resetting the data path, writing or repairing systemd units for Besu, or diagnosing a chain that has stopped sealing. Encodes the EIP-225 two-signer deadlock, the fresh-data-path requirement for any alloc change, and folding live balances into a new genesis before cutover.
---

# Besu / Clique PoA Operations

Typical target: a private EVM chain on Clique PoA (for example 5 s blocks and one or two signers).

## Genesis
`extraData` = 32-byte vanity ++ concatenated 20-byte signer addresses ++ 65-byte seal (zeros in genesis).
`config.clique`: `blockperiodseconds`, `epochlength`.

## The two hard rules

**1. A genesis alloc edit needs a FRESH data path.**
Besu will not re-read the alloc into an existing database; it refuses to start on a genesis hash mismatch. Any alloc change therefore means a chain reset to block 0.

**2. Any live transaction since the last cutover is LOST unless folded into the genesis first.**
Fold balances in by writing live values into the alloc and deducting from the sender so total supply is unchanged. Do this *before* the reset, never after.

## The EIP-225 deadlock
With 2 Clique signers, a block sealed by signer A requires signer B to seal an intervening block. If one signer's key is lost, the chain **halts permanently** — no timeout, no recovery. Fix: relaunch with exactly 1 signer, or restore the missing key. Symptom: chain stuck at a fixed height, node healthy, no errors.

## min-gas-price
On a private chain, set `--min-gas-price=0`. Otherwise: when blocks empty out, `baseFeePerGas` decays toward 7 wei, wallets compute a `maxFeePerGas` below Besu's default `--min-gas-price` (1000 wei), and transactions are rejected **before mining** — so the node logs nothing and the contract simulates fine.

## systemd
- `/etc/systemd/system/` is root-owned: write to `/tmp`, then `sudo cp`.
- **Preserve EXACT file structure.** Reconstructing a unit from memory once merged a directive into a backslash-continued `ExecStart` and crashed with "Unmatched argument".
- Use targeted `sed` against a known-working backup and **verify the diff shows only the intended lines**.
- `systemctl restart`, never `kill` — `Restart=on-failure` wins port races.
- Back up before every change: `besu.service.backup-pre-<change>`.

## Test before cutover
Run any new `ExecStart` standalone on spare ports first: temp data dir, `--p2p-enabled=false`, RPC on 18999. Production is untouched.

## Checklist for a cutover
1. Fold live balances into the alloc.
2. Back up the unit file and the current genesis.
3. Boot on spare ports; verify by `eth_call`.
4. `systemctl stop`, swap data path, `systemctl start`.
5. Confirm sealing (`eth_blockNumber` advancing) and the public endpoint.
