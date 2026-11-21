---
name: bvt-rn-crypto-primitives
description: Generates and reviews cryptographic key code for BitVault React Native and shared-core apps, covering secp256k1 signing, BIP-39 mnemonics, BIP-32 and BIP-44 derivation, entropy sources and key material hygiene. Use whenever code touches private keys, seed phrases, mnemonic generation, transaction signing, randomness, or crypto.getRandomValues.
---

# Crypto Primitives (React Native / shared core)

## THE RNG TRAP — read first
React Native has **no built-in `crypto.getRandomValues`**. Without a polyfill, key generation may silently produce weak or empty entropy. This is a fund-loss bug that passes every functional test.

```js
// index.js — FIRST LINE, before any other import
import 'react-native-get-random-values';
```
Then, in `packages/core`, refuse to run without it:
```ts
if (typeof globalThis.crypto?.getRandomValues !== 'function') {
  throw new Error('CSPRNG unavailable — refusing to generate key material');
}
```
Note: noble signs deterministically (RFC 6979), so **signing** survives a broken RNG. **Key generation does not.** A passing signature test proves nothing about your entropy.

## Libraries
- **`@noble/curves`** (secp256k1) + **`@noble/hashes`** — audited, minimal, constant-time-conscious, `lowS: true` by default (BIP-62 / EIP-2 compliant, non-malleable). Use these.
- **`@scure/bip39`** and **`@scure/bip32`** for mnemonics and HD derivation.
- `react-native-quick-crypto` (JSI/native OpenSSL) only where profiling proves a bottleneck.
- Do **not** use `indutny/elliptic`. Do not hand-roll.
- `ethers`/`viem` are fine for ABI encoding and RPC; prefer noble underneath for raw signing.

## Derivation
`m/44'/60'/0'/0/i` for EVM accounts on BVM L2. Store the **index**, never the derived key.
Validate the path shape before deriving; reject anything not matching the expected pattern.

## Mnemonics
- 12 words = 128-bit entropy. Generate from the CSPRNG only.
- On import: trim, collapse whitespace, lowercase, NFKD-normalise, then **validate the checksum** and reject with a clear message. Never silently accept an invalid phrase.
- Validate against the English wordlist; report the first invalid word's position without echoing the phrase.

## Memory hygiene
- Key material lives in **`Uint8Array`**, never `String`. JS strings are immutable and cannot be wiped.
- Wipe after use: `arr.fill(0)`.
- Decrypt as late as possible, use for milliseconds, wipe immediately.
- **Never** log, `JSON.stringify`, send to an error reporter, put in a state store, or include in a stack trace.
- Add an ESLint rule banning `console` in the crypto module.

## Test vectors, not confidence
Ship the official BIP-39 and BIP-32 test vectors as a test suite in `packages/core`. Run them in CI **and on-device** — a JS engine difference between Hermes and V8 that breaks derivation must fail a test, not a user.
