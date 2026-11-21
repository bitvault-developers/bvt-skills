---
name: bvt-deeplinks-walletconnect
description: Implements WalletConnect v2 session handling and deep linking for a crypto wallet across iOS, Android, desktop and the browser extension. Use when pairing with dapps, handling session proposals and requests, configuring universal links or URI schemes, or debugging reconnection and redirect behaviour.
---

# WalletConnect v2 & Deep Links

## Setup order matters
```js
import '@walletconnect/react-native-compat';  // MUST be first
import { WalletKit } from '@reown/walletkit';
import { Core } from '@walletconnect/core';
```
The compat shim must be imported **before any Reown/WalletConnect import** or the SDK initialises against missing globals and fails in ways that look unrelated.

One shared `Core` instance per app. One project id.

## Session flow
`pair(uri)` → `session_proposal` → **explicit user approval screen** → `approveSession(namespaces)` → `session_request` per signing action → approve/reject → `respondSessionRequest`.

Rules:
- **Never auto-approve a proposal.** Show the dapp origin, the requested chains, the requested methods, and the accounts being exposed.
- **Scope namespaces tightly.** Approve only your chain (for example `eip155:1`) and only the accounts the user picked. Blanket-approving every requested chain is how a wallet ends up signing on a network the user never intended.
- Handle `session_delete`, `session_expire`, and `session_update`; show active sessions in a settings screen with a per-session disconnect.
- Persist sessions and restore on cold start.

## Every `session_request` gets a human-readable screen
Decode the calldata against the known ABI and show the *effect*: contract, function, token, amount, recipient, fee. An undecodable request renders as raw calldata with a prominent warning — never as a bare "Approve".

## Deep links
- Universal Links (iOS) / App Links (Android) preferred over custom schemes; keep a custom `yourapp://` scheme as fallback.
- **Validate and parse every incoming link with a schema.** A deep link is untrusted input from any app or web page on the device.
- Redirect back to the dapp after responding, using the session's `redirect` metadata, or the user is stranded in the wallet.

## The hard rule
**A deep link may navigate; it may never authorize.** No link, notification, or WalletConnect request bypasses the lock screen or a signing confirmation. The root layout's lock gate runs first, always — including when the app is cold-started by the link.

## Extension coexistence
The MV3 build announces via EIP-6963 rather than fighting over `window.ethereum`, and renders any announced provider icon only through `<img src>` — never as raw markup.
