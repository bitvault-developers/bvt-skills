---
name: bvt-rn-expo-conventions
description: Writes React Native and Expo code to strict, crypto-safe conventions covering the New Architecture, Expo Router navigation, EAS Build, Submit and Update, config plugins and native module boundaries. Use for any Expo or React Native app shell code, navigation structure, native dependency choices, or build profile configuration.
---

# React Native + Expo Conventions

## Baseline
Expo SDK with the **New Architecture (Fabric + TurboModules)**. It is default from RN 0.76 and from RN 0.82 it is the **only** architecture — the opt-out flags (`newArchEnabled=false`, `RCT_NEW_ARCH_ENABLED=0`) are ignored and the legacy architecture is frozen. Assume New Arch; do not write bridge-era code.

**Before adding any native dependency**, confirm New Architecture support. An unmaintained native module is a hard blocker, not a slow path. Prefer an Expo module or a JSI-based library.

Pin the SDK. Upgrade deliberately, one SDK at a time, with `npx expo-doctor` and `npx expo install --check` clean before shipping.

## Managed workflow + config plugins, not bare
Stay managed. Native config changes go through **config plugins** in `app.config.ts`, never by hand-editing `ios/` or `android/`. Hand-edited native directories are silently discarded by prebuild and are the main cause of "it works locally, breaks on EAS".

Prebuild artifacts are generated, not source: `ios/` and `android/` stay gitignored.

## Expo Router
File-based routing. Groups for auth state:
```
app/
  (auth)/lock.tsx
  (app)/(tabs)/index.tsx   wallet
  (app)/(tabs)/tokens.tsx
  (app)/send/[token].tsx
  _layout.tsx              root: lock gate + providers
```
The lock gate lives in the root layout and redirects, so no screen can be reached while locked — including via a deep link.

## EAS
Build profiles: `development` (dev client) · `preview` (internal distribution, TestFlight/Play internal) · `production`.
```json
{ "build": {
    "development": { "developmentClient": true, "distribution": "internal" },
    "preview":     { "distribution": "internal" },
    "production":  { "autoIncrement": true } } }
```
`eas build`, `eas submit`, `eas update`. All run from Linux/WSL2 — see `bvt-ci-mobile-no-mac`.

**OTA rule:** `eas update` ships **JS and asset changes only**. Any native dependency change, permission change, or config-plugin change needs a new binary. Never use OTA to alter behaviour the store reviewed — that is a policy violation, not a grey area.

## Runtime versions
Set `runtimeVersion` policy to `appVersion` or a fingerprint so an OTA bundle can never land on an incompatible binary. A mismatched update is a crash loop on user devices with no local fix.

## Rules
- No `react-native` import inside `packages/*` — shells only.
- Every native permission is declared with a purpose string that survives review.
- Test on a **release build on a real device** before submission; Hermes release behaviour differs from dev.
