---
name: bvt-ts-conventions
description: Writes TypeScript to strict, crypto-safe conventions across the monorepo — strict compiler settings, explicit error handling over thrown exceptions in core, branded types for addresses and amounts, and integer-only money handling. Use when adding types, designing function signatures, handling errors, or reviewing TypeScript in any package or app shell.
---

# TypeScript Conventions

## Compiler (non-negotiable in `packages/config/tsconfig.base.json`)
`strict: true` · `noUncheckedIndexedAccess: true` · `exactOptionalPropertyTypes: true` · `noImplicitOverride: true` · `verbatimModuleSyntax: true`.
`any` is banned in `packages/*`. `unknown` + a narrowing guard instead.

## Money is never a number
```ts
type Wei = bigint;                       // always bigint, never number
type Decimals = number;                  // per-token, read from the registry
```
- **No floats anywhere in a balance, amount, price, or fee path.** JS `number` loses precision above 2^53 and 1e18 wei exceeds it immediately.
- Format for display only, at the edge, never round-trip a formatted string back into arithmetic.
- Rounding direction is explicit and documented at each call site.

## Branded types stop whole bug classes
```ts
type Address  = string & { readonly __brand: 'Address' };
type TxHash   = string & { readonly __brand: 'TxHash' };
type Mnemonic = string & { readonly __brand: 'Mnemonic' };
export const asAddress = (s: string): Address => {
  if (!/^0x[0-9a-fA-F]{40}$/.test(s)) throw new Error('bad address');
  return s as Address;
};
```
A raw `string` can no longer be passed where an address is expected. Apply to addresses, hashes, token ids, and chain ids.

## Errors: results in core, exceptions at the edge
`packages/core` returns a discriminated result rather than throwing — a thrown error in a signing path is easy to swallow and hard to test:
```ts
type Result<T, E = AppError> = { ok: true; value: T } | { ok: false; error: E };
```
`AppError` is a tagged union with a stable `code` the UI switches on. Never surface a raw provider error string to the user; map it.

## Discipline
- No default exports in packages (breaks refactors and tree-shaking clarity).
- No barrel file re-exporting the whole package — it defeats tree-shaking and creates cycles.
- `readonly` on every array/object that isn't intentionally mutated.
- Zod (or equivalent) at every trust boundary: RPC responses, deep links, storage reads, push payloads. Parse, don't cast.
- **Never `console.log` a value that could be key material.** Add an ESLint rule banning `console` in `packages/core`.
