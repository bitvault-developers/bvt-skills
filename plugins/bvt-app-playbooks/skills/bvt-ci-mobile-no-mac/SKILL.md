---
name: bvt-ci-mobile-no-mac
description: Builds, signs and ships BitVault iOS and Android applications from a Linux or Windows Subsystem for Linux machine with no Mac, using cloud build services. Use when setting up mobile continuous integration, configuring build credentials, submitting to the stores from a Linux box, or estimating build costs.
---

# Mobile CI Without a Mac

## What is and is not possible
**Possible from Linux/WSL2:** everything — iOS builds, signing, TestFlight upload, App Store Connect submission — via cloud macOS runners.
**Not possible:** running Xcode locally, or attaching a local iOS simulator/device debugger. Building macOS desktop binaries also needs a macOS runner.
**Not acceptable:** macOS in a VM on non-Apple hardware. It violates Apple's licence and will not be a stable release pipeline.

## Options
| Service | Model | Notes |
|---|---|---|
| **EAS Build** (recommended) | Expo-native | `eas build` / `eas submit` from the CLI; manages certificates and provisioning profiles for you |
| Codemagic | CI platform | free tier, paid from ~$39/mo |
| GitHub Actions macOS runner | generic CI | 2,000 free minutes/month but macOS is billed at a **10× multiplier**, so it burns fast |
| Xcode Cloud | Apple | tightly integrated, Apple-account bound |

## EAS pricing shape (verify at signup — plans move)
- **Free:** ~15 iOS + 15 Android builds/month, OTA updates to ~1,000 MAU.
- **Starter ~$19/mo**, **Production ~$199/mo** with build credits included.
- Pay-as-you-go roughly $3/iOS build.
**Start free. Move to Starter when you exceed ~15 iOS builds a month.**

## The lever that keeps you on the free tier
**EAS Update.** JS-only changes ship without a build. Batch native changes (new dependency, permission, config plugin) into deliberate release trains instead of one-off builds. A disciplined team ships weekly binaries and daily OTA updates.

## Credentials
Let EAS manage iOS certificates and provisioning profiles; it is the most common source of self-managed breakage. For Android, generate the upload keystore once and **back it up off-machine** — losing it means you cannot update the app on Play without Google's key-reset process.

Never commit a keystore, a `.p8` App Store Connect key, or a service-account JSON. They belong in EAS secrets / CI secrets.

## Pipeline shape
```
PR            → lint + typecheck + unit tests (Linux, fast, free)
merge to main → eas update (preview channel)
release tag   → eas build --profile production (ios + android)
              → eas submit
              → Maestro E2E against the built artifact
              → staged rollout
```
Run everything cheap on Linux; spend macOS minutes only on the release build.

## Local development without a Mac
Android emulator locally. iOS via **Expo Dev Client on a physical iPhone** with EAS-built dev builds — you can develop iOS features daily from Linux, you just cannot debug native iOS code. If a native iOS module needs real debugging, that is the one task that justifies borrowing or renting a Mac.
