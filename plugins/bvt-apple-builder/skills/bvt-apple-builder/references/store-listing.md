# Store listing: screenshots and text without a Mac

## Screenshot sizes

App Store Connect names the sizes it needs on the upload page; check there first. Collected in November 2026:

| Device | Pixels (portrait) | Needed |
|---|---|---|
| iPhone 6.9 inch | 1320 x 2868 (1290 x 2796 and 1260 x 2736 also accepted) | Yes |
| iPhone 6.5 inch | 1284 x 2778 or 1242 x 2688 | Only if no 6.9 inch set is given |
| iPad 13 inch | 2064 x 2752 or 2048 x 2732 | Only if the app runs on iPad |

One to ten screenshots per set. They must show the real app.

## Ways to get screenshots with no Mac

1. Real iPhone or iPad: take screenshots from the TestFlight build. Simplest and always accepted when the device has the needed size.
2. Cloud simulator: the Expo connector's simulator tools can start a simulator and take screenshots (Expo bills this). Appetize.io and BrowserStack also show the app in a browser.
3. Cloud Mac job: Maestro or fastlane `snapshot` on a GitHub Mac runner, saved as an artifact. Costs Mac minutes; run it only for releases.
4. Design tool: place real screenshots into frames at the exact pixel size (Figma, Canva).

## Store text kept in the repo

Keeping the text in files lets Claude edit and translate it.

| Route | Tool |
|---|---|
| Expo | EAS Metadata: `store.config.json`, then `eas metadata:push` |
| Any | `asc metadata init` and `asc metadata apply` (`asc-route.md`) |
| fastlane users | `deliver` with a `fastlane/metadata` folder |

Fields to prepare: app name (30 characters), subtitle (30), promotional text (170), description, keywords (100 characters, comma separated), support URL, privacy policy URL, "What's New" text, review notes.

For translated listings use the `bvt-store-listing-i18n` skill when installed.
