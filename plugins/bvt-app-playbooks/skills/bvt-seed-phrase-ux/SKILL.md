---
name: bvt-seed-phrase-ux
description: Builds seed phrase creation, backup, verification and recovery screens for crypto wallets with correct screen-capture protection and clipboard handling. Use when implementing wallet creation, twelve word backup or confirmation flows, recovery phrase import, or any screen that displays private key material.
---

# Seed Phrase UX & Screen Protection

## Screen capture — the platform asymmetry
- **Android:** `FLAG_SECURE` blocks screenshots **and** screen recording at OS level. Set it on every screen that renders seed words or a private key. Note it is bypassed on rooted devices.
- **iOS:** there is **no API to block screenshots.** You can only:
  - detect after the fact via `UIApplicationUserDidTakeScreenshotNotification`
  - detect active recording/mirroring via `UIScreen.isCaptured` and blur while true
  - blur or overlay the view on `willResignActive` so the **app snapshot** in the task switcher never contains the phrase
- In Expo, `expo-screen-capture` covers the Android block and the iOS detection.
- Design accordingly: **assume an iOS user can screenshot the phrase**, and warn them in-flow rather than pretending it is prevented.

## Creation flow
1. Generate from the CSPRNG (see `bvt-rn-crypto-primitives`).
2. **Deliberate reveal** — the phrase is hidden behind a tap, not shown on screen entry, so it is not exposed by a stray screenshot or over-the-shoulder glance.
3. Display with word numbers. Monospace. No autocorrect surface.
4. **Verification step is mandatory** — ask for 3–4 words by position. A "I've written it down" checkbox alone produces unrecoverable wallets.
5. Only after verification is the wallet marked backed-up and funds are receivable in the UI.

## Import flow
- Accept paste, but **clear the clipboard afterwards** and warn.
- Per-word validation against the wordlist with position-accurate errors — without echoing the full phrase in an error message or log.
- Normalise (trim / collapse whitespace / lowercase / NFKD) before checksum validation.
- Never autofill, never suggest, never remember. Disable keyboard learning on the field (`autoCorrect={false}`, `spellCheck={false}`, `textContentType="none"`, `keyboardType` default).

## Clipboard
Any copy of a seed or private key auto-clears after ~30–60s and shows that it will. Address copies are fine to persist.

## Copy that must not be softened
- The phrase is the wallet. Anyone with it controls the funds.
- [App name] cannot recover it. There is no reset.
- **No support flow will ever ask for it** — state this in the flow itself, because that sentence is the anti-phishing control.
- TOTP 2FA protects app access, **not** the seed.

## Never
- Render the phrase in a `<WebView>`, a toast, a notification, or an error boundary.
- Send it to an analytics or crash reporter (scrub the entire screen from session replay).
- Allow it in a deep link, a URL, or a QR the app itself generates for sharing.
