---
name: bvt-mobile-perf
description: Optimizes BitVault mobile performance including virtualizing large token lists, coin logo image pipelines, startup time, JavaScript bundle size and animation smoothness. Use when rendering long lists such as the wrapped token registry, when addressing jank or slow cold start, or when reducing bundle size.
---

# Mobile Performance

## Lists — the 909-token problem
`FlatList` is not adequate at this size. Use **FlashList** (recycling, no blank cells while scrolling).
- Set `estimatedItemSize` accurately; a wrong estimate defeats the recycler.
- **Every row is `React.memo`'d** with a stable comparator. One unmemoized row re-renders the visible window on every parent state change.
- Stable `keyExtractor` from the token address, never the array index.
- No inline arrow props on rows — they break memoization every render.
- Search/filter is debounced (~200ms) and runs over a prebuilt index, not a `filter()` over 909 objects per keystroke.
- Consider a section list keyed by rank so the common tokens are reachable without scrolling 900 rows.

## Images / coin logos
- Use `expo-image` — memory + disk caching, `recyclingKey` for lists, `placeholder` for blur-up.
- Ship logos at the **display size**, transparent PNG (or SVG where the renderer supports it). A 1024px PNG scaled to 40px costs full decode memory per row.
- Bundle the top ~50 tokens' logos locally; lazy-fetch the tail with a cached fallback avatar. Never let a missing logo block a row render.

## Startup
- Hermes on, bytecode precompiled.
- **Nothing crypto-heavy on the render path.** Derivation, wallet unlock and RPC fanout happen after first paint, behind a splash/skeleton.
- Lazy-load routes with Expo Router's automatic code splitting; keep the initial route's dependency graph small.
- Measure cold start on a **low-end Android device**, not a flagship or the simulator. That is the device your Indian market is on.

## Bundle size
- `npx expo-atlas` or source-map-explorer to find the offenders.
- Import narrowly (`import { formatUnits } from 'viem'`), never a namespace import of a large library.
- Watch for a full `ethers` or `moment` pull; prefer `viem` + `Intl` / `date-fns`.
- No barrel re-exports in packages — they defeat tree-shaking.

## Animation
Reanimated on the UI thread; nothing driving an animation from JS state per frame. Gesture Handler for touch. If a list janks during scroll, the cause is almost always a non-memoized row or an oversized image, not the animation library.

## Rule
Profile before optimizing, and profile on a release build. Dev-mode React Native is 3–10× slower and will send you after the wrong bottleneck.
