---
name: apple-compliance
description: Checks an iPhone, iPad or Mac app against Apple's upload and review rules. Use for privacy manifest, export compliance, account deletion, crypto rules or an App Review rejection.
metadata:
  version: "0.3.0"
---

# Apple compliance check

Follow `references/compliance.md` in the `bvt-apple-builder` skill.

1. Ask what the app does in one line, which account type the developer has (Individual or Organisation), and whether users create an account in the app.
2. Go through the hard stops in section 1. Name each one that fails and the fix. For a wallet from an Individual account, stop here and say the account must change first.
3. Privacy manifest: ask which data leaves the device and which of the listed system functions the app's own code uses. Make the file with `scripts/privacy_manifest.py` when code execution is available; otherwise write it by hand from the template.
4. Export compliance: show the decision tree. Ask which crypto code the app uses and for what. The user chooses the answer. Then write the key in the right place for the route.
5. For a rejection: ask for Apple's full message, find the guideline in the "App Review rejections" table in `references/ci-log-triage.md`, give the fix and a short, polite reply for the Resolution Center.

Rules:

- Do not decide legal questions (licences, export reports, tax). Say they need a lawyer or adviser.
- Guideline numbers and wording change. Before a first submission, have the user open the App Review Guidelines page and check the sections named.
- For crypto review notes and policy detail, use `bvt-appstore-release` when installed.
