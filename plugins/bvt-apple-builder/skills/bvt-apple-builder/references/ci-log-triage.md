# Reading a failed build log

## Method

1. Find the **first** line with `error:` or `❌`. The last lines of a log are usually only "exit code 65" and tell nothing.
2. Ask the user for that line plus about 50 lines above and below. On GitHub: open the failed step, use the search box in the log, search `error:`.
3. fastlane hides detail. The full Xcode log is in `~/Library/Logs/gym` on the runner; `templates/ios-native.yml` saves it as an artifact on failure. Ask for that file when the short log is not enough.
4. Name one cause, give one fix, return the full fixed file.
5. If the error is not in the tables below, say so. Search the exact error text before proposing a fix; do not invent one.

## Signing

| Log text | Cause | Fix |
|---|---|---|
| `No profiles for 'X' were found` / `requires a provisioning profile` | No profile for this bundle ID, or the bundle ID in the project differs from the registered one | Make them equal. Native route: run lane `certs`. Expo: `eas credentials` |
| `Provisioning profile "..." doesn't include the ... entitlement` / `doesn't support the ... capability` | The app uses a capability (push, Sign in with Apple, App Groups) that is not ticked on the App ID | Tick it under Identifiers in the developer portal, then make the profile again (lane `certs` with `force: true`, or EAS regenerates) |
| `No signing certificate "iOS Distribution" found` / `No certificate matching` | Certificate is not in the runner's keychain | Check `setup_ci` and `match` run before `build_app`; check the match secrets |
| Build hangs for many minutes at `CodeSign` | Keychain is locked and waiting for a password window | `setup_ci` is missing in the lane |
| `There are no devices registered in your account` / `no devices from which to generate a provisioning profile` | Automatic signing wants a development profile, and the team has zero devices | Register one iPhone or iPad: developer portal > Devices > "+", or `eas device:create` |
| `Could not decrypt the repo` / `Invalid password` (match) | Wrong `MATCH_PASSWORD` | Fix the secret. If the password is lost: empty the certificates repo, revoke the certificate in the portal, run `certs` again |
| `Authentication failed` while cloning the match repo | Bad `MATCH_GIT_BASIC_AUTHORIZATION` or token without access | Make the base64 of `user:token` again; give the token access to the certificates repo |
| `Maximum number of certificates generated` | Apple's limit on distribution certificates is reached | Revoke unused ones in the portal, or reuse the existing certificate |

## Talking to Apple

| Log text | Cause | Fix |
|---|---|---|
| `Authentication credentials are missing or invalid` / 401 | Wrong Key ID or Issuer ID, damaged `.p8`, or the secret is not base64 | Remake the secret with the PowerShell command; check there are no extra spaces or line breaks |
| 403 `A required agreement is missing or has expired` | A new Apple agreement is waiting | Account Holder accepts it at developer.apple.com and in App Store Connect > Business |
| 403 `This request is forbidden for security reasons` / role errors | API key role too low | Make a key with App Manager or Admin role |
| `The bundle version must be higher than the previously uploaded version` / `Redundant Binary Upload` | Build number was already used | Raise the build number. Templates use the workflow run number |
| `Invalid Pre-Release Train` / `The train version 'x' is closed` | That app version is already released | Raise the version (for example 1.0.0 to 1.0.1) |
| `ITMS-90725` / `SDK version issue` | Built with an Xcode older than Apple now accepts | Use a newer runner image and Xcode; Expo: `"image": "latest"` and a current Expo SDK |
| `ITMS-90683: Missing purpose string` | The app, or a library in it, touches camera, photos, Face ID, location and so on, with no text saying why | Add the `NS...UsageDescription` key named in the message |
| `ITMS-91053: Missing API declaration` / `ITMS-91061` | Privacy manifest missing for the app or a library | Add `PrivacyInfo.xcprivacy` (`compliance.md`); update the named library |
| `ITMS-91055: Invalid API declaration` | A reason code that does not belong to that API category | Fix the code; make the file again with `scripts/privacy_manifest.py` |
| `ITMS-90161: Invalid Provisioning Profile` | Wrong profile type, wrong team, or expired profile | Make the profile again (lane `certs`); check it is an App Store profile |
| Upload step is green but no build appears in TestFlight after 30 minutes | altool has reported success on failed uploads, or the build went to another app with a similar bundle ID | Pass the numeric app ID (`apple_id` / `--apple-id`); check with `asc builds list`; read the email Apple sends to the Account Holder |
| `--upload-app` warnings or odd upload failures | That altool command is deprecated | Use `--upload-package` with `--apple-id`, `--bundle-id`, `--bundle-version`, `--bundle-short-version-string` |
| `Missing required icon` / `ITMS-90022` / `ITMS-90713` | No AppIcon, or icon has transparency | 1024x1024 PNG, no alpha, in `AppIcon.appiconset` |
| TestFlight shows "Missing Compliance" | Encryption question not answered | Answer it in App Store Connect, or set `ITSAppUsesNonExemptEncryption` in Info.plist after the user decides the right answer |

## Build

| Log text | Cause | Fix |
|---|---|---|
| `Command PhaseScriptExecution failed with a nonzero exit code` | A script inside the build failed. The real error is above it | Scroll up. In React Native it is usually a JS bundling error or Node not found |
| `CocoaPods could not find compatible versions for pod` | Pod versions do not fit together | Expo: `npx expo install --fix`. Others: delete `Podfile.lock`, or raise the iOS deployment target |
| `The iOS deployment target ... is set to X, but the range of supported deployment target versions is ...` | Target too low for this Xcode or library | Raise the deployment target |
| `xcodebuild: error: ... does not exist` / `does not contain a scheme named` | Wrong path or scheme, or the project was not generated | Check `xcodegen generate` ran; scheme name equals the target name in `project.yml` |
| `No such module 'X'` | A Swift package or pod is missing | Add it under `packages:` in `project.yml`, or run pod install |
| `can't find crate for 'std'` / `target may not be installed` (Tauri) | Rust target missing | Add `aarch64-apple-ios` (iOS) or both darwin targets (Mac) to the toolchain step |
| `failed to find development team` (Tauri) | Team ID not set | `bundle.iOS.developmentTeam` in `tauri.conf.json` and `APPLE_DEVELOPMENT_TEAM` in the workflow |
| The job was cancelled after the time limit | Build is slower than the limit | Raise `timeout-minutes`; add caching. EAS free plan has its own time limit |
| `No space left on device` | Runner disk is full | Remove unused simulators or caches in a step before the build |
| Warning that an action uses a deprecated Node version, or an action fails to start | Old action major (`checkout@v4`, `upload-artifact@v4` and so on) | Use `checkout@v6`, `setup-node@v6`, `cache@v5`, `upload-artifact@v7` |
| Build worked last month, fails now with no code change | The runner's default Xcode moved | Pin the Xcode version; read the runner README for what is installed |
| `pod install` cannot find a new pod or version | CocoaPods' central index (trunk) is read-only from 2 December 2026; existing versions still install, new ones do not appear | Use the Swift Package version of the library; keep the existing `Podfile.lock` |
| Tauri: `Missing Info.plist key` or a permission prompt crashes the app | Reason text not in the app's Info.plist | Add it to `src-tauri/Info.ios.plist` |
| Tauri: plugin fails to link in the iOS build | CLI, core and plugins on different versions | Upgrade them together |
| Flutter: warning that a plugin does not support Swift Package Manager | Old plugin | Upgrade the plugin, or keep CocoaPods for now |

## Expo EAS

| Log text | Cause | Fix |
|---|---|---|
| Asks for an Apple login code and stops in CI | No stored credentials for a non-interactive build | Run the first build on the PC, where codes can be typed, or add the API key in `eas credentials` |
| `bundleIdentifier` errors | `ios.bundleIdentifier` missing in `app.json` | Add it; it must equal the registered bundle ID |
| Fails in "Install pods" after adding a library | Native library needs a config plugin or a newer SDK | `npx expo install <library>`, add its plugin to `app.json`, run `npx expo-doctor` |
| Queue waits a very long time | Free plan has low priority | Build at a quiet hour, or use a paid plan for that month |
| Workflow says credentials are not set up | Signing files were never created on EAS | Run `eas credentials` once on the PC (iOS, production) |
| Expo connector `build_run` refuses | No GitHub repo linked to the Expo project | Link the repo on expo.dev, or start the build with `eas build` |

## Mac notarization

| Log text | Cause | Fix |
|---|---|---|
| Status `Invalid` | Apple refused the file | Get the notary log: `rcodesign notary-log --api-key-file key.json <submission id>`. It lists each file and reason |
| `The executable does not have the hardened runtime enabled` | Signed without the hardened runtime | Sign with the runtime flag. Tauri does this by default |
| `The binary is not signed with a valid Developer ID certificate` | Signed with the wrong certificate type, or a helper binary inside is unsigned | Use Developer ID Application; sign every binary inside the app |
| `The signature does not include a secure timestamp` | No timestamp | Sign with a timestamp (default for Tauri and rcodesign) |
| Mac App Store upload refused, message about `com.apple.quarantine` | A file inside the app carries the download mark | `xattr -dr com.apple.quarantine App.app` before `productbuild` (the template does this) |
| Mac App Store: `App sandbox not enabled` / missing `application-identifier` | Entitlements file not applied, or profile not embedded | Check `tauri.appstore.conf.json` is passed with `--config`, and both files exist |
| `productbuild: error: Could not find appropriate signing identity` | Installer certificate not in the keychain, or wrong identity name | Check the three `MAS_INSTALLER_*` secrets; the name starts with `3rd Party Mac Developer Installer:` |
| `security: SecKeychainItemImport: MAC verification failed` | `.p12` made by OpenSSL 3 without `-legacy`, or wrong password | Make the `.p12` again with `-legacy`; check `APPLE_CERTIFICATE_PASSWORD` |

## App Review rejections

The message from Apple names a guideline number. Read the full message; reviewers often say exactly what to change.

| Guideline | Usual cause | Fix |
|---|---|---|
| 2.1 App Completeness | Crash, empty screens, login that the reviewer cannot pass | Fix it; give a working demo account or funded test wallet in the review notes |
| 2.3 Accurate Metadata | Screenshots or text do not match the app | Use real screens; remove claims the app does not meet |
| 3.1.1 In-App Purchase | Digital features sold or unlocked outside IAP | Use IAP, or remove the purchase from the iOS app |
| 3.1.5 Cryptocurrencies | Wallet from an individual account; exchange with no licence proof; on-device mining; crypto rewards for tasks | See `compliance.md` and `bvt-appstore-release` |
| 4.2 Minimum Functionality | App is a website in a shell | Add real native value: Face ID, offline use, push, widgets |
| 4.2.6 | App looks made from a commercial template | Submit own, original work under the owner's account |
| 4.3 Spam | Many near-identical apps | Merge them, or make each clearly different |
| 4.8 Login Services | Third-party login without a privacy-friendly option | Add Sign in with Apple |
| 5.1.1 Data Collection | Asks for data it does not need; no account deletion | Ask less; add in-app account deletion |
| 5.1.2 Data Use | Personal data sent to a third party, including AI services, without clear consent | Disclose and ask first |

Answer a rejection in App Store Connect's Resolution Center politely and to the point. Do not resubmit unchanged.
