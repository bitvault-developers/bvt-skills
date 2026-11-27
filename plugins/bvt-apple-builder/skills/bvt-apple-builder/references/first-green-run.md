# First green run: prove the whole path with an empty app

A "green run" is a cloud build that finishes with no error and puts the app in TestFlight.
Do this once with an almost empty Expo app before any real app. It proves the Apple account, the keys, the build service and TestFlight. After it, a failed build means a problem in the app, not in the setup.

```
empty Expo app -> EAS cloud Mac build -> App Store Connect -> TestFlight -> opens on the iPhone
       |                 |                       |                 |
   10 minutes       20-40 minutes          5-30 minutes        2 minutes
```

## Before starting

- [ ] Apple Developer Program membership is active (not "pending").
- [ ] Node.js LTS and Git are installed on the PC.
- [ ] An Expo account exists (free).
- [ ] A bundle ID is registered and an app record exists in App Store Connect (`setup-from-windows.md` section 2). Use a throwaway name such as `com.example.firstbuild`; a bundle ID cannot be reused or deleted after an upload, so do not use a real product's ID for this test.
- [ ] The TestFlight app is installed on one iPhone or iPad, signed in with an Apple ID that is a user in App Store Connect.

## Steps

1. Create the app:

```
npx create-expo-app@latest bvt-first-build
cd bvt-first-build
npm install -g eas-cli
eas login
```

2. In `app.json`, inside `"expo"`, set the iOS block (routes.md section 1 has the full block): `bundleIdentifier`, `supportsTablet`, `config.usesNonExemptEncryption` (an empty Expo app uses only the system's HTTPS, so `false`), `privacyManifests`.
3. Add `eas.json` from `templates/eas.json` and fill in `ascAppId` and `appleTeamId`.
4. Check the files: `python3 ${CLAUDE_SKILL_DIR}/scripts/validate.py <folder>` when the files are in Claude's workspace.
5. Link the project and build:

```
eas init
eas build --platform ios --profile production
```

EAS asks to sign in with the Apple ID and offers to create the certificate and profile. Answer yes. Wait for the build to finish.

6. Send it to Apple:

```
eas submit --platform ios --latest
```

EAS offers to create an App Store Connect API key for later uploads. Answer yes.

7. In App Store Connect > TestFlight, wait until the build shows as ready. Add yourself to an internal testing group. Open TestFlight on the iPhone and install.

## It is green when

- [ ] The build page on expo.dev says finished.
- [ ] The build shows in App Store Connect > TestFlight with no warning email from Apple.
- [ ] The app opens on a real iPhone.

## Write it down

Add a file `APPLE_BUILD_STATUS.md` to each app's repo and keep it up to date. Claude reads it at the start of Apple work and updates it after each first green run.

```
# Apple build status
| Route | First green run | Tool versions | Notes |
|---|---|---|---|
| Expo + EAS | 2026-12-03 | Expo SDK xx, eas-cli xx | API key stored on EAS |
| Tauri Mac .dmg | not yet | | |
| Tauri iPhone | not yet | | |
```

A route with "not yet" is untested. Say so each time that route is used.

## Order for the other routes

Each step adds one new thing, so a failure points to that one thing.

1. Expo + EAS (this page): proves account, keys, TestFlight.
2. Tauri Mac `.dmg`: adds the Developer ID certificate and notarization. No review needed.
3. Tauri iPhone: adds the generated iOS project and signing on a GitHub runner.
4. Native SwiftUI or Flutter on GitHub: adds fastlane match.
5. Mac App Store: adds the sandbox, two more certificates and a profile.

For each one: start with the framework's empty starter app, get it green, record it, then move the real app over.
