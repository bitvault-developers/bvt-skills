# Tests, crashes, versions, renewals and cost

## Tests on the cloud Mac

| Kind | How |
|---|---|
| Unit tests, native | `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=<a simulator on the runner>'`. List them first with `xcrun simctl list devices available` |
| UI flows, any framework | Maestro: flows are small YAML files. EAS Workflows has a `maestro` job (marked alpha by Expo); on GitHub, install Maestro and run `maestro test` against a simulator build |
| JS tests, lint, type checks | Run on a Linux runner, never on a Mac runner. Linux minutes cost about a tenth |

Keep Mac jobs for the release build. Put everything else on Linux.

## Crashes

- TestFlight collects crashes and tester feedback: App Store Connect > TestFlight. The Expo connector can read them (`testflight_crashes`, `testflight_feedback`).
- Sentry or Firebase Crashlytics for live apps. Symbol files (dSYM) must be uploaded for readable crash reports: the Sentry Expo plugin does it during EAS builds; elsewhere add `sentry-cli debug-files upload` after the build step.
- For a wallet, strip addresses, balances and keys from crash data (`bvt-app-observability`).

## Versions

- Version (for example `1.2.0`): chosen by the user, shown in the store. Raise it for every App Store release.
- Build number: must be higher for every upload of the same version. Templates use the GitHub run number; Expo uses `appVersionSource: remote` with `autoIncrement`.
- Moving an app from one build system to another: the new build numbers must still be higher than the old ones. Set a starting offset if needed.

## Yearly renewals

| Item | Lifetime | What to do |
|---|---|---|
| Apple Developer Program | 1 year | Renew before it ends, or the apps leave the store |
| Distribution certificate + profiles | 1 year | Native, Flutter, bare RN: run lane `certs` again. Expo: EAS offers to make a new one. Installed apps keep working |
| Developer ID certificate (Mac download) | 5 years | Make a new one before it ends; already notarized apps keep working |
| APNs key, App Store Connect API key | No expiry | Rotate if leaked: make a new key, update the secrets, revoke the old one |
| TestFlight build | 90 days | Upload a new build |
| GitHub token for the match repo | As set when created | Make a new token, update `MATCH_GIT_BASIC_AUTHORIZATION` |

If a secret leaked (pasted in chat, pushed to a repo, printed in a log): revoke it at Apple or GitHub first, then replace it. Deleting the message is not enough.

## Cost guard for GitHub Mac minutes

- Start Mac workflows by hand or on tags only. Never on every push.
- `timeout-minutes` on every Mac job.
- `concurrency` so two builds of the same app do not run together.
- Caches: Rust (`Swatinem/rust-cache`), npm (`setup-node` cache), Swift packages and pods (`actions/cache`).
- Fix one cause per build; run `scripts/validate.py` before starting a build.
- A public repo gets free minutes, but never make a wallet's repo public to save money.
- Check GitHub's billing page for the current free allowance and per-minute price.
