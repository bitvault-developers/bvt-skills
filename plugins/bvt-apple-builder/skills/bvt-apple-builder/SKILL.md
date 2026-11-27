---
name: bvt-apple-builder
description: Builds, signs and ships iPhone, iPad and Mac apps with no Mac, using cloud Mac builders. Use for iOS, iPadOS or macOS builds of Expo, Tauri, Flutter or SwiftUI apps, TestFlight and build errors.
metadata:
  version: "0.3.0"
---

# BVT Apple Builder

Take an app from idea to an installable iPhone, iPad or Mac app when the user has no Mac.

## The one fact everything rests on

An App Store build must be compiled by Xcode, and Xcode runs only on macOS. So the plan is always the same:

```
Claude writes code + build files
        |
        v
user pushes to GitHub (or runs one EAS command on Windows)
        |
        v
a Mac in the cloud builds it  ---- fails? ---> log comes back, Claude fixes, build again
        |
        v
iPhone / iPad: TestFlight -> App Store        Mac: signed + notarized .dmg, or Mac App Store
```

Never suggest these as a release route: macOS in a virtual machine on a PC, a "Hackintosh", jailbreak tools, re-signing tools, or xtool. They break Apple's licence or cannot reach the App Store.

## How to work with this user

- The user works on Windows and Android and has no Mac. Write every file in full and give exact commands. The user runs them and pastes the result back. Do not require Claude Code.
- Use simple words and short sentences. Explain each technical word once, in one line.
- For every manual step on a website, give the menu path and a link to the official page that shows it (list at the end of `references/setup-from-windows.md`). Add a small text diagram when it helps.
- Never ask the user to open Xcode. Projects are made from text files (XcodeGen, Tauri, Flutter, Expo).
- Never ask the user to paste a `.p8` key, a `.p12` certificate, a password or a token into chat. These go into GitHub Secrets, EAS or Codemagic only. If the user pastes one, tell them to revoke it and make a new one.
- Give complete files, not fragments, so the user can copy and replace.
- Do not say a build works until the user reports a green build. Every template here is a starting point written from the vendors' docs; none has been run on this user's projects. Say "untested" until the first green run of that route.

## Step 1 - Pick ONE route

| App is made with | Build on | Templates | Mac needed |
|---|---|---|---|
| React Native + Expo | Expo EAS | `templates/eas.json`, `templates/eas-workflow-release-ios.yml` | Never |
| Tauri v2, iPhone/iPad | GitHub Actions Mac runner | `templates/tauri-ios.yml`, `templates/resources/tauri-Info.ios.plist` | Never |
| Tauri v2, Mac desktop download | GitHub Actions Mac runner | `templates/tauri-macos.yml` | Never |
| Tauri v2, Mac App Store | GitHub Actions Mac runner | `templates/tauri-mas.yml`, `templates/resources/tauri.appstore.conf.json`, `templates/resources/mac-app-store-Entitlements.plist` | Never |
| Flutter | Codemagic, or GitHub Actions | `templates/codemagic.yaml`, or `templates/flutter-ios.yml` + `templates/fastlane/Fastfile.existing-project` | Never |
| React Native without Expo | GitHub Actions + fastlane | `templates/rn-bare-ios.yml` + `templates/fastlane/Fastfile.existing-project` | Never |
| Native SwiftUI (new app) | GitHub Actions + XcodeGen + fastlane | `templates/ios-native.yml`, `templates/project.yml`, `templates/fastlane/`, `templates/resources/` | Never |
| Single-file JSX / web app | No build: PWA. Or wrap it in Expo | - | Never |

Rules for choosing:

1. If the app already exists, keep its framework. Do not rewrite an app to change route.
2. For a new app with Android + iPhone, prefer Expo. It is the route with the least to go wrong without a Mac.
3. Choose native SwiftUI only when the app is Apple-only or needs deep Apple features.
4. iPhone and iPad apps also run on Apple-silicon Macs through the Mac App Store unless the developer opts out. For many apps this covers "MacBook" with no extra build. Use a real Mac build (Tauri) for a desktop-class app.
5. Prove the whole path once with the easiest route (Expo) and an almost empty app before building other routes: `references/first-green-run.md`.
6. If the app's repo has `APPLE_BUILD_STATUS.md`, read it first. A route with no recorded green run is untested; say so. Update the file after each first green run.

Details and exact commands for each route: `references/routes.md`.

## Step 2 - Check the one-time setup

Ask which of these are done, then guide only the missing ones from `references/setup-from-windows.md`:

1. Apple Developer Program membership (Organisation account for a crypto wallet).
2. Bundle ID registered and app record created in App Store Connect.
3. App Store Connect API key made (Key ID, Issuer ID, `.p8` file).
4. Secrets stored where the chosen route needs them.
5. One real iPhone or iPad available for TestFlight.

Signing files, renewals and the `asc` command-line tool: `references/asc-route.md` and the `apple-signing` skill.

## Step 3 - Write the files, then check them

1. Copy the template for the route, replace every `REPLACE_...` value, and return complete files with their paths. State which values the user must fill in and where each one comes from.
2. Add the compliance files every route needs: privacy manifest and export compliance key (`references/compliance.md`).
3. When code execution is available and the files are in the workspace, run the checker and fix what it reports before the user starts a build:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py <project folder>
python3 ${CLAUDE_SKILL_DIR}/scripts/privacy_manifest.py --out PrivacyInfo.xcprivacy --api userdefaults
python3 ${CLAUDE_SKILL_DIR}/scripts/make_icons.py <picture> <Assets.xcassets folder>
```

The checker finds known mistakes (old action versions, deprecated upload command, unpinned Xcode, missing compliance files, placeholders, keys in the repo). A clean result does not prove the build will pass.

## Step 4 - Build loop

1. The user starts the build (EAS command or workflow, "Run workflow" in the GitHub Actions tab, a Codemagic build). With the Expo connector connected, Claude may start EAS builds and workflows after asking (`references/connectors.md`).
2. On failure, get the first error and about 100 lines around it, not only the end of the log. Read it through a connector when one is present; otherwise the user pastes it or runs `gh run view --log-failed`.
3. Match the error in `references/ci-log-triage.md`. Give the cause in one sentence and the fixed file in full.
4. Fix one cause at a time. Cloud Mac minutes cost money, so do not guess with several pushes.
5. After the upload step, confirm the build really arrived in TestFlight. A green step alone is not proof.

## Step 5 - Ship

Run `references/release-checklist.md` before every upload. Other files for this step:

| Need | File |
|---|---|
| Rules that get apps refused, privacy manifest, encryption question | `references/compliance.md` |
| Push, universal links, Sign in with Apple, IAP, Face ID | `references/capabilities.md` |
| Screenshots and store text | `references/store-listing.md` |
| Tests, crashes, versions, yearly renewals, cost | `references/quality-and-cost.md` |
| Mac app as a download | `references/macos-notarize.md` |
| Widgets, watch, TV, Vision Pro, EU rules | `references/more-targets.md` |

## Use these BVT skills together with this one, when installed (from the same bvt-skills marketplace)

- `bvt-ci-mobile-no-mac`: Expo release pipeline and how to stay on the free tier.
- `bvt-appstore-release`: Apple and Google crypto rules, review notes. It is the source for policy; this skill is the source for build mechanics.
- `bvt-desktop-signing-updates`, `bvt-tauri-desktop`: desktop signing and the Tauri updater key.
- `bvt-rn-expo-conventions`, `bvt-mobile-secure-storage`, `bvt-push-privacy`, `bvt-app-design-system`: code, key storage, push and theme.

## When a Mac is really needed

See `references/no-mac-limits.md`. Say so plainly when the task is one of those cases, and give the cheapest way (rent a cloud Mac for one day).

## Facts that go stale

Check the vendor page before stating any of these: prices and free limits, the Xcode version Apple requires for uploads, the Xcode versions on the GitHub runner, action versions, Flutter and Tauri behaviour, `asc` command flags, App Review Guideline numbers. The notes in the reference files were collected in November 2026.
