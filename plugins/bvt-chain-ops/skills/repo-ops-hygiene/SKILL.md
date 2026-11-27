---
name: repo-ops-hygiene
description: Keeps repositories free of secrets and safe to publish. Use when scanning for keys, purging a secret from git history, responding to a leak, configuring ignore rules and pre-commit hooks, or replacing password authentication with SSH keys. A text search is insufficient because compiled artifacts hide key material, so a byte-level binary scan is required.
---

# Repo & Ops Hygiene

## Scanning — two passes, always
1. **Text pass** — `git grep`, `gitleaks`, `trufflehog` across all refs.
2. **Binary pass** — scan raw bytes of every object.

**The text pass silently skips compiled artifacts.** A real case: a binary scan caught plaintext key material in two `.pyc` files that the text pass had reported clean. Never conclude "clean" from a text grep alone.

Check working tree, all branches, all tags, and stashes.

## If a secret is committed
Order matters:
1. **Revoke the secret's authority first.** On-chain: strip every role the key holds (minter, admin, oracle updater, fee destination, proposer). Off-chain: rotate the credential at the provider. Purging history while the key still holds authority achieves nothing.
2. **Rotate** to a new key.
3. **Purge history** — `git filter-repo` (or BFG), then force-push.
4. **Verify** with both scan passes.
5. **Ask the host to expunge stale unreachable objects** — a force-push does not delete them, and they remain fetchable by hash until the host garbage-collects.
6. **Every clone must be deleted and re-cloned**, not pulled. A pull re-introduces the purged objects.

## Multi-repo trap
If a secret existed in two repos and only one was rewritten, the un-rewritten one still carries it. Remove its `origin` remote so it cannot push, and treat it as contaminated until rewritten. Document which repo is clean and which is the working copy.

A workable split: develop in the working repo (which holds `.env`, `node_modules`, tooling), **copy changed files** into the clean repo, and commit and push only from there.

## Prevention
- `.gitignore` for `.env*`, `*.key`, `key`, `keystore/`, `*.pem`, `secrets/`
- pre-commit hook running a secret scanner; CI job that fails the build on a hit
- **never** commit a key file "temporarily"
- keep test keys in a clearly named directory and confirm none matches a live address

## Credentials handling
Never request, echo, or repeat a credential. If one appears in a conversation or a log, say so once, plainly, and move on — do not restate it.

**Replace password auth with keys:**
```
ssh-keygen -t ed25519 -C "<label>"
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@host
# then: PasswordAuthentication no  in sshd_config, and reload sshd
```
Key files `chmod 600`. Rotate on any suspicion.
