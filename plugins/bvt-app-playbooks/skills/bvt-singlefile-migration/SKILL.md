---
name: bvt-singlefile-migration
description: Migrates BitVault's three hand-synced single-file React builds into a shared TypeScript core with thin platform shells. Use when extracting code out of BVTWallet.jsx, BVTWallet_mobile.jsx or BVTWallet_extension.jsx, deciding what belongs in a shared package, or planning the order of a strangler-fig migration off the single-file architecture.
---

# Single-File → Shared-Core Migration

## The situation
Three ~48k-line single files kept in sync by hand: web/PWA, "mobile" (a React web build, **not a native app**), and MV3 extension. Every feature is written three times. Drift is guaranteed. There is no real Android or iOS app.

## Strangler fig, never big bang
A big-bang rewrite of 48k lines that handles private keys is how funds get lost. Extract one seam at a time; both architectures run side by side until the old file is empty.

## Extraction order (do not reorder)
1. **Crypto / keys** → `packages/core`. Write exhaustive BIP-39/32/44 test vectors **before** moving a single line. This is the only step where a bug is unrecoverable.
2. **RPC + token registry** → `packages/rpc`. L1 client, BVM L2 (chainId 31338), the ~909 wrapped tokens, logo resolution.
3. **Business logic** → `packages/business`. Subscription (`BRUSD.approve` → `subscribe()`), bridge, stablecoin/oracle reads.
4. **Shared UI primitives** → `packages/ui`, react-native-web where it pays.
5. **Build the Expo shell**, wire it to core, then **delete `BVTWallet_mobile.jsx`**.
6. Web and extension become shells over the same core last.

## Per-seam procedure
- Locate by a unique anchor string, never a line number.
- Copy the function into the package **unchanged**; add tests against the old behaviour.
- Replace the original body with a call into the package. Old file still runs.
- Diff behaviour, not code. Ship. Then delete the dead body.
- One seam per commit. A commit that touches two seams cannot be bisected.

## Rules
- **Never edit all three files in one pass again.** If a change would require it, that code is a migration candidate — extract instead.
- Core must import nothing platform-specific. Enforce it (see `bvt-shared-core-monorepo`).
- Keep a `MIGRATION.md` with a table: symbol · old file · new package · status · verified-by.
- Retire `bvt-frontend-system` (the single-file skill) once the mobile file is deleted; it describes an architecture you are leaving.

## Done means
`packages/core` has no React import, the three JSX files are shells under 2k lines each, and a feature ships by touching one package plus at most one shell.
