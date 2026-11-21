---
name: bvt-app-design-system
description: Applies your design system across the mobile, desktop, web and extension app shells, covering design tokens, token colour conventions, component structure and dark mode. Use when building or restyling UI components, adding a screen, defining spacing or typography, or keeping visual behaviour consistent between platforms.
---

# App Design System

## Tokens live in one place
`packages/config/tokens.ts` — colours, spacing scale, radii, typography, motion durations. Every shell imports from it. **No hardcoded hex values, no magic pixel numbers in components.** A colour that appears in a component file is a bug.

Token colours are fixed identity, not theme: **give each token one colour** (for example main token blue, USD stablecoin silver, INR stablecoin green). They do not change between light and dark mode; only their surrounding surfaces do.

## Cross-platform component strategy
- Primitives (`Text`, `Button`, `Card`, `Sheet`, `Field`) live in `packages/ui`, written against React Native primitives and rendered on web via **react-native-web**.
- Where a platform genuinely diverges, use `.native.tsx` / `.web.tsx` file extensions rather than runtime `Platform.OS` branching inside a shared component. Branching accumulates; file splits stay readable.
- The extension and desktop shells consume the same primitives — that is what stops the three-way drift returning.

## Financial UI rules
- **Amounts are never truncated on a confirmation screen.** Truncate in lists, never at the point of authorization.
- Monospace/tabular figures for balances so digits align in a list.
- Address display: first 6 and last 4 with a copy affordance; full address available on tap and in the accessibility label.
- **State is never encoded by colour alone** — send/receive needs a sign or icon as well as red/green, for colour-blind users and for screenshots.
- Destructive and irreversible actions (send, reveal seed, delete wallet) use a distinct, consistent treatment across all four shells.

## Dark mode
Both themes are first-class. Define semantic tokens (`surface`, `surfaceRaised`, `textPrimary`, `textMuted`, `danger`) and map them per theme — never reference a raw palette value in a component. Test seed and confirmation screens in both; contrast failures show up in dark mode first.

## Coin logos
Transparent, background-removed, served at display size. Source art arrives as JPEG on white, so background removal runs every time — a white box behind a coin logo is a shipped bug. Fallback avatar (ticker initials on a token-derived colour) whenever a logo is missing; a missing image never blocks a row.

## Motion
Short (150–250ms), Reanimated on the UI thread, and honouring `prefers-reduced-motion` / the OS reduce-motion setting. No animation on the path between tapping Send and seeing the confirmation.
