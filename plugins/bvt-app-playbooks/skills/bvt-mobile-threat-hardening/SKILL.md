---
name: bvt-mobile-threat-hardening
description: Hardens BitVault mobile and desktop apps against device-level compromise. Use when adding root or jailbreak detection, integrity attestation, certificate pinning, anti-tampering or obfuscation, or when deciding how the app should behave on a device it does not trust.
---

# Threat Hardening

## Integrity attestation
- **Android: Play Integrity API.** Verify the token **server-side** — a client-side verdict is worthless. Check device, app and account integrity verdicts.
- **iOS: App Attest / DeviceCheck.** Same rule: assertion verified server-side.
- Attestation gates **server-side privileges** (withdrawal endpoints, exchange API keys), not local wallet features. A non-custodial wallet that refuses to open on a rooted device just loses the user.

## Root / jailbreak detection
Detect and **degrade, don't block**, for the non-custodial wallet: warn clearly, disable biometric-gated auto-unlock, and require the PIN each time. For custodial paths (BVTEx, BVTBank), a failed integrity check blocks the privileged action server-side.

Detection is a speed bump — every check is defeatable. Never rely on it as a security boundary; layer it.

## Certificate pinning
Pin the RPC and API endpoints. Pin to the **SPKI hash of an intermediate or a backup key**, not a leaf certificate, and ship **at least two pins** including a not-yet-deployed backup. A single leaf pin plus a certificate rotation equals a bricked app with no remote fix.
Ship a documented un-pin path via a forced update, and never pin in a way that OTA cannot recover.

## Anti-tampering
- Verify the signing certificate at runtime (Android) / bundle identifier and receipt (iOS).
- ProGuard/R8 for Android release builds; Hermes bytecode on RN already limits casual JS reading.
- Obfuscation raises cost, it does not provide secrecy. **Never ship a secret in the bundle** — there is no such thing as a client-side secret.

## Overlay and input attacks
- Android: `filterTouchesWhenObscured` on approve/sign buttons to defeat tapjacking overlays.
- Disable third-party keyboard capture on secret fields where the platform allows.
- Reject deep links that trigger a signing action without an explicit in-app confirmation screen.

## Debug surface
Release builds must have: no remote debugging, no dev menu, no verbose logging, no source maps shipped to the device, and Flipper/dev-only native modules excluded. Verify by inspecting the release artifact, not the config.

## Honest framing
Everything here raises the attacker's cost. **The security boundary is the hardware keystore and the user's passphrase**, not detection code. Write the threat model down and do not let hardening theatre substitute for it.
