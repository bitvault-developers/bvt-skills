# One-time setup, done from Windows and a web browser

Guide only the steps the user has not done. Everything here works without a Mac.

## 1. Apple Developer Program

- Cost: US$99 a year, charged in local currency. In India, enrolment is done in the Apple Developer app on an iPhone or iPad. Check Apple's enrolment page for the current price and steps.
- Individual account: the seller name is the person's own name. Fast.
- Organisation account: the seller name is the company. Needs a legal entity, a D-U-N-S number (a free company ID from Dun & Bradstreet), a website on the company's domain, and a work email. Allow one to several weeks.
- A crypto wallet must come from an Organisation account (App Review Guideline 3.1.5). Start the D-U-N-S request first; it is the slowest step.

## 2. Bundle ID and app record (web browser)

- Bundle ID = the app's unique name, for example `com.example.wallet`. It can never be changed after the first upload.
- developer.apple.com > Account > Certificates, Identifiers & Profiles > Identifiers > "+" > App IDs. Tick the capabilities the app uses (Push Notifications, Associated Domains, and so on).
- appstoreconnect.apple.com > Apps > "+" > New App. Pick the bundle ID. Note the numeric Apple ID of the app (App Information page). It is used everywhere as `ASC_APP_ID`: EAS, Codemagic, fastlane and altool all ask for it.

## 3. App Store Connect API key

This key lets the build tools talk to Apple with no password and no login codes.

- appstoreconnect.apple.com > Users and Access > Integrations > App Store Connect API > "+".
- Role: App Manager is enough for uploading. Tauri's automatic iOS signing asks for Admin.
- Write down the **Key ID** and the **Issuer ID**. Download the `.p8` file. Apple lets it be downloaded only once. Keep a copy in a password manager.
- Team ID: developer.apple.com > Account > Membership details.

## 4. Turn files into base64 text for secrets

GitHub secrets hold text, so files are stored as base64 text. In PowerShell:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("AuthKey_ABC123.p8")) | Set-Clipboard
```

Then paste into the secret. The same command works for a `.p12` file.

## 5. GitHub secrets

Repo > Settings > Secrets and variables > Actions > New repository secret.

| Secret | Value | Used by |
|---|---|---|
| `ASC_KEY_ID` | Key ID | all GitHub routes |
| `ASC_ISSUER_ID` | Issuer ID | all GitHub routes |
| `ASC_KEY_P8_BASE64` | base64 of the `.p8` file | all GitHub routes |
| `ASC_APP_ID` | numeric Apple ID of the app | all GitHub routes |
| `APPLE_TEAM_ID` | Team ID | all GitHub routes |
| `MATCH_GIT_URL` | https URL of the private certificates repo | native SwiftUI |
| `MATCH_PASSWORD` | a new long password, chosen by the user | native SwiftUI |
| `MATCH_GIT_BASIC_AUTHORIZATION` | base64 of `githubuser:token` | native SwiftUI |
| `APPLE_CERTIFICATE` | base64 of the Developer ID `.p12` | Tauri Mac |
| `APPLE_CERTIFICATE_PASSWORD` | the `.p12` password | Tauri Mac |
| `APPLE_SIGNING_IDENTITY` | `Developer ID Application: NAME (TEAMID)` | Tauri Mac |

Keep the app repo private. Never put these values in a file in the repo.

Secrets can also be set from the PC with the GitHub CLI: `gh secret set ASC_KEY_ID` (it asks for the value and does not show it). For a file: `gh secret set ASC_KEY_P8_BASE64 < key-base64.txt`.

## 6. fastlane match repo (native SwiftUI route only)

1. Create a second, empty, private GitHub repo, for example `bvt-certificates`.
2. Create a fine-grained personal access token with read and write access to that one repo only.
3. Make the value for `MATCH_GIT_BASIC_AUTHORIZATION`:

```powershell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("GITHUB_USERNAME:TOKEN")) | Set-Clipboard
```

4. Run the workflow once with lane `certs`. Keep `MATCH_PASSWORD` safe: without it the stored certificates cannot be read.

## 7. Developer ID certificate without a Mac (Mac download route only)

Only the Account Holder of the team can create Developer ID certificates. OpenSSL comes with Git for Windows (use Git Bash).

```bash
# 1. private key + certificate request
openssl genrsa -out developer_id.key 2048
openssl req -new -key developer_id.key -out developer_id.csr -subj "/emailAddress=REPLACE_EMAIL/CN=REPLACE_NAME/C=IN"

# 2. developer.apple.com > Certificates > "+" > Developer ID Application
#    upload developer_id.csr, download developerID_application.cer

# 3. turn it into a .p12
openssl x509 -inform DER -in developerID_application.cer -out developer_id.pem
openssl pkcs12 -export -legacy -inkey developer_id.key -in developer_id.pem -out developer_id.p12
```

- `-legacy` matters with OpenSSL 3: without it the Mac runner often cannot import the file. If the installed OpenSSL does not know `-legacy`, leave it out.
- The signing identity text is the certificate's name, in the form `Developer ID Application: Company Name (TEAMID)`. Read it with `openssl x509 -in developer_id.pem -noout -subject`.
- Store `developer_id.key` and `developer_id.p12` offline. Do not commit them.

## 7b. Mac App Store certificates and profile (Mac App Store route only)

Same OpenSSL method as section 7, done twice, for two other certificate types. Only the Account Holder or an Admin can create distribution certificates.

```bash
# app certificate
openssl genrsa -out mas_app.key 2048
openssl req -new -key mas_app.key -out mas_app.csr -subj "/emailAddress=REPLACE_EMAIL/CN=REPLACE_NAME/C=IN"
# portal > Certificates > "+" > Apple Distribution > upload mas_app.csr > download distribution.cer
openssl x509 -inform DER -in distribution.cer -out mas_app.pem
openssl pkcs12 -export -legacy -inkey mas_app.key -in mas_app.pem -out mas_app.p12

# installer certificate
openssl genrsa -out mas_installer.key 2048
openssl req -new -key mas_installer.key -out mas_installer.csr -subj "/emailAddress=REPLACE_EMAIL/CN=REPLACE_NAME/C=IN"
# portal > Certificates > "+" > Mac Installer Distribution > upload mas_installer.csr > download mac_installer.cer
openssl x509 -inform DER -in mac_installer.cer -out mas_installer.pem
openssl pkcs12 -export -legacy -inkey mas_installer.key -in mas_installer.pem -out mas_installer.p12
```

- A team may hold only a small number of distribution certificates. If an Apple Distribution certificate already exists (made by EAS or fastlane match), its private key lives there; make a new one only if the limit allows, or reuse the existing files.
- Identity names for the secrets: read each with `openssl x509 -in <file>.pem -noout -subject`. They look like `Apple Distribution: Company (TEAMID)` and `3rd Party Mac Developer Installer: Company (TEAMID)`.
- Profile: portal > Profiles > "+" > Mac App Store Connect > pick the App ID and the Apple Distribution certificate > download. Store its base64 as `MAS_PROFILE_BASE64`.

| Secret | Value |
|---|---|
| `MAS_APP_CERT_P12_BASE64`, `MAS_APP_CERT_PASSWORD`, `MAS_APP_SIGNING_IDENTITY` | Apple Distribution `.p12`, its password, its identity name |
| `MAS_INSTALLER_P12_BASE64`, `MAS_INSTALLER_P12_PASSWORD`, `MAS_INSTALLER_IDENTITY` | Mac Installer Distribution `.p12`, its password, its identity name |
| `MAS_PROFILE_BASE64` | Mac App Store provisioning profile |

## 8. Register a test iPhone or iPad (needed for development builds and for Tauri automatic signing)

- Expo way, also fine for non-Expo apps: `eas device:create` gives a link or QR code. Open it on the iPhone and install the small profile. The device is then registered on the Apple account.
- Web way: developer.apple.com > Devices > "+", with the device's UDID. On Windows, the Apple Devices app (or iTunes) shows the UDID when the serial number is clicked.

## 8b. Expo

`eas login`, then the first `eas build --platform ios` creates and stores the signing files. To avoid Apple ID prompts later, add the API key in `eas credentials` or on expo.dev under the project's credentials.

## 9. Codemagic (Flutter)

codemagic.io > Teams > Integrations > Developer Portal > add the API key (Key ID, Issuer ID, `.p8`). Give it a name and use the same name in `codemagic.yaml`.

## 10. Fewer website steps: the asc tool

Many of the steps above (signing files, uploads, TestFlight, store text) can be done from the Windows command line with the unofficial `asc` tool. See `asc-route.md`.

## Official pages with pictures (give these links with each step)

- Apple, enrolment: https://developer.apple.com/programs/enroll/
- Apple, create an API key: https://developer.apple.com/documentation/appstoreconnectapi/creating-api-keys-for-app-store-connect-api
- Apple, TestFlight: https://developer.apple.com/testflight/
- Apple, upcoming upload requirements: https://developer.apple.com/news/upcoming-requirements/
- Apple, App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- Expo, first build: https://docs.expo.dev/build/setup/
- Expo, submit to the App Store: https://docs.expo.dev/submit/ios/
- GitHub, Apple certificates on Mac runners: https://docs.github.com/en/actions/use-cases-and-examples/deploying/installing-an-apple-certificate-on-macos-runners-for-xcode-development
- GitHub, runner images and Xcode versions: https://github.com/actions/runner-images
- Tauri, App Store: https://v2.tauri.app/distribute/app-store/
- Tauri, iOS signing: https://v2.tauri.app/distribute/sign/ios/
- Tauri, macOS signing: https://v2.tauri.app/distribute/sign/macos/
- fastlane match: https://docs.fastlane.tools/actions/match/
- Codemagic, Flutter: https://docs.codemagic.io/yaml-quick-start/building-a-flutter-app/
- rcodesign: https://gregoryszorc.com/docs/apple-codesign/stable/
- Apple, altool upload guide: https://help.apple.com/asc/appsaltool/
- Apple, privacy manifest reasons: https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api
- Expo, EAS Workflows jobs: https://docs.expo.dev/eas/workflows/pre-packaged-jobs/
- Expo connector: https://docs.expo.dev/mcp/
- asc tool: https://github.com/rorkai/App-Store-Connect-CLI
- Claude plugins: https://claude.com/docs/plugins/build
