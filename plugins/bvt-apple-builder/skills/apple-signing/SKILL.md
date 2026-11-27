---
name: apple-signing
description: Sets up and renews Apple signing with no Mac. Use for certificates, provisioning profiles, App Store Connect API keys, fastlane match, the asc tool, capabilities, expired certificates or a leaked key.
metadata:
  version: "0.3.0"
---

# Apple signing without a Mac

Words, said once to the user:

- Certificate = proof of who built the app.
- Provisioning profile = a file that ties the app's bundle ID, the certificate and the allowed features together.
- API key = lets build tools talk to Apple without a password.

Files to follow in the `bvt-apple-builder` skill:

| Job | File |
|---|---|
| First setup from Windows (API key, secrets, match repo, Developer ID `.p12`) | `references/setup-from-windows.md` |
| Doing it from the command line with `asc` | `references/asc-route.md` |
| Adding push, universal links, Sign in with Apple | `references/capabilities.md` |
| Yearly renewals, leaked secrets | `references/quality-and-cost.md` |
| A signing error in a build log | `references/ci-log-triage.md` |

Which tool signs on each route:

| Route | Who makes and keeps the signing files |
|---|---|
| Expo | EAS (`eas credentials`) |
| Native SwiftUI, Flutter on GitHub, bare React Native | fastlane match, lane `certs` |
| Tauri iPhone/iPad | Xcode automatic signing through the API key; manual files as the fallback |
| Tauri Mac download | Developer ID `.p12` made with OpenSSL on Windows |
| Flutter on Codemagic | Codemagic, through its App Store Connect integration |

Rules:

- Never ask for a key, certificate, password or token in chat. If one is pasted, tell the user to revoke it now and make a new one.
- Keep signing files out of the repo. Run `scripts/validate.py` to catch them.
- After any change to an App ID's capabilities, make the profile again.
- For `asc` commands not listed in `references/asc-route.md`, ask the user to run the command with `--help` and paste the output. Do not guess flags.
- After three failed builds on the same signing problem, say that one rented Mac day may be cheaper (`references/no-mac-limits.md`).
