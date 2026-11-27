---
name: apple-ship
description: Runs the release checklist to send an iPhone, iPad or Mac app to TestFlight, the App Store or a notarized Mac download. Use when the user says ship, submit, release or TestFlight for an Apple app.
metadata:
  version: "0.3.0"
---

# Ship an Apple app

Follow `references/release-checklist.md` in the `bvt-apple-builder` skill.

1. Ask where the build should go: TestFlight (testers), App Store (public), or Mac download from a website.
2. Check the hard stops first (`references/compliance.md` section 1). If one fails, stop and say what must change before any upload. A wallet from an Individual developer account is the most common one.
3. Go through the matching parts of the checklist. Ask only about lines that cannot be seen from the project files. Run `scripts/validate.py` when code execution is available.
4. For each line that fails, give the fix: the file change in full, or the website step with its menu path and official link.
5. Give the exact command or button for the upload. Then have the user confirm the build shows in TestFlight.
6. Store text and screenshots: `references/store-listing.md`.
7. For a crypto app, also use `bvt-appstore-release` for the review rules and the review-notes text. State that licensing questions need a lawyer.
8. For a Mac download, follow `references/macos-notarize.md` and end with the `spctl` check.

Do not say the app is submitted or approved. Only the user can see that in App Store Connect.
