---
name: bvt-rn-native-modules
description: Designs and writes native modules for BitVault React Native apps when JavaScript cannot do the job, using Expo Modules API or TurboModules with JSI. Use when a feature requires platform APIs, when moving a performance-critical or security-critical operation off the JavaScript thread, or when evaluating whether a native module is necessary at all.
---

# Native Modules

## First: do you need one?
Write a native module only when one of these is true:
1. The platform API has no JS binding (Secure Enclave key ops, StrongBox, App Attest, FLAG_SECURE).
2. Key material must never enter the JS heap.
3. Profiling proves a JS hot path is the bottleneck.

"It feels faster in native" is not a reason. Every native module is a build-breaking upgrade risk and doubles the surface you maintain.

## Which API
- **Expo Modules API (Swift/Kotlin)** — default. Far less boilerplate, works with config plugins, managed-workflow friendly.
- **TurboModules + JSI (C++)** — only for synchronous, zero-copy, high-frequency paths.
- Never write a legacy bridge module. It will not survive the New Architecture.

## Security-critical modules — the boundary rule
For key operations, the **native side owns the secret and exposes only an operation**:
```
// GOOD: JS asks for a signature, never sees the key
signWithStoredKey(keyId: string, digest: Uint8Array): Promise<Uint8Array>

// BAD: key crosses into the JS heap where anything can read it
getPrivateKey(keyId: string): Promise<string>
```
There is no safe version of the second signature. If a JS dependency is compromised, anything the JS heap has touched is gone.

## Interface design
- Async by default; sync only via JSI with a measured reason.
- Typed arrays (`Uint8Array`) for binary, never base64 strings for key material — base64 creates immutable JS strings you cannot wipe.
- Errors as rejected promises with a stable `code`, never a raw platform exception string.
- Keep the surface tiny. Every method is a permanent compatibility obligation.

## Platform parity
Implement both platforms or fail loudly. A module that silently no-ops on Android and gates a security control is worse than absent. Ship a runtime capability check (`isSecureEnclaveAvailable()`) and let the shell degrade explicitly.

## Packaging
Live in `apps/wallet-mobile/modules/<name>` (Expo local modules) until reused by a second app; only then extract to a package. Ship with a config plugin if it needs native config. Document the required Expo SDK / RN version range in the module README.
