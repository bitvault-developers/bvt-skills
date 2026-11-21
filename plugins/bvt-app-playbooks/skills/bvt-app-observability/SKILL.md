---
name: bvt-app-observability
description: Adds crash reporting, error tracking and privacy safe analytics to BitVault apps without leaking wallet addresses, balances or key material. Use when integrating an error reporter, adding logging or telemetry, debugging a production issue, or reviewing what data an app sends off device.
---

# App Observability (privacy-safe)

## The constraint that comes first
A wallet's telemetry can deanonymize its users. **Never send off device:** seed phrases or keys (obviously), wallet addresses, balances, transaction hashes, token holdings, API keys, or any value derived from them. An error reporter that captures a redux/Zustand snapshot will capture all of it by default.

## Crash and error reporting
- Sentry (or equivalent) with **aggressive scrubbing configured before the first release**, not after an incident.
- `beforeSend` hook that drops any event whose message, breadcrumbs, extra data, or stack frames match address-like or mnemonic-like patterns. Fail closed: if a value can't be classified, drop it.
- **Disable session replay and screenshot capture entirely** on wallet screens — ideally app-wide.
- Strip request bodies from breadcrumbs; keep the URL path, drop query strings.
- Upload source maps for readable stack traces, but **never ship source maps to devices**.

## Logging
- Structured levels; **release builds log nothing above `warn` to any sink**.
- A lint rule bans `console.*` inside `packages/core`.
- Never log a variable named `seed`, `mnemonic`, `privateKey`, `secret`, or their contents — and never log a whole object that might contain one. Log field names, not values.
- An in-app debug log the user can view and *choose* to share is far better than an automatic upload; it puts consent where it belongs.

## Analytics
- Event-level only, no user identity beyond an **anonymous, rotatable install id** that is not derived from any address.
- Count actions ("send_completed"), never their parameters (amount, token, destination).
- Opt-in, with a visible toggle in settings, defaulting to off for the wallet. For the custodial exchange, standard product analytics is more defensible — but keep the two apps' telemetry configurations separate so a shared default cannot leak wallet data.

## What to actually monitor
Crash-free session rate (per release, per platform) · cold start time · RPC error rate and endpoint failover frequency · transaction broadcast failure rate · unlock failure rate · OTA adoption. These are the signals that predict user-visible wallet failures.

## Release gate
A staged rollout advances only if crash-free rate holds. A regression in transaction broadcast success or unlock failure is a **rollback**, not a fix-forward — those two failure modes lose money or lock users out of their funds.
