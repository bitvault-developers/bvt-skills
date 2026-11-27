# Release checklist

Run this before every upload. Tick each line with the user.

## A. Before the build

- [ ] `python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py <project folder>` shows no STOP lines.
- [ ] Hard stops in `compliance.md` section 1 are all clear (account type, account deletion, crypto rules).
- [ ] Bundle ID in the project equals the bundle ID in App Store Connect.
- [ ] Version (for example 1.0.0) and build number are higher than the last upload.
- [ ] The build uses an Xcode and SDK that Apple accepts today. Check Apple's "Upcoming Requirements" page. In November 2026 the rule was: built with Xcode 26 or later with the iOS 26 SDK. The Xcode version in the workflow is pinned.
- [ ] App icon: 1024x1024 PNG, no transparency (`scripts/make_icons.py`).
- [ ] iPad: if the app supports iPad, all four orientations are allowed, or the app is marked full-screen only.
- [ ] Every permission the app or its libraries use has a clear reason text (`NSCameraUsageDescription`, `NSFaceIDUsageDescription`, and so on).
- [ ] Privacy manifest is present and true (`compliance.md` section 2).
- [ ] Export compliance key is set, and the user chose the answer (`compliance.md` section 3).
- [ ] Capabilities agree in all three places (`capabilities.md`).
- [ ] No test keys, test servers or debug menus in the release build.

## B. After the upload

- [ ] The build really arrived: it shows in App Store Connect > TestFlight, or in `asc builds list`. A green upload step alone is not proof.
- [ ] Processing finished, and no email from Apple lists problems (`ITMS-...`).

## C. TestFlight

- [ ] Internal testers (people in the team) can install at once. External testers need a short Beta App Review first.
- [ ] "What to Test" text written.
- [ ] Tested on a real iPhone and, if supported, a real iPad: install, first launch, every main flow of the app, background and return, no network.
- [ ] Crashes and tester feedback checked (`quality-and-cost.md`).

## D. App Store submission

- [ ] App Privacy answers filled in App Store Connect, matching the privacy manifest, and a privacy policy URL that works.
- [ ] Age rating questionnaire answered.
- [ ] Screenshots in the sizes App Store Connect asks for (`store-listing.md`), showing the real app.
- [ ] Description, keywords, support URL.
- [ ] Review notes: what the app does, a demo account or funded test wallet with steps, how custody works, and licence proof where needed.
- [ ] Countries: only where the app is allowed to operate.
- [ ] Agreements in App Store Connect > Business are accepted; for paid apps or In-App Purchase, bank and tax details are complete.

## E. Crypto apps

Use the `bvt-appstore-release` skill for the full rules and review-note wording, and `compliance.md` for the hard stops. This is build guidance, not legal advice. Licensing questions go to a lawyer.

## F. Mac app given out as a download

- [ ] Signed with Developer ID Application, hardened runtime on.
- [ ] Notarized and stapled (`macos-notarize.md`).
- [ ] Checked on the cloud Mac: `spctl -a -vv "App.app"` says `accepted` and `source=Notarized Developer ID`.
- [ ] Opened once on a real Mac by a tester, from a fresh download, before publishing the link.
- [ ] Tauri updater key backed up (see `bvt-desktop-signing-updates`).

## G. After release

- [ ] Keep the previous build ready to go back to.
- [ ] Consider phased release for updates (App Store Connect > the version > Phased Release).
- [ ] Expo: JS-only fixes may go by `eas update`. Never use an update to change what Apple reviewed.
- [ ] Note the renewal dates (`quality-and-cost.md`).
