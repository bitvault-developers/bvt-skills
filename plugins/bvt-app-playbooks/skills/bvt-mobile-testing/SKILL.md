---
name: bvt-mobile-testing
description: Writes and runs tests for crypto mobile apps including end to end user journeys, crypto flow tests against testnets, and device coverage. Use when adding end to end tests, testing send, receive, signing or import flows, setting up test automation in continuous integration, or deciding what to test on real devices.
---

# Mobile Testing

## Layers
| Layer | Tool | Covers |
|---|---|---|
| unit | Vitest/Jest | `packages/core` — crypto, derivation, formatting, business rules |
| component | React Native Testing Library | screens with mocked ports |
| E2E | **Maestro** (default) | real user journeys on a built binary |
| E2E (gray-box) | Detox | when you need RN idle-state synchronisation |

**Default to Maestro.** YAML flows, no native test build, runs against an EAS-built binary and on cloud devices. Reach for Detox only when flakiness demands RN-internal sync.

## The rule that matters
**Never use real funds, mainnet keys, or a production seed in a test.** Not "a small amount". Tests run in CI logs, on shared devices, and in artifacts.
- Fixed, publicly-known test mnemonics from the BIP-39 vectors.
- A dedicated testnet / local EVM node, funded from a faucet.
- Crypto correctness is proven by **official test vectors**, not by moving value.

## What must have a test before shipping
- BIP-39/32/44 vectors, run in CI **and on-device** (Hermes vs Node divergence is real).
- Import → derive → address matches expected, for every supported path.
- Send flow: build → simulate → sign → broadcast, against a local node.
- Lock/unlock: after lock, key material is unreadable and cache is cleared.
- Reorg: cached confirmed tx reverts to pending.
- Large list: list of 900+ tokens scrolls and filters without dropped frames (perf assertion, not just render).

## Device coverage
Test the release build on: one low-end Android (2–3GB RAM, the realistic Indian-market device), one current Android, one older iPhone, one current iPhone. Simulators do not have a Secure Enclave and will not catch keystore failures — **any secure-storage test must run on physical hardware.**

## CI
Unit + component on every PR. E2E on a build artifact per release candidate, not per commit (build minutes are the constraint — see `bvt-ci-mobile-no-mac`). Screenshot tests are optional; behaviour tests are not.

## Anti-flake
No fixed `sleep`. Assert on visible state. Seed a deterministic app state via a launch argument rather than clicking through onboarding in every flow.
