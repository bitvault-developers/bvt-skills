---
name: apple-fix
description: Reads a failed iPhone, iPad or Mac cloud build log and gives the fix. Use when the user pastes a build error from EAS, GitHub Actions, Codemagic, fastlane, Xcode, altool or notarization.
metadata:
  version: "0.3.0"
---

# Fix a failed Apple build

Follow `references/ci-log-triage.md` in the `bvt-apple-builder` skill.

1. Get the log. If Expo or GitHub tools are present in the session, read the failed build's log with them (`references/connectors.md`). Otherwise use what the user pasted. If it has no line with `error:`, ask for the first error and about 50 lines around it, and say where to find it (`gh run view --log-failed > build-log.txt` on Windows, or the search box in the GitHub log).
2. Match the error in the tables. Answer in this order:
   - What went wrong, in one simple sentence.
   - Why, in one sentence.
   - The fix: the full corrected file, or the exact website step with its menu path.
   - How to run the build again.
3. When the fix changes build files and code execution is available, run `scripts/validate.py` on them before handing them back.
4. Fix one cause per build. Each cloud Mac build costs minutes.
5. If the error is not in the tables, say so. Search the exact error text on the web before proposing a fix. Do not present a guess as certain.
6. If the upload step was green but no build shows in TestFlight, treat it as a failed upload (see the table).
7. After three failed builds on the same signing problem, say plainly that one day on a rented Mac may be cheaper, and point to `references/no-mac-limits.md`.

Never ask the user to paste keys, certificates or passwords.
