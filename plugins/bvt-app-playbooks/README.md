# BVT App Playbooks

Twenty-nine engineering skills for building crypto wallet and exchange apps across mobile, desktop, web and browser extension.

| Skill | What it covers |
|---|---|
| `bvt-app-api-client` | Designs typed client code for backend and exchange APIs including request signing, idempotency, pagination, error taxonomy and response validation. |
| `bvt-app-auth-biometrics` | Implements app lock, biometric authentication and time-based one-time password two-factor for crypto apps across mobile and desktop. |
| `bvt-app-design-system` | Applies your design system across the mobile, desktop, web and extension app shells, covering design tokens, token colour conventions, component structure and dark mode. |
| `bvt-app-observability` | Adds crash reporting, error tracking and privacy safe analytics to crypto apps without leaking wallet addresses, balances or key material. |
| `bvt-app-rpc-resilience` | Builds resilient chain connectivity for crypto apps against layer one and layer two nodes, covering endpoint failover, retry and backoff, request batching, timeouts, reorg awareness and network switching. |
| `bvt-app-state-management` | Structures client state for crypto apps — server and chain state via a query cache, ephemeral UI state locally, and persisted user state in encrypted storage. |
| `bvt-appstore-release` | Prepares crypto apps for App Store and Google Play submission, covering Apple's cryptocurrency rules, Google Play's crypto and financial policies, developer account enrolment, review notes, staged rollout and over the air update limits. |
| `bvt-charts-and-market-viz` | Implements charts and market data visualization for crypto apps including candlestick charts, portfolio and sparkline views, and performant rendering on mobile. |
| `bvt-ci-mobile-no-mac` | Builds, signs and ships iOS and Android apps from a Linux or Windows Subsystem for Linux machine with no Mac, using cloud build services. |
| `bvt-deeplinks-walletconnect` | Implements WalletConnect v2 session handling and deep linking for a crypto wallet across iOS, Android, desktop and the browser extension. |
| `bvt-desktop-signing-updates` | Handles desktop code signing, notarization and auto update for desktop apps on Windows, macOS and Linux. |
| `bvt-exchange-client-ui` | Builds a crypto exchange client interface including real time order book rendering, websocket reconnection with sequence gap recovery, order entry, and application background and foreground handling. |
| `bvt-frontend-system` | Builds and maintains your single-file React applications. |
| `bvt-i18n-a11y` | Implements localization and accessibility for crypto apps, covering Hindi and other Indian languages, number and currency formatting, screen reader support and dynamic type. |
| `bvt-mobile-perf` | Optimizes crypto mobile app performance including virtualizing large token lists, coin logo image pipelines, startup time, JavaScript bundle size and animation smoothness. |
| `bvt-mobile-secure-storage` | Implements secure secret storage and hardware-backed key protection for crypto apps across the iOS Secure Enclave and Keychain, the Android Keystore and StrongBox, and desktop operating system keystores. |
| `bvt-mobile-testing` | Writes and runs tests for crypto mobile apps including end to end user journeys, crypto flow tests against testnets, and device coverage. |
| `bvt-mobile-threat-hardening` | Hardens crypto mobile and desktop apps against device-level compromise. |
| `bvt-offline-sync` | Implements offline-first encrypted local data and chain state cache invalidation for crypto apps using SQLite. |
| `bvt-push-privacy` | Implements transaction, price and order push notifications for crypto apps without leaking wallet addresses or balances to the push infrastructure. |
| `bvt-pwa-shell` | Maintains a crypto app's web and progressive web app shell including the service worker, offline behaviour, install prompts and browser storage limits. |
| `bvt-rn-crypto-primitives` | Generates and reviews cryptographic key code for React Native and shared-core crypto apps, covering secp256k1 signing, BIP-39 mnemonics, BIP-32 and BIP-44 derivation, entropy sources and key material hygiene. |
| `bvt-rn-expo-conventions` | Writes React Native and Expo code to strict, crypto-safe conventions covering the New Architecture, Expo Router navigation, EAS Build, Submit and Update, config plugins and native module boundaries. |
| `bvt-rn-native-modules` | Designs and writes native modules for React Native apps when JavaScript cannot do the job, using Expo Modules API or TurboModules with JSI. |
| `bvt-seed-phrase-ux` | Builds seed phrase creation, backup, verification and recovery screens for crypto wallets with correct screen-capture protection and clipboard handling. |
| `bvt-shared-core-monorepo` | Enforces your shared-core monorepo architecture using pnpm workspaces and Turborepo, with packages for crypto, RPC and business logic and thin per-platform app shells. |
| `bvt-singlefile-migration` | Migrates hand-synced single-file React builds (web, mobile, extension) into a shared TypeScript core with thin platform shells. |
| `bvt-tauri-desktop` | Builds and packages a crypto desktop app with Tauri version two, covering the capabilities and permissions model, webview content security policy, inter process communication, secret storage and Rust command design. |
| `bvt-ts-conventions` | Writes TypeScript to strict, crypto-safe conventions across the monorepo — strict compiler settings, explicit error handling over thrown exceptions in core, branded types for addresses and amounts, and integer-only money handling. |

Written for public use: replace the example tokens, chains and app names with your own. Made by the BitVault team.

## Install

```text
/plugin install bvt-app-playbooks --marketplace bitvault-developers/bvt-skills
```

Or, in your terminal:

```bash
claude plugin install bvt-app-playbooks --marketplace bitvault-developers/bvt-skills
```

For the Claude app, download single skills as zips from the [latest release](https://github.com/bitvault-developers/bvt-skills/releases/latest) or the [`dist`](../../dist) folder and upload them where you add skills in Claude's settings.
