---
name: custody-and-key-management
description: Designs custody for exchange and treasury funds. Use when splitting hot, warm and cold tiers, choosing between multisig, multi-party computation and hardware security modules, defining withdrawal approval thresholds, setting allowlists and velocity limits, planning key ceremonies, rotation and disaster recovery, or reviewing how signing keys are stored on a server.
---

# Custody & Key Management

## Tiering
| Tier | Share | Control | Purpose |
|---|---|---|---|
| hot | 2–5% | automated signing | instant withdrawals |
| warm | 5–10% | multisig or MPC, human approval | refills, larger withdrawals |
| cold | 90%+ | air-gapped, geographically separated | reserves |

Cold must be **genuinely offline** — not "a server we don't use much".

## The honest threat model
**A host that holds the sole signing key controls everything that key controls.** If the same machine can rewrite state, it already controls the chain outright. Therefore:
- Multisig protects against **theft of one key by an external attacker**.
- Multisig does **not** protect against compromise of a host that holds a threshold of keys.
- Moving a second key onto the same server that holds the first collapses the property to single-key security. That may be an acceptable operational trade — but state it as such, never as defence in depth.
- A key that doubles as the chain's block-signing key is mixing roles; separate them.

## Withdrawal controls (layer all of these)
- destination allowlist with a **24h cool-down** on additions
- per-user and platform-wide velocity limits
- amount thresholds escalating to manual approval, then to multi-approver
- anomaly checks: new destination, dormant account waking, withdrawal shortly after a password or 2FA change
- **simulate before broadcast** (see the Tenderly note in the skills catalogue)
- a hard kill switch that halts all outbound movement

## Key ceremony
Documented, witnessed, recorded. Generate on an air-gapped device. Split backups (Shamir or geographic multisig), stored in separate physical locations. **Test recovery on a schedule** — an untested backup is not a backup.

## Never
- a private key in plaintext in a repository, a config file, or a chat message
- a key file readable by more than its owner (`chmod 600` minimum)
- password authentication where key authentication is possible
- reusing an operational key as a governance key

If a key is exposed: **revoke its on-chain authority first**, rotate second, purge history third. Order matters — history purging while the key still holds authority achieves nothing.
