---
name: mv3-extension-constraints
description: Builds Chrome and Edge Manifest V3 extensions, with emphasis on crypto wallet constraints. Use when writing the service worker, handling its termination and restart, choosing between session and local storage, injecting a page provider through a content script, configuring the manifest and content security policy, or debugging state that vanished between extension events.
---

# MV3 Extension Constraints

## Service worker lifecycle — the core constraint
The MV3 background is a **service worker that terminates**, typically after ~30s idle, and restarts on the next event. Consequences:
- Module-scoped variables are **not** durable state.
- Timers (`setTimeout`/`setInterval`) do not survive; use `chrome.alarms` (minimum ~1 min period).
- Long operations must be resumable, not assumed-continuous.
- Any listener must be registered **synchronously at top level**, or the event that woke the worker is missed.

## Storage choice
| API | Persists | Use for |
|---|---|---|
| `chrome.storage.local` | across restarts | encrypted vault, settings, address book |
| `chrome.storage.session` | in-memory, cleared on browser close | **unlocked keys, session tokens** |
| `chrome.storage.sync` | synced, small quota | non-secret preferences only |

Never put secret material in `local` unencrypted or in `sync` at all.

## Provider injection
Content script (`world: "MAIN"` or an injected script tag) exposes the provider on the page; it relays to the background via `chrome.runtime` messaging. Announce with **EIP-6963** so the wallet coexists with others instead of fighting over `window.ethereum` (see `wallet-dapp-connectivity`).

## Manifest and CSP
- `manifest_version: 3`, `background.service_worker`
- Request the **minimum** permissions; `<all_urls>` host permissions on a wallet will draw review scrutiny — scope where possible
- No remote code. No `eval`, no `new Function`, no CDN scripts. Bundle everything.
- `content_security_policy.extension_pages` stays strict.

## Messaging
- `chrome.runtime.sendMessage` for one-shot; `connect`/`Port` for streams.
- Return `true` from an `onMessage` listener when responding asynchronously, or the channel closes.
- Validate the sender on every message. A content script's message is attacker-influenced.

## Debug checklist for "state disappeared"
1. Did the worker terminate? (`chrome://serviceworker-internals`)
2. Was the value in a module variable rather than storage?
3. Was the listener registered at top level?
4. Was a `setTimeout` expected to survive?
