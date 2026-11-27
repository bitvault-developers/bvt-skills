---
name: apple-new
description: Starts an iPhone, iPad or Mac version of an app with all files for cloud Mac building. Use when the user says new iOS app, add iOS, or make an iPhone, iPad or Mac version of an app.
metadata:
  version: "0.3.0"
---

# Start an Apple version of an app

Follow the `bvt-apple-builder` skill. This skill is the short path for "set it up".

1. Find out, from the conversation or by asking once: the framework (Expo, Tauri, Flutter, React Native, SwiftUI, web), the targets (iPhone, iPad, Mac), the app name, and the bundle ID.
2. Pick one route with the table in `bvt-apple-builder`.
3. Write every file the route needs, in full, with its path, from that skill's `templates/` folder. Replace each `REPLACE_...` value that is known. List the ones the user must fill in and where to find each.
4. Add the files every route needs: a privacy manifest and the export compliance key (`references/compliance.md`). The user chooses the export compliance answer.
5. When code execution is available, run `scripts/validate.py` on the files and fix what it reports. Make the icon set with `scripts/make_icons.py` if the user gave a picture.
6. Give the one-time setup steps that are still missing, from `references/setup-from-windows.md`, with the official link for each step.
7. Give the exact command or button that starts the first build.
8. End with a short text diagram of the path from push to iPhone, and the list of secrets to add.

If no route has had a green run yet (no `APPLE_BUILD_STATUS.md`, or all "not yet"), do `references/first-green-run.md` first.

Do not write app features in this step unless asked. The goal is a first green build of an almost empty app, so that later failures are about the code and not about signing. Say that the route is untested until that first green build.
