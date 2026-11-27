# BVT Apple Builder

Build iPhone, iPad and Mac apps from a Windows PC with no Mac.

Claude writes the code and the build files. A Mac in the cloud builds the app. When a build fails, Claude reads the log and gives the fix.

```
You + Claude (Windows)  ->  GitHub / Expo  ->  cloud Mac builds  ->  TestFlight  ->  iPhone / iPad
                                                                 ->  signed .dmg  ->  Mac
```

## What is inside

| Skill | What it does |
|---|---|
| `bvt-apple-builder` | Main skill. Picks the build route; holds templates, setup steps, error tables, checklists and three checking scripts |
| `apple-new` | Sets up an iPhone, iPad or Mac version of an app with all build files |
| `apple-fix` | Reads a failed build log and gives the fix |
| `apple-ship` | Release checklist for TestFlight, App Store or a Mac download |
| `apple-compliance` | Privacy manifest, encryption question, account deletion, crypto rules, review rejections |
| `apple-signing` | Certificates, profiles, API keys, renewals, the asc tool |

## Routes covered

| App made with | Built on |
|---|---|
| React Native + Expo | Expo EAS (commands or an EAS Workflow) |
| Tauri v2 (iPhone, iPad, Mac download, Mac App Store) | GitHub Actions Mac runner |
| Flutter | Codemagic, or GitHub Actions |
| React Native without Expo | GitHub Actions + fastlane |
| Native SwiftUI | GitHub Actions + XcodeGen + fastlane |
| Web app | PWA |

## Scripts

They run in Claude's code sandbox on the files Claude writes. They never contact Apple or GitHub.

- `validate.py` finds known mistakes in build files before a build is started.
- `privacy_manifest.py` writes the privacy manifest from simple answers.
- `make_icons.py` makes the 1024 px app icon with no transparency.

## Install

```text
/plugin install bvt-apple-builder --marketplace bitvault-developers/bvt-skills
```

Or, in your terminal:

```bash
claude plugin install bvt-apple-builder --marketplace bitvault-developers/bvt-skills
```

For the Claude app, download single skills as zips from the [latest release](https://github.com/bitvault-developers/bvt-skills/releases/latest) or the [`dist`](../../dist) folder and upload them where you add skills in Claude's settings.

## What you need once

1. Apple Developer Program membership (US$99 a year; Organisation account for a crypto wallet).
2. An App Store Connect API key.
3. A GitHub account, and an Expo or Codemagic account for those routes.
4. One real iPhone or iPad for testing.

The skills guide each step from a web browser.

## Connector and data

The plugin lists the Expo connector (mcp.expo.dev). Connecting it is optional. When connected, Claude can read your Expo builds and logs and, after asking, start builds, through your own Expo account. Without it, paste the log into chat. The plugin stores no keys and sends nothing anywhere by itself; keys go into GitHub Secrets, EAS or Codemagic only.

## Honest limits

- The build templates are written from the vendors' documentation and checked for syntax. They have not been run on a cloud Mac yet. Expect a few fix rounds on the first build of each route.
- Prices, free limits, tool versions and Apple's rules change. The skills tell Claude to check them before quoting.
- Some jobs still need a real Mac for a day (deep debugging, some first-time capability setup). The skills say when.
- Compliance content is build guidance, not legal advice.

## Try it

After adding the plugin, these messages should each start the right skill:

- "Set up an iPhone and iPad version of my Expo app" (apple-new)
- "Here is my failed build log" with the log pasted (apple-fix)
- "Is my wallet app ready for App Review?" (apple-compliance)
- "My distribution certificate expired" (apple-signing)
- "Send this build to TestFlight" (apple-ship)

## Changes in 0.3.0

- Mac App Store is now a ready workflow (`tauri-mas.yml`) with its config, entitlements and certificate steps from Windows.
- New guide for the first test build with an empty app, and a status file that records which routes have run green.
- New guide for widgets, watch, TV, Vision Pro and EU rules (pointers, no templates).
- Apple guideline numbers and Apple's dated upload rules checked against Apple's pages on 27 November 2026 and written into the compliance guide.
- Tauri iPhone route now names the extra Info.plist in the config.

## Changes in 0.2.0

- Upload no longer uses the deprecated `altool --upload-app`.
- GitHub action versions raised; Xcode version pinned; signing key kept in the runner's temp folder.
- Added privacy manifest, export compliance and account-deletion checks.
- New routes: EAS Workflows, Flutter on GitHub Actions, React Native without Expo, Mac App Store steps.
- New guides: compliance, capabilities, the asc tool, store listing, tests and cost, connectors.
- New skills: `apple-compliance`, `apple-signing`. New scripts. Expo connector listed.

Made by the BitVault team. MIT licence.
