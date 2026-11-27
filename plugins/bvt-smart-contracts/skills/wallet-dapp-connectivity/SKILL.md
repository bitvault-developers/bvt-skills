---
name: wallet-dapp-connectivity
description: Implements wallet to dapp connectivity standards. Use when injecting an EIP-1193 provider, announcing a wallet via EIP-6963 multi injected provider discovery, integrating WalletConnect, implementing chain add and chain switch requests for a custom network, or debugging provider conflicts between multiple browser wallets.
---

# Wallet ↔ dApp Connectivity

## EIP-1193 (the provider interface)
`request({ method, params })` plus events: `accountsChanged`, `chainChanged`, `connect`, `disconnect`.
Standard errors: 4001 user rejected · 4100 unauthorised · 4200 unsupported method · 4900 disconnected · 4901 chain disconnected. Return these codes, don't invent your own.

## EIP-6963 (multi-provider discovery) — implement this
Wallets fighting over `window.ethereum` is the problem 6963 solves.

**Wallet side:** on load and on every `eip6963:requestProvider` event, dispatch:
```js
window.dispatchEvent(new CustomEvent("eip6963:announceProvider", {
  detail: Object.freeze({ info: { uuid, name, icon, rdns }, provider })
}));
```
- `uuid` — fresh UUIDv4 per page load
- `rdns` — reverse-DNS identifier, e.g. `com.example.wallet`
- `icon` — data URI

**dApp side:** listen for `eip6963:announceProvider`, then dispatch `eip6963:requestProvider`. Collect all, let the user pick.

**Security:** render the announced `icon` **only** via `<img src={icon}>`. Never inject it as raw HTML/SVG markup — that is an XSS path from any installed extension.

Keep a legacy `window.ethereum` shim for dApps that haven't adopted 6963.

## Adding a custom EVM network
`wallet_addEthereumChain` with: chainId (hex), chainName, `rpcUrls`, `nativeCurrency: { name, symbol: "<SYMBOL>", decimals: 18 }`, `blockExplorerUrls`.
Then `wallet_switchEthereumChain`; error `4902` means not added — add, then retry.

**MetaMask constraint:** the chain ID is **not editable** on an existing network. The RPC URL is. Changing chain ID requires delete-and-re-add.

## WalletConnect
v2, one project id, declare required vs optional namespaces, handle session proposal/approval/expiry, and support pairing by URI and by QR. Persist the session and restore it on load.

## Common failures
- Two wallets installed → the wrong provider captured. Fix: 6963.
- `accountsChanged` returning `[]` means locked/disconnected — handle it as a state, not an error.
- Chain switch resolving before the switch completes — re-read `chainId` after.
