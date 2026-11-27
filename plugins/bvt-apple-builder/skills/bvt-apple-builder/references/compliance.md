# Compliance: what gets an upload or a review refused

This is build guidance, not legal advice. Where a line says "the user decides", do not decide for them.

## 1. Hard stops (check before any upload)

| Check | Rule | If it fails |
|---|---|---|
| Wallet app, account type | Guideline 3.1.5(i): wallets only from developers enrolled as an organisation | Stop. Enrol as an Organisation first |
| Exchange or other regulated finance | 3.1.5(iii) and 5.1.1(ix): licensed where offered, submitted by the legal entity that provides the service, not an individual | Limit the countries; put licence proof in the review notes |
| Account creation in the app | 5.1.1(v): an app that lets people create an account must let them delete it inside the app | Add Settings > Delete account. A non-custodial wallet with no account does not need it |
| On-device mining | 3.1.5(ii): not allowed | Remove it; a pool dashboard is fine |
| Crypto rewards for tasks | 3.1.5(v): no crypto for downloading apps, posting on social media and so on | Remove on iOS |
| Unlocking features with crypto | 3.1.1: digital features are unlocked with In-App Purchase | Use IAP, or do not sell the feature in the iOS app |
| Social login as the main sign-in | 4.8: also offer an equal login option that asks only for name and email, lets the user hide the email, and does not track for ads without consent | Add Sign in with Apple (it meets all three), or use only the company's own login |
| NFTs or tokens that unlock features | 3.1.1: owning an NFT or paying with crypto may not unlock features or content | Remove the unlock on iOS, or sell it as In-App Purchase |
| Hidden or switched-off features | 2.5.19: no hidden, dormant or undocumented features | Remove them, or show and describe them to the reviewer |
| ICOs, futures, crypto-securities trading | 3.1.5(iv): only from established financial institutions, within the law | Leave out of the iOS app unless that fits |
| Personal data sent to a third-party AI | 5.1.2(i): say so clearly and ask permission first | Add the disclosure and a consent step |
| Age rating questions | App Store Connect asks an updated age-rating questionnaire | Answer it in App Store Connect before submitting |

The guideline numbers in this file were checked against Apple's App Review Guidelines page on 27 November 2026. Apple edits the guidelines several times a year. Before a first submission, open the page and read the sections named above.

## 2. Privacy manifest (`PrivacyInfo.xcprivacy`)

A privacy manifest is a small file that tells Apple which sensitive system functions the app uses and why, and what data it collects. Without it the upload gets `ITMS-91053`.

- Make it: `python3 ${CLAUDE_SKILL_DIR}/scripts/privacy_manifest.py --out PrivacyInfo.xcprivacy --api userdefaults` (add `--expo` to get the `app.json` form).
- Common reason codes: UserDefaults `CA92.1`, file timestamps `C617.1`, system boot time `35F9.1`, disk space `E174.1`, active keyboards `54BD.1`. A code from the wrong category gives `ITMS-91055`.
- Where it goes: Expo `app.json > expo.ios.privacyManifests`; native `Resources/PrivacyInfo.xcprivacy` listed in `project.yml`; Tauri and Flutter: add the file to the app target of the committed iOS project.
- Libraries must ship their own manifest. If the upload email names a library, update that library.
- The "App Privacy" answers in App Store Connect must say the same as this file. A wallet whose keys and seed phrase never leave the device can truthfully answer that it does not collect that data.

## 3. Export compliance (encryption question)

Every build needs an answer, or it waits in TestFlight as "Missing Compliance". The answer is the Info.plist key `ITSAppUsesNonExemptEncryption`.

```
Does the app use encryption?
 |
 +- Only what Apple's system gives (HTTPS, Keychain, CryptoKit) ......... NO  (exempt)
 |
 +- Own crypto code, used only to sign, hash or prove identity
 |  (for example signing a transaction, SHA-256, no hiding of data) ..... usually NO; the user confirms
 |
 +- Own crypto code that hides data (for example its own AES encryption
    of a seed backup, end-to-end chat, VPN) ............................ YES
        -> App Store Connect then asks more questions
        -> standard algorithms: usually no documents, but France may need a declaration
        -> non-standard algorithms: documents needed
```

- Where the key goes: Expo `expo.ios.config.usesNonExemptEncryption`; native `INFOPLIST_KEY_ITSAppUsesNonExemptEncryption` in `project.yml`; Tauri `src-tauri/Info.ios.plist`.
- A crypto wallet often sits in the second or third branch. Ask the user which crypto code the app uses and where, show the tree, and let the user choose. Record the choice in the repo README.
- Apple's page "Complying with Encryption Export Regulations" has the official wording. A yearly self-classification report to the US government can apply to some apps; whether it applies to this developer is a question for an export adviser.

## 4. Other items reviewers check

- Permission texts (`NS...UsageDescription`) say in plain words why the app needs the camera, Face ID, photos and so on.
- A working demo account or a funded test wallet, with steps, in the review notes (Guideline 2.1).
- Screenshots show the real app (2.3).
- The app does more than show a website (4.2), is the developer's own work and not a template with a new name (4.2.6), and is not a copy of many similar apps (4.3).
- A privacy policy URL that works.

## 5. Dates Apple has set (from its Upcoming Requirements page, read 27 November 2026)

| Since | Rule |
|---|---|
| 28 Apr 2026 | Uploads must be built with Xcode 26 or later and the iOS 26 family of SDKs |
| 9 Sep 2026 | iPhone and iPad apps must target iOS 13 or later |
| 31 Jan 2026 | The updated age rating questions must be answered, or updates are held |
| 1 May 2024 | Privacy manifest reasons required for the listed system functions, including those used by libraries |
| 17 Feb 2025 | Apps with no verified EU trader status are removed from the EU App Store |
| 18 Feb 2025 | Mac apps: remove the `com.apple.quarantine` mark from all files before upload |

No 2027 rule was listed on that date. Check the page before each release.

## 6. Not covered here

Alternative app stores in the EU, tax and payout setup, and country licences. See `more-targets.md`. Tell the user these exist when the app is offered in those places, and that they need their own check.
