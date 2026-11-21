---
name: bvt-appstore-release
description: Prepares BitVault applications for App Store and Google Play submission, covering Apple's cryptocurrency rules, Google Play's crypto and financial policies, developer account enrolment, review notes, staged rollout and over the air update limits. Use when preparing a submission, writing review notes, responding to a rejection, or planning a release.
---

# App Store & Play Submission

## Apple — Review Guideline 3.1.5(b), the three rules that shape the product
- **Wallets:** apps may facilitate virtual currency storage **only if offered by a developer enrolled as an organization.** An individual Apple Developer account **cannot** ship BVTWallet. This is the single most common cause of a crypto wallet rejection and it is not appealable — you enrol as an org or you don't ship.
- **Mining:** on-device mining is prohibited; processing must be off-device (cloud/pool). **BVTMiner must be a remote pool dashboard only** — no hashing on the device, no background compute. Say so explicitly in the review notes.
- **Exchanges:** trading/transmission is permitted only on an approved exchange **offered by the exchange itself**, in regions where it is licensed. BVTEx ships from the operating entity, region-gated.

Also expect scrutiny under 3.1.1 (IAP): the 10 BRUSD/month subscription unlocks **blockchain services**, not in-app digital content. Frame it that way and be ready to explain it; this is the least-derisked policy question in the plan.

## Organization enrolment prerequisites
Legal entity (no trade names/DBAs) · **D-U-N-S number** (free, allow up to ~5 business days) · a public website on the org's domain · signing authority. Start this first — it gates every iOS build. $99/year.

## Google Play
- The Cryptocurrency Exchanges and Software Wallets policy (effective 29 Oct 2025) requires licensing for **custodial** wallets and exchanges. Google has stated **non-custodial wallets are out of scope.**
- So: **BVTWallet (non-custodial) → out of scope. BVTEx and BVTBank (custodial) → in scope**, requiring the relevant local registration.
- Complete the **Financial Features Declaration** under App Content; you'll get country-specific forms.
- Expect Play Integrity expectations for financial apps.

## India
FIU-IND registration under the PMLA is mandatory for VDA service providers — Principal Officer **and** a separate Designated Director, full AML/KYC program, ≥5-year retention, Travel Rule. Custodial products are clearly in scope. A purely non-custodial wallet is generally treated as out of scope, **but that is a legal determination for counsel**, not an engineering call — especially given the custody-backed BVT bridge.

## Review notes that reduce rejections
Include: a working demo account (or a funded testnet wallet with instructions), a plain description of custody model (non-custodial: keys never leave the device), where keys are stored (Secure Enclave-wrapped, Keychain), confirmation that no mining occurs on device, and the regions the exchange is offered in.

## Release engineering
- Staged rollout on Play (5% → 20% → 50% → 100%), watching crash-free rate at each step.
- TestFlight and Play internal testing before every production submission — no exceptions for "small" changes to a wallet.
- **OTA rule:** JS/asset changes only. Never use an OTA update to change behaviour Apple or Google reviewed — that is a policy violation, and it is detectable.
- Keep a rollback plan: the previous binary re-promotable, and an OTA revert path for JS.

## Android fallback
APK/sideload distribution is a real fallback if Play rejects, and is the practical route for the exchange client in some regions. You lose auto-update trust and Play Integrity, so treat it as secondary distribution, not primary.
