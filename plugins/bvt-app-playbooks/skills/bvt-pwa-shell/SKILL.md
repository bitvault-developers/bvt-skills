---
name: bvt-pwa-shell
description: Maintains the BitVault web and progressive web app shell including the service worker, offline behaviour, install prompts and browser storage limits. Use when working on the web build's caching strategy, offline pages, install experience, or when browser storage or web crypto constraints affect wallet behaviour.
---

# Web / PWA Shell

## Role after migration
The web build is a **thin shell over `packages/core`**, not a second implementation. Its job: routing, DOM rendering, and providing the web implementations of the ports (storage, crypto RNG, clipboard).

## Service worker
- Precache the app shell; **network-first for anything chain-derived.** A cached balance served from a service worker with no revalidation is a correctness bug.
- **Never cache an RPC response** in the service worker. Chain reads go through the query layer with block-stamped invalidation, not HTTP caching.
- Version the cache and clean old versions on activate; a stale bundle paired with a new API is a support nightmare.
- Show an explicit "update available — reload" prompt rather than silently swapping the bundle mid-session; a bundle swap during a signing flow is unacceptable.

## Storage reality on the web
- `IndexedDB` holds the encrypted keystore blob. **`localStorage` never holds key material** — it is synchronous, plaintext, and readable by any script on the origin.
- Browser storage is **evictable**. Safari's ITP clears IndexedDB after ~7 days of no interaction. Request `navigator.storage.persist()`, and regardless of the answer, **treat the browser as a place where the wallet can vanish**: the seed backup prompt is mandatory before funds are receivable.
- Never rely on the web build as the only copy of a wallet. Say so in the UI.

## Web Crypto
`crypto.subtle` for PBKDF2/AES-GCM, `crypto.getRandomValues` for entropy — both are native here, so the RN polyfill problem does not apply. The port interface stays identical so core is unchanged.

## Security headers (served, not meta-tagged)
`Content-Security-Policy` with no `unsafe-eval`, `frame-ancestors 'none'` · `Strict-Transport-Security` · `X-Content-Type-Options: nosniff` · `Referrer-Policy: no-referrer` · `Cross-Origin-Opener-Policy: same-origin`.
Ban third-party scripts on any route that renders key material — no analytics, no tag manager, no session replay on wallet screens.

## Install / PWA
- Manifest with maskable icons, `display: standalone`, theme colour.
- Custom install prompt after the user has done something meaningful, not on load.
- iOS PWA limits are real: no push parity, storage eviction, no background sync. The PWA is a convenience surface; the **native app is the wallet you recommend** for holding value.
