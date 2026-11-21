---
name: bvtwallet-architecture
description: Builds BVTWallet features across its web, mobile and extension builds. Use for seed phrase generation and twelve word import, key derivation, keystore encryption, time-based one-time password two-factor setup, transaction construction and broadcast, token list rendering, and the secure storage differences between platforms. A decrypted seed must never persist in extension service worker state.
---

# BVTWallet Architecture

## Seed and derivation
- BIP-39 mnemonic, 12 words (128-bit entropy). Entropy from `crypto.getRandomValues` only — never `Math.random`.
- Validate the checksum on import and reject with a clear message; do not silently accept an invalid phrase.
- BIP-32/44 path `m/44'/60'/0'/0/i` for EVM accounts.
- Normalise input: trim, collapse whitespace, lowercase, NFKD.

## Storage of secrets
Encrypt the seed at rest with a key derived from the user passphrase (`PBKDF2` with a high iteration count, or `scrypt`), then `AES-GCM`. Store salt, IV and ciphertext; never the passphrase.

| Target | At rest | In memory |
|---|---|---|
| web / PWA | IndexedDB, encrypted blob | unlocked key in a module-scoped variable, cleared on lock/tab close |
| mobile | platform secure storage / keychain | cleared on background |
| extension | `chrome.storage.local`, encrypted blob | **`chrome.storage.session` only** — see below |

**Extension rule: a decrypted seed must never persist in service-worker state.** MV3 workers terminate and restart arbitrarily; anything held in a module variable is lost silently and anything written to `local` unencrypted is exposed. Use `chrome.storage.session` for the unlocked state and re-prompt after the auto-lock timeout.

## Auto-lock
Lock on: timeout (default 5–15 min), explicit lock, tab/app close. Zero the key material on lock.

## TOTP 2FA
RFC 6238, 30s step, SHA-1, 6 digits, ±1 step drift window. Provision via `otpauth://` URI + QR. **Generate and display recovery codes at setup** and require acknowledgement. Note plainly: TOTP protects app access, **not** the seed — anyone with the seed phrase controls the funds regardless.

## Send flow
1. Build the transaction; resolve fee data.
2. Simulate (`provider.call`) before asking for a signature.
3. Show the human-readable effect: asset, amount, destination, fee, total.
4. Sign, broadcast, then track by hash with a pending state.
5. Handle replacement/repricing; `tx.wait()` returning `null` means replaced.

If signing runs through a backend service, the backend never receives the seed — it receives a signed payload or a signing request bound to an authenticated session.

## Receive screen
Address + QR + copy. Show the derivation index. **Every screen needs its state declared** (loading, ready, error): a missing one is a common cause of a screen that won't open.

## Security copy that must not be softened
- The seed phrase is shown once, in a deliberate reveal, with a confirmation step.
- Never transmit, log, screenshot-allow, or autofill the seed.
- No support flow ever asks for it.
