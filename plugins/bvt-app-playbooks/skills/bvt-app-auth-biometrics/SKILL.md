---
name: bvt-app-auth-biometrics
description: Implements app lock, biometric authentication and time-based one-time password two-factor for crypto apps across mobile and desktop. Use when adding Face ID, Touch ID or fingerprint gating, PIN fallback, auto-lock timeouts, TOTP enrolment and verification, or deciding which actions require re-authentication.
---

# App Lock, Biometrics & TOTP

## Layers, and what each actually protects
| Control | Protects | Does not protect |
|---|---|---|
| App lock (PIN/biometric) | device-in-hand access | the seed if extracted from storage |
| Hardware-backed storage | key at rest | a compromised running app |
| TOTP 2FA | app/account access | funds, if the seed leaks |

State this in the UI. A user who believes 2FA protects their funds will store the seed carelessly.

## Biometric gating
- iOS: `LocalAuthentication` (`.deviceOwnerAuthenticationWithBiometrics`), with device passcode as the fallback policy.
- Android: `BiometricPrompt` with `setAllowedAuthenticators(BIOMETRIC_STRONG | DEVICE_CREDENTIAL)`. **`BIOMETRIC_WEAK` is not acceptable** for a signing gate.
- Expo: `expo-local-authentication`, but the gate must be tied to the **keystore access control**, not just a UI boolean. A biometric check that only sets `unlocked = true` in JS is trivially bypassed on a rooted device — the key must be unreadable without the biometric.
- Re-enrolment: `.biometryCurrentSet` on iOS and `setInvalidatedByBiometricEnrollment(true)` on Android, so adding a new face/finger invalidates the key.

## Re-authenticate for
sending funds · revealing the seed · exporting a private key · changing security settings · adding a withdrawal destination · enabling/disabling 2FA. Not for viewing balances.

## Auto-lock
Default 5 minutes idle. Also lock on: app backgrounded past a short grace period, device lock, explicit lock. On lock, **wipe the in-memory key and the account-scoped query cache** (see `bvt-app-state-management`), then reset navigation.

## TOTP (Google Authenticator compatible)
RFC 6238 · 30s step · SHA-1 · 6 digits · **±1 step drift window** (accept previous, current, next).
- Provision with an `otpauth://totp/<AppName>:<label>?secret=...&issuer=<AppName>` URI plus QR.
- Show the secret in plaintext as a manual-entry fallback.
- **Generate recovery codes at enrolment**, require the user to acknowledge them, and store them hashed.
- Store the TOTP secret in secure storage, encrypted, same as any other secret.
- Rate-limit verification attempts and lock out with backoff — TOTP is 6 digits and brute-forceable without it.

## Never
- A "remember me for 30 days" bypass on a signing gate.
- Biometric state cached across a cold start.
- Falling back to no auth when biometrics are unavailable — fall back to the PIN.
