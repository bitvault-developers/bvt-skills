# More targets and regions: what this plugin only points to

These are possible without a Mac but have no ready template here. Say that plainly, read the framework's current docs first, and build the files with the user step by step.

## Extra parts of an iPhone app

Each one is a second "target" inside the same app. A target has its own bundle ID (for example `com.example.wallet.widget`), its own provisioning profile, and often an App Group to share data with the main app.

| Part | What it is | Notes without a Mac |
|---|---|---|
| Widget, Live Activity | Small views on the home screen or lock screen, written in SwiftUI | Expo: through a config plugin or Expo's own widget support; check the current Expo docs. Native: a second target in `project.yml`. Needs an App Group |
| Notification service extension | Changes a push before it shows (for example to decrypt it) | Second target; needed for private push content |
| App Clip | A small part of the app that opens from a link or code | Second target with strict size limits |
| Share extension | The app appears in the system share sheet | Second target |
| watchOS app | Apple Watch companion | Extra target and extra screenshots; hard to test without a watch |

Signing for extra targets: every target's bundle ID must be registered, and every one needs a profile. fastlane match takes a list of bundle IDs in the `Matchfile`. EAS handles extra targets it knows about from the config plugin.

Previews and the simulator help a lot for widgets. If three builds fail on a widget, suggest one rented Mac day (`no-mac-limits.md`).

## Other Apple devices

| Device | Route |
|---|---|
| Mac | Tauri (`routes.md` section 3), or the iPhone/iPad app offered on Apple-silicon Macs with no extra build |
| Apple TV (tvOS), Vision Pro (visionOS) | Native SwiftUI target with `platform: tvOS` or `visionOS` in `project.yml`. The same Xcode and SDK upload rule applies |

## European Union

- Trader status: Apple asks every developer to declare in App Store Connect whether they are a "trader" under the EU Digital Services Act. Apps without a verified status are not available in the EU App Store. Do this in App Store Connect > Business before choosing EU countries.
- Other app stores and web distribution in the EU exist under Apple's alternative terms. They have their own agreement, fees and notarization step. Not covered here; the user reads Apple's EU pages before deciding.

## Money and legal setup

Bank and tax forms in App Store Connect > Business, local tax on proceeds, and licences for financial services are outside this plugin. Name them when the app is paid, has In-App Purchase, or is a financial service, and say they need the user's accountant or lawyer.
