#!/usr/bin/env python3
"""Check Apple build files for known problems before a cloud Mac build is started.

Usage:  python3 validate.py <project folder>

It reads text files only. It never contacts Apple or GitHub. It finds:
  STOP  = will break the build, the upload or App Review, or leaks a secret
  FIX   = should be changed before the first real release
  NOTE  = worth a look
Exit code is 1 when a STOP is found, else 0.
"""
import json
import os
import plistlib
import re
import sys

try:
    import yaml  # optional
except Exception:  # pragma: no cover
    yaml = None

SKIP_DIRS = {".git", "node_modules", "Pods", "build", "target", "dist", ".dart_tool", "DerivedData", ".expo"}
OLD_ACTIONS = {
    "actions/checkout": 6,
    "actions/setup-node": 6,
    "actions/upload-artifact": 6,
    "actions/download-artifact": 6,
    "actions/cache": 5,
}
BUNDLE_ID_RE = re.compile(r"^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$")
SECRET_FILE_RE = re.compile(r"(\.p8|\.p12|\.mobileprovision|\.provisionprofile|\.keystore|\.jks)$", re.I)

findings = []


def add(level, path, message):
    findings.append((level, path, message))


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def walk(root):
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            yield os.path.join(folder, name)


def check_workflow(path, text):
    if yaml is not None:
        try:
            yaml.safe_load(text)
        except Exception as error:
            add("STOP", path, f"YAML does not parse: {str(error).splitlines()[0]}")
    for action, minimum in OLD_ACTIONS.items():
        for match in re.finditer(re.escape(action) + r"@v(\d+)", text):
            if int(match.group(1)) < minimum:
                add("FIX", path, f"{action}@v{match.group(1)} runs on an old Node version; use v{minimum} or newer")
    if "--upload-app" in text:
        add("STOP", path, "altool --upload-app is deprecated; use --upload-package with --apple-id, or fastlane upload_to_testflight")
    if re.search(r"xcode-version:\s*['\"]?latest", text):
        add("FIX", path, "Xcode is not pinned (latest/latest-stable); write an exact version such as \"26.6\"")
    if "macos-" in text and "setup-xcode" not in text and "xcode-select" not in text and "tauri-action" not in text:
        add("NOTE", path, "No Xcode version is chosen; the runner's default Xcode changes over time")
    if re.search(r"runs-on:\s*macos-(1[0-9]|latest)\b", text):
        add("FIX", path, "Old or moving macOS image; name a current one such as macos-26")
    if "macos-" in text and "timeout-minutes" not in text:
        add("FIX", path, "No timeout-minutes; a stuck Mac build keeps costing minutes")
    if re.search(r"on:\s*\n\s*push:\s*\n(?!\s*(tags|branches|paths))", text) or re.search(r"^on:\s*\[?\s*push\s*\]?\s*$", text, re.M):
        add("FIX", path, "Builds on every push; start Mac builds by hand or on tags to save minutes")
    if re.search(r"upload-artifact[\s\S]{0,200}(RUNNER_TEMP|private_keys|\.p8)", text):
        add("STOP", path, "An artifact step may upload the key folder; never upload keys")


def check_secrets(path, text):
    if "BEGIN PRIVATE KEY" in text or "BEGIN RSA PRIVATE KEY" in text or "BEGIN EC PRIVATE KEY" in text:
        add("STOP", path, "A private key is inside this file; remove it, revoke the key, use CI secrets")
    if re.search(r"gh[pousr]_[A-Za-z0-9]{30,}", text):
        add("STOP", path, "A GitHub token is inside this file; revoke it and use CI secrets")


def bundle_id_ok(value, path, where):
    if "REPLACE_" in value:
        return
    if not BUNDLE_ID_RE.match(value):
        add("STOP", path, f"{where} '{value}' is not a valid bundle ID (letters, digits, hyphens and dots only)")


def check_expo(path, text, state):
    try:
        data = json.loads(text)
    except Exception as error:
        add("STOP", path, f"JSON does not parse: {error}")
        return
    expo = data.get("expo", data)
    ios = expo.get("ios") or {}
    state["expo"] = True
    if not ios.get("bundleIdentifier"):
        add("STOP", path, "expo.ios.bundleIdentifier is missing")
    else:
        bundle_id_ok(ios["bundleIdentifier"], path, "expo.ios.bundleIdentifier")
    uses = (ios.get("config") or {}).get("usesNonExemptEncryption")
    plist_key = (ios.get("infoPlist") or {}).get("ITSAppUsesNonExemptEncryption")
    if uses is None and plist_key is None:
        add("FIX", path, "Export compliance answer missing: set expo.ios.config.usesNonExemptEncryption (see references/compliance.md)")
    else:
        state["export_key"] = True
    if not ios.get("privacyManifests"):
        add("FIX", path, "expo.ios.privacyManifests is missing (privacy manifest)")
    else:
        state["privacy"] = True
    if ios.get("supportsTablet") is None:
        add("NOTE", path, "expo.ios.supportsTablet is not set; set true for a real iPad app")


def check_eas(path, text):
    try:
        data = json.loads(text)
    except Exception as error:
        add("STOP", path, f"JSON does not parse: {error}")
        return
    build = data.get("build") or {}
    if "production" not in build:
        add("FIX", path, "No build.production profile")
    for name, profile in build.items():
        if (profile.get("ios") or {}).get("image") == "latest":
            add("NOTE", path, f"build.{name}.ios.image is 'latest'; it can change under you")
    submit_ios = ((data.get("submit") or {}).get("production") or {}).get("ios") or {}
    if not submit_ios.get("ascAppId"):
        add("NOTE", path, "submit.production.ios.ascAppId is not set; eas submit will ask for it")


def check_tauri(path, text, state):
    try:
        data = json.loads(text)
    except Exception as error:
        add("STOP", path, f"JSON does not parse: {error}")
        return
    state["tauri"] = True
    identifier = data.get("identifier")
    if not identifier:
        add("STOP", path, "identifier (bundle ID) is missing")
    else:
        bundle_id_ok(identifier, path, "identifier")
        if identifier.endswith(".app"):
            add("FIX", path, "identifier ends with .app; this clashes with the Mac app bundle extension")
    if not data.get("version"):
        add("NOTE", path, "version is not set here; the upload step falls back to package.json")
    ios = (data.get("bundle") or {}).get("iOS") or {}
    if not ios.get("developmentTeam"):
        add("NOTE", path, "bundle.iOS.developmentTeam is not set; the workflow must pass APPLE_DEVELOPMENT_TEAM")


def check_xcodegen(path, text, state):
    state["native"] = True
    for match in re.finditer(r"PRODUCT_BUNDLE_IDENTIFIER:\s*['\"]?([^\s'\"]+)", text):
        bundle_id_ok(match.group(1), path, "PRODUCT_BUNDLE_IDENTIFIER")
    if "ITSAppUsesNonExemptEncryption" in text:
        state["export_key"] = True
    if "PrivacyInfo.xcprivacy" in text:
        state["privacy"] = True
    if "scheme:" not in text and "schemes:" not in text:
        add("FIX", path, "No shared scheme; add `scheme: {}` to the target so fastlane can find it")


def check_plist(path, state):
    try:
        with open(path, "rb") as handle:
            data = plistlib.load(handle)
    except Exception as error:
        add("STOP", path, f"plist does not parse: {str(error)[:120]}")
        return
    name = os.path.basename(path)
    if name.endswith(".xcprivacy"):
        state["privacy"] = True
        for key in ("NSPrivacyTracking", "NSPrivacyCollectedDataTypes", "NSPrivacyAccessedAPITypes"):
            if key not in data:
                add("FIX", path, f"{key} is missing from the privacy manifest")
        for entry in data.get("NSPrivacyAccessedAPITypes", []):
            if not entry.get("NSPrivacyAccessedAPITypeReasons"):
                add("STOP", path, f"{entry.get('NSPrivacyAccessedAPIType')} has no reason code")
    if isinstance(data, dict) and "ITSAppUsesNonExemptEncryption" in data:
        state["export_key"] = True


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print(__doc__)
        return 2
    root = sys.argv[1]
    state = {"expo": False, "tauri": False, "native": False, "export_key": False, "privacy": False}
    checked = 0
    for path in walk(root):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        name = os.path.basename(path)
        if SECRET_FILE_RE.search(name):
            add("STOP", rel, "Signing file inside the project folder; keep keys and certificates out of the repo")
            continue
        if os.path.getsize(path) > 2_000_000:
            continue
        lower = name.lower()
        is_workflow = "/workflows/" in "/" + rel and lower.endswith((".yml", ".yaml"))
        interesting = (
            is_workflow
            or lower in {"eas.json", "app.json", "tauri.conf.json", "project.yml", "codemagic.yaml", "fastfile",
                         "matchfile", "appfile", "gemfile", "apple-app-site-association"}
            or lower.endswith((".plist", ".xcprivacy", ".entitlements"))
        )
        if not interesting:
            continue
        checked += 1
        text = read(path)
        check_secrets(rel, text)
        if "REPLACE_" in text:
            names = sorted(set(re.findall(r"REPLACE_[A-Za-z0-9_]+", text)))
            add("STOP", rel, "Placeholders not filled in: " + ", ".join(names))
        if is_workflow or lower == "codemagic.yaml":
            check_workflow(rel, text)
        elif lower == "app.json":
            check_expo(rel, text, state)
        elif lower == "eas.json":
            check_eas(rel, text)
        elif lower == "tauri.conf.json":
            check_tauri(rel, text, state)
        elif lower == "project.yml":
            check_xcodegen(rel, text, state)
        elif lower == "fastfile":
            if "upload_to_testflight" in text and "apple_id" not in text:
                add("FIX", rel, "upload_to_testflight has no apple_id; pass the numeric app ID so the build lands on the right app")
            if "build_app" in text and "setup_ci" not in text:
                add("STOP", rel, "setup_ci is missing; signing will hang on the runner")
        elif lower.endswith((".plist", ".xcprivacy", ".entitlements")) and "REPLACE_" not in text:
            check_plist(path, state)

    if state["tauri"] or state["native"]:
        if not state["export_key"]:
            add("FIX", ".", "No export compliance answer found (ITSAppUsesNonExemptEncryption); builds will wait at 'Missing Compliance'")
        if not state["privacy"]:
            add("FIX", ".", "No privacy manifest found (PrivacyInfo.xcprivacy or expo.ios.privacyManifests)")

    order = {"STOP": 0, "FIX": 1, "NOTE": 2}
    findings.sort(key=lambda item: (order[item[0]], item[1]))
    print(f"Checked {checked} build files in {root}")
    if not findings:
        print("No known problems found. This does not prove the build will pass; only a real cloud build does.")
        return 0
    for level, path, message in findings:
        print(f"[{level}] {path}: {message}")
    counts = {level: sum(1 for item in findings if item[0] == level) for level in order}
    print(f"STOP {counts['STOP']}  FIX {counts['FIX']}  NOTE {counts['NOTE']}")
    return 1 if counts["STOP"] else 0


if __name__ == "__main__":
    sys.exit(main())
