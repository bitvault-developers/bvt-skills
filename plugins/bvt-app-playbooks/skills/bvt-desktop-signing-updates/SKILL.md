---
name: bvt-desktop-signing-updates
description: Handles desktop code signing, notarization and auto update for desktop apps on Windows, macOS and Linux. Use when preparing a desktop release, configuring the Tauri or Electron updater, obtaining or rotating signing certificates, or diagnosing an unsigned or blocked installer.
---

# Desktop Signing & Auto-Update

## Why this is not optional
An unsigned wallet installer triggers SmartScreen on Windows and Gatekeeper on macOS. Users who are told "this app may be dangerous" by their OS while installing a crypto wallet will not install it — and those who click through are exactly the users you least want trained to ignore that warning.

## Windows
- Code-signing certificate: **OV** (cheaper, SmartScreen reputation must be earned over time and downloads) or **EV** (hardware token, instant SmartScreen reputation). **Azure Trusted Signing** is the low-cost modern route (~$10/month tier) and avoids managing a token.
- Sign the installer **and** the executable.
- Reputation resets on certificate change — plan renewals before expiry, don't switch issuers casually.

## macOS
- **Apple Developer ID Application** certificate (requires the $99/yr Apple Developer Program — the same enrollment as iOS).
- Sign with hardened runtime, then **notarize** via `notarytool`, then **staple** the ticket. Notarization is mandatory; without it Gatekeeper blocks the app on any Mac.
- macOS signing and notarization require a macOS machine — use a CI macOS runner.

## Linux
AppImage / .deb / .rpm. GPG-sign the artifacts and publish the public key. No OS-level gatekeeper, so the signature is for users and package managers.

## Tauri updater — the key you cannot lose
- Updates are signed with **minisign (Ed25519)**. Signature verification **cannot be disabled**.
- **Back up the updater private key and its password, off-machine, in two places.** Losing it means every already-installed client can never be updated again. There is no recovery path — you would have to get users to manually reinstall.
- Keep the updater key separate from the OS code-signing key, and separate from anything that touches the chain.
- Serve the update manifest over HTTPS from a host you control; pin the endpoint in config.

## Release checklist
- [ ] version bumped consistently across `tauri.conf.json`, `package.json`, `Cargo.toml`
- [ ] Windows installer + exe signed and timestamped
- [ ] macOS signed, notarized, stapled — verified with `spctl -a -vv`
- [ ] Linux artifacts GPG-signed
- [ ] update manifest signed with minisign, served over HTTPS
- [ ] tested an actual upgrade from the previous released version, not a clean install
- [ ] changelog published
