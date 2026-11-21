---
name: bvt-mobile-secure-storage
description: Implements secure secret storage and hardware-backed key protection for BitVault across the iOS Secure Enclave and Keychain, the Android Keystore and StrongBox, and desktop operating system keystores. Use when storing or retrieving seeds, keys, PINs or session tokens, when adding biometric gating to storage, or when choosing between platform storage APIs.
---

# Mobile & Desktop Secure Storage

## iOS — the Secure Enclave cannot hold your key
The Secure Enclave supports **ECDSA on NIST P-256 only**. It cannot store or sign with **secp256k1** (Bitcoin/Ethereum) or ed25519, and cannot store arbitrary data.

**The pattern every wallet uses — wrap, don't store:**
1. Generate a **P-256 keypair inside the Secure Enclave**, non-exportable, biometric-gated.
2. Use it to **encrypt (wrap) the BIP-39 seed / keystore blob**.
3. Store the wrapped blob in the Keychain.
The seed is useless without a biometric unlock on that exact device, and the wrapping key never leaves hardware.

Keychain flags:
- `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` — excludes the item from backups and blocks restore onto another device.
- `kSecAccessControl` with **`.biometryCurrentSet`** — adding a new fingerprint/face invalidates access. `.biometryAny` does not, and is the wrong choice for a wallet.
- Keychain items **survive app deletion**. Decide deliberately whether reinstall should recover the wallet or start clean, and document it.
- **The simulator has no Secure Enclave** — SE operations fail. Fall back to software P-256 in the simulator only, never in a release build.

## Android
- **Android Keystore**, hardware-backed via **StrongBox** (dedicated secure element) or **TEE** (TrustZone). Use `setIsStrongBoxBacked(true)` with a TEE fallback — not all devices have StrongBox.
- `setUserAuthenticationRequired(true)` + `BiometricPrompt`; set a short validity window rather than an unbounded one.
- **`EncryptedSharedPreferences` is deprecated** (androidx.security-crypto 1.1.0-alpha07). New code uses **Jetpack DataStore + Tink + Keystore**. Do not add it to a new build.
- **StrongBox is slow.** Use it to protect a wrapping key, not for bulk encryption on a hot path.
- Use hardware key attestation to prove the key is hardware-backed before enabling high-value flows.

## Desktop — state the ceiling honestly
macOS Keychain · Windows Credential Manager (DPAPI) · Linux Secret Service (libsecret / GNOME Keyring / KWallet).

**None of these isolate keys from same-user processes.** Once the user's session is unlocked, any process running as that user can read them. That is the realistic desktop threat and the OS store does not stop it. Therefore:
- Always encrypt the seed with a **user passphrase/PIN** via **Argon2id**, stored nowhere.
- The OS store holds the *encrypted* blob, not the seed.
- Real hardware isolation on desktop means an external signer (Ledger/Trezor). Say so in the UI rather than implying more security than exists.
- Linux Secret Service may be **absent** on minimal/headless desktops — handle its absence as a supported path, not a crash.

## Cross-platform libraries
| Library | Backing | Note |
|---|---|---|
| `expo-secure-store` | Keychain / Keystore | good default, small values only |
| `react-native-keychain` | Keychain / Keystore | richer access-control + biometric flags |
| `tauri-plugin-stronghold` | IOTA Stronghold vault | password hash must be **exactly 32 bytes**; default Argon2 params are modest — raise them |

## Rules
- Never store a seed unencrypted, on any platform, for any duration.
- Never put key material in AsyncStorage, MMKV (unencrypted), `localStorage`, or `chrome.storage.local` in plaintext.
- Every read is gated by an unlock; there is no "cached unlocked" path that outlives the lock timeout.
