---
name: bvt-shared-core-monorepo
description: Enforces your shared-core monorepo architecture using pnpm workspaces and Turborepo, with packages for crypto, RPC and business logic and thin per-platform app shells. Use when creating or moving files between packages, adding dependencies, wiring imports across web, mobile, desktop or extension, or reviewing code for platform leakage.
---

# Shared-Core Monorepo

## Layout
```
apps/
  wallet-mobile/     Expo RN (Android + iOS)
  wallet-desktop/    Tauri v2 shell
  wallet-web/        PWA shell
  wallet-extension/  MV3 shell
packages/
  core/       crypto, keys, BIP-39/32/44, signing      -- pure TS
  rpc/        L1 + L2 chain clients, token registry      -- pure TS
  business/   subscription, bridge, stablecoin logic   -- pure TS
  ui/         shared components (react-native-web)
  config/     eslint / tsconfig / design tokens
```

## Tooling
**pnpm workspaces** (strict resolution surfaces phantom dependencies) + **Turborepo** (task graph and caching) + TypeScript project references. Internal deps use the workspace protocol: `"@yourapp/core": "workspace:*"`.

Metro supports monorepos but needs `watchFolders` pointed at the repo root and `nodeModulesPaths` covering both the app and the root — the classic "module not found in the monorepo but fine standalone" failure.

## The one rule that matters
**`packages/core` must never import `react-native`, `react-dom`, `expo-*`, `chrome.*`, `window`, `document`, `fs`, or any platform API.** Not behind a conditional. Not behind a try/catch.

Enforce it, don't trust it:
```json
"no-restricted-imports": ["error", { "patterns": [
  "react-native", "react-native/*", "react-dom", "expo-*",
  "@tauri-apps/*", "next/*"
]}]
```
applied to `packages/core`, `packages/rpc`, `packages/business` via an ESLint override. CI fails on violation.

## Dependency direction
Shells → packages. Never the reverse. A package importing from `apps/` is always a bug.
`core` ← `rpc` ← `business` ← `ui` ← shells. No cycles.

## Platform differences
When behaviour genuinely differs by platform, the **shell injects the implementation**, core defines the interface:
```ts
// packages/core/src/ports.ts
export interface SecureStore { get(k: string): Promise<Uint8Array|null>; set(k: string, v: Uint8Array): Promise<void>; }
```
Each shell provides its own `SecureStore`. Core never branches on platform.

## Checklist for any new file
- [ ] Is it pure logic? → `packages/*`
- [ ] Does it touch a platform API? → `apps/*`, behind a port
- [ ] Does it import upward? → wrong, invert it
- [ ] Is it duplicated in a second shell? → it belongs in a package
