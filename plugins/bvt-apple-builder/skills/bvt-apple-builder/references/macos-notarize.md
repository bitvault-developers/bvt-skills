# Mac apps: sign, notarize, staple

Words:

- Sign = put the developer's digital stamp on the app.
- Notarize = send the app to Apple's automatic malware check. Without it macOS blocks the app.
- Staple = attach Apple's "passed" ticket to the file so it opens even offline.

## Normal way: do it on the cloud Mac during the build

`templates/tauri-macos.yml` does all three. The Tauri bundler signs with `APPLE_CERTIFICATE` and `APPLE_SIGNING_IDENTITY`, then notarizes with `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH`. Nothing else is needed.

The app itself must still be compiled on macOS. Signing tools do not change that.

## Other way: rcodesign on Windows or Linux

rcodesign is an open-source tool (apple-codesign project) that signs and notarizes Apple files on any system. Use it when a `.app` or `.dmg` was built in CI without signing and the user wants to sign it later, or to check on a notarization from the PC.

Install: download a release from the `indygreg/apple-platform-rs` GitHub releases page, or `cargo install apple-codesign`.

```bash
# 1. one time: pack the API key into one JSON file
rcodesign encode-app-store-connect-api-key -o asc-key.json ISSUER_ID KEY_ID AuthKey_KEYID.p8

# 2. sign for notarization with the Developer ID certificate
rcodesign sign --for-notarization --p12-file developer_id.p12 --p12-password-file p12-password.txt MyApp.app

# 3. upload to Apple, wait, and staple
rcodesign notary-submit --api-key-file asc-key.json --staple MyApp.app

# check and debug
rcodesign notary-list --api-key-file asc-key.json
rcodesign notary-log  --api-key-file asc-key.json SUBMISSION_ID
```

Flags differ a little between versions. Run `rcodesign sign --help` and `rcodesign notary-submit --help` on the installed version before giving final commands. `--for-notarization` exists only in newer versions; on older ones use `--code-signature-flags runtime`.

A `.dmg` is signed and notarized the same way as a `.app`: sign the `.app`, put it in the `.dmg`, sign the `.dmg`, then `notary-submit --staple` the `.dmg`.

There is also a GitHub Action, `indygreg/apple-code-sign-action`, that runs rcodesign on cheap Linux runners.

## Check

On a Mac (the cloud runner is fine): `spctl -a -vv MyApp.app` and `xcrun stapler validate MyApp.dmg`.
