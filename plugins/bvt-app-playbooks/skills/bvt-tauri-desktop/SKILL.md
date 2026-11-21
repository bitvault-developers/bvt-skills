---
name: bvt-tauri-desktop
description: Builds and packages a crypto desktop app with Tauri version two, covering the capabilities and permissions model, webview content security policy, inter process communication, secret storage and Rust command design. Use for any Tauri desktop shell code, tauri.conf.json changes, command definitions or desktop secret handling.
---

# Tauri v2 Desktop Shell

## Why Tauri here
System WebView + Rust backend: single-digit-MB binaries versus Electron's ~100MB+, materially lower memory, and a real permission model. The same web frontend as the PWA shell drives it. (Electron remains the fallback if a required capability is missing — Ledger Live ships desktop on Electron.)

## Capabilities — default deny
v2 replaces the v1 allowlist with **capabilities**: explicit permission sets scoped to window labels.
```json
{ "identifier": "main-capability", "windows": ["main"],
  "permissions": ["core:default", "store:default", "updater:default"] }
```
- Grant the narrowest permission that works; never `fs:allow-*` broadly.
- **Never grant command access to a remote origin.** The frontend is local; if a window can load remote content, it must have its own capability set with no privileged commands.
- Enable the **Isolation pattern** so IPC messages pass through a trusted sandbox before reaching Rust.

## CSP
Strict, in `tauri.conf.json`:
```
default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
connect-src 'self' https://<your-rpc-host>; img-src 'self' data:;
object-src 'none'; frame-ancestors 'none'
```
No `unsafe-eval`. No wildcard `connect-src` — enumerate the RPC and API hosts.

## Command design
Keep signing and key handling in **Rust**, expose narrow, validated commands:
```rust
#[tauri::command]
async fn sign_digest(key_id: String, digest: Vec<u8>) -> Result<Vec<u8>, String>
```
The frontend never receives a private key. Validate every argument in Rust — an IPC argument is untrusted even from your own frontend, because a compromised dependency in the web bundle can call it.

## Secrets
`tauri-plugin-stronghold` (IOTA Stronghold vault).
- The password hash passed to the builder must be **exactly 32 bytes** — a Stronghold requirement.
- Default KDF is Argon2; **raise the parameters** above the modest defaults for a wallet.
- The salt sits beside the vault in plaintext; security reduces to the user's password. Enforce a real passphrase, not a 4-digit PIN.
- Confirm Stronghold's maintenance status before depending on it; the OS keystore holding an Argon2id-encrypted blob is a valid alternative.

## Desktop security ceiling
State it plainly in the UI: on desktop, any process running as the same user can read the OS keystore once the session is unlocked. The passphrase is the real protection. Hardware isolation means an external signer.

## Build
`tauri build` per target — Windows and Linux from Linux; **macOS builds require macOS** (CI runner). Signing and updates: see `bvt-desktop-signing-updates`.
