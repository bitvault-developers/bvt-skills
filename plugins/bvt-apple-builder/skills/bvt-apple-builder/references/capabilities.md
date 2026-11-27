# Capabilities without a Mac

A capability is a special Apple feature an app must be allowed to use (push, Face ID login links, Sign in with Apple). Three places must agree, or the build or upload fails:

```
1. App ID in the developer portal  -> capability ticked
2. Provisioning profile            -> made again AFTER step 1
3. Entitlements file in the app    -> has the matching key
```

After changing step 1, always renew the profile: lane `certs` (native, Flutter, bare RN), or EAS does it on the next build, or Tauri automatic signing does it.

Where the entitlements live:

| Route | Place |
|---|---|
| Expo | `app.json > expo.ios.entitlements`, plus helpers such as `expo.ios.associatedDomains` and `expo.ios.usesAppleSignIn` |
| Native SwiftUI | `Resources/App.entitlements` |
| Tauri | the `.entitlements` file inside the committed `src-tauri/gen/apple` project |
| Flutter / bare RN | `ios/Runner/Runner.entitlements` or `ios/<App>/<App>.entitlements` |

## Push notifications

1. Developer portal > Keys > "+" > Apple Push Notifications service (APNs). Download the `.p8` once. This is a different key from the App Store Connect API key.
2. Tick Push Notifications on the App ID. Renew the profile.
3. Entitlement: `aps-environment` = `production` (TestFlight and App Store builds).
4. Sender: Expo push service (`expo-notifications`; `eas credentials` uploads the APNs key), or Firebase Cloud Messaging (upload the same `.p8` in the Firebase console), or the app's own server.
5. Push only works on a real iPhone. For a wallet, never put addresses or balances in the push text (see `bvt-push-privacy`).

## Universal links (https links that open the app)

1. Tick Associated Domains on the App ID. Renew the profile.
2. Entitlement: `com.apple.developer.associated-domains` = `["applinks:REPLACE_DOMAIN"]`.
3. Host `templates/resources/apple-app-site-association` at `https://REPLACE_DOMAIN/.well-known/apple-app-site-association`. No file extension, content type `application/json`, HTTPS, no redirect.
4. Test: open the link from the Notes app on a real iPhone. Typing it in Safari's address bar does not open the app.

## Sign in with Apple

Tick the capability on the App ID; entitlement `com.apple.developer.applesignin` = `["Default"]`. Expo: `expo-apple-authentication` and `usesAppleSignIn: true`.

## Face ID, Keychain, Secure Enclave

- Face ID needs only the text `NSFaceIDUsageDescription`. No capability.
- The Keychain needs no capability for the app's own items. Sharing items between apps needs Keychain Sharing or App Groups.
- Key storage rules for wallets: `bvt-mobile-secure-storage`.

## In-App Purchase and subscriptions

Products are created in App Store Connect. Code uses StoreKit 2, a library such as `react-native-iap`, or RevenueCat. A Paid Apps agreement, bank and tax details must be complete in App Store Connect > Business first. Sandbox testing needs a real device and a sandbox tester account.

## Background modes, App Groups, iCloud

Each is a tick on the App ID plus an entitlement or Info.plist key. First-time setup by trial and error on a cloud runner is slow. If three builds fail on the same capability, suggest one rented Mac day (`no-mac-limits.md`).
