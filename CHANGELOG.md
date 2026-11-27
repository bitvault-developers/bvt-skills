# Changelog

All notable changes to BVT Skills are listed here. Versions follow [Semantic Versioning](https://semver.org).

## 1.1.0 — 2026-11-28

133 skills in 9 plugins (was 54 in 6).

### New: bvt-apple-builder 0.3.0

- Build, sign and ship iPhone, iPad and Mac apps with no Mac: routes for Expo EAS, Tauri v2 (iPhone, iPad, Mac download, Mac App Store), Flutter, React Native without Expo and SwiftUI, with templates, signing from Windows, build-log triage, release checklist and App Review compliance. Skills: `bvt-apple-builder`, `apple-new`, `apple-fix`, `apple-ship`, `apple-compliance`, `apple-signing`.

### New: bvt-smart-contracts 1.0.0

- 7 skills: `ethers-v6-conventions`, `contract-upgrade-safety`, `evm-storage-surgery`, `smart-contract-audit-checklist`, `wallet-dapp-connectivity`, `metamask-troubleshooting`, `mv3-extension-constraints`.

### New: bvt-skill-loaders 1.0.0

- 42 loaders for open-source skill packs, each pinned to a reviewed commit (Firecrawl, PostHog, Composio, gstack, Ponytail, ECC, CLI-Anything, Agent Reach, Strix, Trail of Bits, OpenZeppelin, Expo, Firebase, LangChain, Vercel, Callstack, Three.js, Blender, GSAP, HyperFrames, Opuscar, Reanimate, rea-video, real-sfx, earshot, watch-video and more), plus our own `openverse-sounds`.

### bvt-crypto-architecture 1.1.0

- 17 new skills: matching engine, market data feeds, trading API, liquidity and market making, exchange ledger, custody and keys, deposit sweeping, fiat ramp and card, India VASP compliance, stablecoin mechanics, token listing metadata, oracles, bridges, wrapped token factory, mining pool, block explorer and indexing.

### bvt-chain-ops 1.1.0

- 3 new skills: `besu-clique-ops`, `chain-relaunch-migration`, `repo-ops-hygiene`.

### bvt-multi-language 1.1.0

- The playbook is also available as three focused skills: `adding-language-switching`, `translating-app-languages`, `checking-translation-quality`.

## 1.0.0 — 2026-11-22

First public release.

### bvt-multi-language 1.0.0

- Language switcher and full multilingual system for React, Next.js, Vue, Svelte, Angular, Flutter, FlutterFlow, React Native, Android, iOS, Electron, Tauri and WordPress.
- 7 scripts: `mt_translate.py` (Google, Azure, DeepL, LibreTranslate or Claude, with caching, glossary and cost estimate), `check_locales.py`, `convert_locale_format.py`, `make_registry.mjs`, `find_hardcoded.py`, `seo_hreflang.py`, `screenshot_langs.py`.
- Right-to-left layout, plural rules, local number, currency and date formats, pseudo-locale testing, and a quality gate before release.

### bvt-save-token 1.0.0

- Short replies, diff-only code, handoff notes for fresh chats, and a setup audit.

### bvt-crypto-architecture 1.0.0

- `bvtex-exchange-architecture`: ledger first, single-writer matching engine, safe build order.
- `bvtwallet-architecture`: seed phrase, encrypted storage, 2FA and send flow for web, mobile and browser extensions.

### bvt-i18n-playbooks 1.0.0

- 15 localization skills: architecture, ICU message format, string authoring, text expansion, RTL, fonts and scripts, number and currency, date and time, crypto terminology, seed phrase language rules, store listings, regulatory translation, translation pipeline, AI translation QA and testing.

### bvt-app-playbooks 1.0.0

- 29 app engineering skills for crypto wallet and exchange apps across mobile, desktop, web and browser extension.

### bvt-chain-ops 1.0.0

- 6 skills: Solidity standard, governance flow, PoW L1 operations, edge operations, incident runbooks, branding and docs.
