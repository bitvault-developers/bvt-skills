---
name: bvt-frontend-system
description: Builds and maintains BitVault's single-file React applications. Use when editing the large single-file JSX builds, keeping the web, mobile and extension variants of an app in sync, adding a screen or component, or applying BitVault visual conventions including token colours and embedded transparent logo assets. Encodes what may safely diverge between build targets and what must not.
---

# BitVault Frontend System

## Build targets
Each app ships as parallel **single-file** builds kept in sync:
- `<App>.jsx` — web / PWA
- `<App>_mobile.jsx` — mobile
- `<App>_extension.jsx` — MV3 Chrome/Edge

## Sync discipline
**Must be identical across all three:**
- business logic, validation, and state machines
- contract ABIs, addresses, chain params
- copy for anything security-relevant (seed warnings, confirmations)
- number formatting and rounding

**May diverge, and only these:**
- storage layer (IndexedDB / native secure storage / `chrome.storage`)
- crypto entry points where the platform differs
- navigation shell and viewport layout
- manifest / service worker (extension only)
- clipboard, camera, deep-link, and biometric access

**Rule:** when a change touches anything in the first list, apply it to all three in the same pass and diff them before shipping. A behaviour divergence between wallet builds is a security bug, not a UI inconsistency.

## Working in a very large single file
- Locate by a unique anchor string, not a line number.
- Make one surgical replacement at a time; re-read before the next edit.
- Keep a section index comment block at the top of the file and update it when adding a screen.
- Every new screen needs: its state declaration, its route/case entry, and its render branch. **A missing state declaration is the classic "screen won't open" bug** — check that first.

## Visual conventions
- BVT blue, BRUSD silver, BRINR green.
- Coin logos must be **transparent, background-removed**. Sources arrive as JPEG on white, so background removal runs every time — never ship the white box.
- Embed logo assets in-file (data URIs) so a single file stays self-contained.

## Checklist before shipping a change
- [ ] applied to all three builds
- [ ] state declared for every new screen
- [ ] no target-specific API leaked into shared logic
- [ ] logos transparent
- [ ] tested at mobile width
