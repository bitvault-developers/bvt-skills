# Routes: exact steps for each kind of app

All commands run on Windows (PowerShell or Git Bash) unless marked "on the cloud Mac".
Status of every template: written from the vendors' docs, not yet run on this user's projects. Say so until the user reports a green build.

## Contents

1. Expo (React Native) with EAS
2. Tauri v2 for iPhone and iPad
3. Tauri v2 for Mac desktop (download, and Mac App Store)
4. Flutter (Codemagic, or GitHub Actions)
5. Bare React Native (no Expo)
6. Native SwiftUI with XcodeGen + fastlane
7. Web app as a PWA
8. Other frameworks
9. Testing with no iPhone or Mac

---

## 1. Expo (React Native) with EAS

EAS = Expo's cloud build service. It has Macs; the user does not need one.

Files: `eas.json` (from `templates/eas.json`), optional `.eas/workflows/release-ios.yml` (from `templates/eas-workflow-release-ios.yml`), and in `app.json`:

```json
{
  "expo": {
    "ios": {
      "bundleIdentifier": "REPLACE_BUNDLE_ID",
      "supportsTablet": true,
      "config": { "usesNonExemptEncryption": false },
      "privacyManifests": {
        "NSPrivacyAccessedAPITypes": [
          {
            "NSPrivacyAccessedAPIType": "NSPrivacyAccessedAPICategoryUserDefaults",
            "NSPrivacyAccessedAPITypeReasons": ["CA92.1"]
          }
        ]
      }
    }
  }
}
```

- `supportsTablet: true` makes it a real iPad app, not a stretched iPhone app.
- `usesNonExemptEncryption`: decide the value with `compliance.md`. Do not leave it out.
- `privacyManifests`: make the right content with `scripts/privacy_manifest.py --expo`.
- In `eas.json`, set `cli.version` to the major version the user has (`eas --version`).

Way A, commands:

```
npm install -g eas-cli
eas login
eas build:configure
eas build --platform ios --profile production
eas submit --platform ios --latest
```

Way B, one workflow (build, then TestFlight): commit `.eas/workflows/release-ios.yml`, then `eas workflow:run release-ios.yml`. With the Expo connector connected, Claude can start it and read its logs (`connectors.md`).

- On the first iOS build EAS asks to sign in with the Apple ID. It then makes the certificate and provisioning profile and stores them. Let EAS manage them.
- To put a test build straight on one iPhone without TestFlight: `eas device:create` (opens a link on the iPhone to register it), then `eas build --platform ios --profile preview`.
- JS-only changes do not need a new build: `eas update`. Native changes (new native library, permission, icon) need a build.
- `eas build --local` for iOS needs a Mac. Always use cloud builds.

## 2. Tauri v2 for iPhone and iPad

Files:

- `.github/workflows/tauri-ios.yml` from `templates/tauri-ios.yml`
- `src-tauri/Info.ios.plist` from `templates/resources/tauri-Info.ios.plist` (export compliance key and permission texts)
- in `src-tauri/tauri.conf.json`: `identifier` equal to the registered bundle ID, a `version`, and

```json
{
  "bundle": {
    "iOS": {
      "developmentTeam": "REPLACE_TEAM_ID",
      "minimumSystemVersion": "15.0",
      "infoPlist": "Info.ios.plist"
    }
  }
}
```

`bundle.iOS.infoPlist` names the extra Info.plist file (path from the `src-tauri` folder). `bundle.iOS.bundleVersion` also exists if a fixed build number is wanted; the template passes the build number on the command line.

Secrets: `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8_BASE64`, `ASC_APP_ID`, `APPLE_TEAM_ID`.

The iOS project folder (`src-tauri/gen/apple`) can only be created on macOS. The workflow handles this:

```
first run:  no gen/apple in repo -> runner creates it -> saved as artifact "tauri-ios-project"
user:       download artifact -> unzip into src-tauri/gen/apple -> commit
later runs: use the committed folder (entitlements and settings edits are kept)
```

Signing:

- Automatic (default in the template): Tauri reads `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH` and lets Xcode make the certificate and profile. Tauri's docs ask for an API key with Admin access. It fails if the Apple account has no registered device; register one iPhone first.
- Manual (use when automatic keeps failing): set `IOS_CERTIFICATE` (base64 `.p12`, Apple Distribution), `IOS_CERTIFICATE_PASSWORD`, `IOS_MOBILE_PROVISION` (base64 App Store profile). Get the files with the asc tool (`asc-route.md`) or the developer portal.

Upload: the template uses `xcrun altool --upload-package` with the numeric app ID. The older `--upload-app` is deprecated; do not use it.

Things that differ from desktop Tauri:

- Desktop-only plugins (tray, global shortcut, updater, window controls) do not exist on iOS. Guard them with `#[cfg(desktop)]`.
- `src-tauri/src/lib.rs` must hold the app's `run` function with the mobile entry point attribute, and `Cargo.toml` needs the `staticlib` and `cdylib` crate types. `tauri ios init` reports what is missing.
- Upgrade the Tauri CLI, core and plugins together before the first iOS build.

## 3. Tauri v2 for Mac desktop

| Way | Certificate | Result |
|---|---|---|
| Download from the website | Developer ID Application | signed + notarized `.dmg` |
| Mac App Store | Apple Distribution + Mac Installer Distribution | `.pkg` uploaded to App Store Connect |

Start with the website download. It needs no review.

### Download (.dmg)

Files: `.github/workflows/tauri-macos.yml` from `templates/tauri-macos.yml`.

Secrets: `APPLE_CERTIFICATE` (base64 of the Developer ID `.p12`), `APPLE_CERTIFICATE_PASSWORD`, `APPLE_SIGNING_IDENTITY`, `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8_BASE64`. How to make the `.p12` on Windows: `setup-from-windows.md`.

The Tauri bundler signs, notarizes and staples on the runner. The `.dmg` is saved as a workflow artifact.

### Mac App Store (.pkg)

Files:

- `.github/workflows/tauri-mas.yml` from `templates/tauri-mas.yml`
- `src-tauri/Entitlements.plist` from `templates/resources/mac-app-store-Entitlements.plist`
- `src-tauri/tauri.appstore.conf.json` from `templates/resources/tauri.appstore.conf.json`
- in `tauri.conf.json`: `bundle.category` (for example `Finance`), and a `src-tauri/Info.plist` holding `ITSAppUsesNonExemptEncryption` (Tauri merges this file into the Mac app's Info.plist)

One-time: add the macOS platform to the app record in App Store Connect, register the bundle ID for macOS, make two certificates (Apple Distribution, Mac Installer Distribution) and a Mac App Store provisioning profile. Steps from Windows: `setup-from-windows.md`, section "Mac App Store".

What the workflow does on the cloud Mac:

```
build universal .app, signed with Apple Distribution + sandbox entitlements + embedded profile
   -> remove the "quarantine" mark from files
   -> productbuild: wrap it in a .pkg signed with Mac Installer Distribution
   -> altool --upload-package to App Store Connect
```

The App Sandbox limits what the app can do (files outside its own folder, child processes, some network uses). Add an entitlement for each need (for example `com.apple.security.files.user-selected.read-write`). Mac App Store apps are not notarized; App Review replaces that step. Test the sandboxed build from TestFlight for Mac before submitting.

## 4. Flutter

`flutter create` on Windows already makes the `ios/` folder. Only the build needs a Mac.

Way A, Codemagic: `codemagic.yaml` in the repo root from `templates/codemagic.yaml`. One-time in the Codemagic website: connect the repo; add the App Store Connect API key under Team integrations with the same name as in the yaml file. Codemagic fetches or creates the signing files.

Way B, GitHub Actions: `.github/workflows/flutter-ios.yml` from `templates/flutter-ios.yml`, plus in `ios/`: `Gemfile`, `fastlane/Fastfile` (from `templates/fastlane/Fastfile.existing-project`), `fastlane/Matchfile`, `fastlane/Appfile`. Run lane `certs` once, then `beta`.

Set the bundle ID by search-and-replace of `PRODUCT_BUNDLE_IDENTIFIER` in `ios/Runner.xcodeproj/project.pbxproj` (a text file).

Newer Flutter versions use Swift Package Manager instead of CocoaPods for iOS plugins. Check the Flutter release notes for the installed version; do not add a `pod install` step unless an `ios/Podfile` exists.

Mac desktop from Flutter: `flutter build macos` on the cloud Mac, then sign and notarize as in `macos-notarize.md`.

## 5. Bare React Native (no Expo)

Prefer moving the app to Expo (prebuild) + EAS when possible. Otherwise: `.github/workflows/rn-bare-ios.yml` from `templates/rn-bare-ios.yml`, plus in `ios/`: `Gemfile` with both `fastlane` and `cocoapods`, and the same fastlane files as Flutter way B. Replace `REPLACE_APP` with the Xcode project name.

## 6. Native SwiftUI with XcodeGen + fastlane

- XcodeGen = a tool that makes the Xcode project from one text file (`project.yml`). No Xcode window needed.
- fastlane = a tool that runs signing, building and uploading from a script.
- match = the part of fastlane that keeps certificates and profiles, encrypted, in a private git repo.

Repo layout:

```
project.yml                          <- templates/project.yml
Sources/AppMain.swift                <- templates/swiftui-starter/AppMain.swift
Sources/Assets.xcassets/             <- make with scripts/make_icons.py
Resources/PrivacyInfo.xcprivacy      <- scripts/privacy_manifest.py or templates/resources/
Resources/App.entitlements           <- templates/resources/App.entitlements
Gemfile                              <- templates/fastlane/Gemfile
fastlane/Fastfile  Appfile  Matchfile
.github/workflows/ios-native.yml
```

First run: start the workflow with lane `certs`. It creates the certificate and profile through the API key and saves them in the match repo. After that, run lane `beta` for every build.

Secrets: `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_P8_BASE64`, `ASC_APP_ID`, `APPLE_TEAM_ID`, `MATCH_GIT_URL`, `MATCH_PASSWORD`, `MATCH_GIT_BASIC_AUTHORIZATION`.

For a Mac version of the same SwiftUI app, add a second target to `project.yml` and a second lane. No ready template yet; this is the shape, to be checked against the fastlane docs when first used:

```yaml
  AppMac:
    type: application
    platform: macOS
    deploymentTarget: "13.0"
    sources: [Sources]
    scheme: {}
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: REPLACE_BUNDLE_ID
        GENERATE_INFOPLIST_FILE: YES
        INFOPLIST_KEY_LSApplicationCategoryType: public.app-category.finance
        CODE_SIGN_ENTITLEMENTS: Resources/AppMac.entitlements   # must contain the App Sandbox key
```

```ruby
lane :mac_beta do
  setup_ci
  key = asc_key
  match(type: "appstore", platform: "macos", additional_cert_types: ["mac_installer_distribution"], readonly: true, api_key: key)
  build_mac_app(project: "App.xcodeproj", scheme: "AppMac", export_method: "app-store")
  upload_to_testflight(api_key: key, apple_id: ENV["ASC_APP_ID"], app_platform: "osx", skip_waiting_for_build_processing: true)
end
```

## 7. Web app as a PWA

PWA = a website that installs to the home screen from Safari: Share > Add to Home Screen. No Mac, no Apple fee, no review.

Limits on iPhone: no App Store listing, less access to phone features, push works only after it is added to the home screen, and browser storage is weaker than the iOS Keychain. Good as a first step. Not a place to keep wallet keys. A web page wrapped in an app shell with nothing native is often rejected (Guideline 4.2).

## 8. Other frameworks

Capacitor / Ionic, Kotlin or Compose Multiplatform, .NET MAUI: the iPhone part is always an Xcode project. Use the bare React Native workflow as the pattern (checkout, pinned Xcode, framework build step, fastlane with `Fastfile.existing-project`). No ready template yet; write it with the user and say it is new.

Widgets, App Clips, watchOS, Live Activities: each is an extra target with its own bundle ID and profile. Possible on every route but not covered here. Search the framework's current docs first.

## 9. Testing with no iPhone or Mac

| Need | Use |
|---|---|
| Real testers | TestFlight. Internal testers get builds at once; external testers after Beta App Review. Builds expire after 90 days |
| Own iPhone, Expo app | development build + `eas device:create` |
| See the app in a browser | Appetize.io or BrowserStack with a simulator build (`eas build --profile simulator`) |
| Cloud simulator driven by Claude | Expo connector simulator tools (billed by Expo) |
| Automatic UI tests | Maestro or XCUITest on the cloud Mac's simulator (`quality-and-cost.md`) |

Buying one used iPhone is worth it. A wallet app should not be released without a test on a real device.
