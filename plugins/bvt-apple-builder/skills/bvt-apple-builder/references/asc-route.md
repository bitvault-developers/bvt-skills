# The asc tool: App Store Connect from the Windows command line

`asc` (App Store Connect CLI, repo `rorkai/App-Store-Connect-CLI`, MIT licence) is an unofficial tool that calls Apple's App Store Connect API. It can replace many clicks on Apple's websites: signing files, build uploads, TestFlight, metadata, screenshots, review submission.

Tell the user before using it: it is not made by Apple, and it holds the API key. Use a key with the lowest role that works, and set `ASC_TELEMETRY_DISABLED=1` if they do not want usage data sent.

## Install on Windows

```
winget install --id Rorkai.ASC --exact
```

Or download the Windows file from the project's GitHub releases page.

## Log in (once)

```
asc auth login --name "REPLACE_NAME" --key-id "REPLACE_KEY_ID" --issuer-id "REPLACE_ISSUER_ID" --private-key C:\path\to\AuthKey_XXXX.p8 --network
asc auth status --validate
```

In CI, or when the system keychain is not available, add `--bypass-keychain`.

## Commands shown in the project's README

```
# signing files for an app (certificate + App Store profile), creating what is missing
asc signing fetch --bundle-id REPLACE_BUNDLE_ID --profile-type IOS_APP_STORE --output .asc/signing --create-missing --create-missing-certificate

# capabilities on a bundle ID
asc bundle-ids capabilities list --bundle "REPLACE_BUNDLE_ID"

# upload a build, then confirm it arrived
asc builds upload --app "REPLACE_ASC_APP_ID" --ipa "path\to\App.ipa"
asc builds list --app "REPLACE_ASC_APP_ID" --output table

# TestFlight groups
asc testflight groups list --app "REPLACE_ASC_APP_ID" --output table

# store text kept in the repo
asc metadata init --dir "./metadata" --version "1.0.0" --locale "en-US"
asc metadata apply --app "REPLACE_ASC_APP_ID" --version "1.0.0" --dir "./metadata" --dry-run

# screenshots
asc screenshots plan --app "REPLACE_ASC_APP_ID" --version "1.0.0" --review-output-dir "./screenshots/review"
asc screenshots apply --app "REPLACE_ASC_APP_ID" --version "1.0.0" --review-output-dir "./screenshots/review" --confirm

# send a build for review
asc publish appstore --app "REPLACE_ASC_APP_ID" --ipa "path\to\App.ipa" --version "1.0.0" --submit --confirm
asc submit status --version-id "VERSION_ID"
```

## Rules for using it

- The tool changes often. Before giving any command not in the list above (creating bundle IDs, adding capabilities, registering devices, adding testers), ask the user to run `asc <command> --help` and paste the output. Do not guess flags.
- Run changing commands with `--dry-run` first where the tool offers it.
- Keep the `.asc/` folder and any downloaded signing files out of git (`.gitignore`).
- The private key of a certificate exists only where the certificate was created. If `asc` creates one, back up the files it writes.
- The first app record (the "New App" step) is still done on the App Store Connect website.

## When to use which tool

| Job | Use |
|---|---|
| Expo app | EAS does signing and upload; `asc` only for store text and review |
| Native, Flutter, bare RN on GitHub | fastlane match in the workflow; `asc` on the PC to check builds and manage TestFlight |
| Tauri iOS manual signing | `asc signing fetch` to get the certificate and profile for the secrets |
| Check that an upload really arrived | `asc builds list` |
