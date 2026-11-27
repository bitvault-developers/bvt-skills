#!/usr/bin/env python3
"""Write a privacy manifest (PrivacyInfo.xcprivacy) from simple answers.

Usage:
  python3 privacy_manifest.py --out PrivacyInfo.xcprivacy --api userdefaults,filetimestamp [options]

Options:
  --api LIST        comma list of "required reason" APIs the app's own code uses:
                      userdefaults   app settings storage          (reason CA92.1)
                      filetimestamp  reads file dates              (reason C617.1)
                      boottime       measures time since boot      (reason 35F9.1)
                      diskspace      checks free disk space        (reason E174.1)
                      keyboards      reads active keyboards        (reason 54BD.1)
  --collect LIST    comma list of data the app sends off the device, each as Type or Type:linked
                      e.g. CrashData,EmailAddress:linked,UserID:linked
                    Type is the end of Apple's name NSPrivacyCollectedDataType<Type>.
  --tracking        the app tracks users across other companies' apps or sites (rare; needs ATT)
  --expo            also print the same content as JSON for app.json > expo.ios.privacyManifests

The reason codes above are the most common one for each API. Read Apple's page
"Describing use of required reason API" and change a code if another reason fits better.
Libraries the app uses must ship their own manifest; this file covers the app's own code.
"""
import json
import plistlib
import sys

API = {
    "userdefaults": ("NSPrivacyAccessedAPICategoryUserDefaults", "CA92.1"),
    "filetimestamp": ("NSPrivacyAccessedAPICategoryFileTimestamp", "C617.1"),
    "boottime": ("NSPrivacyAccessedAPICategorySystemBootTime", "35F9.1"),
    "diskspace": ("NSPrivacyAccessedAPICategoryDiskSpace", "E174.1"),
    "keyboards": ("NSPrivacyAccessedAPICategoryActiveKeyboards", "54BD.1"),
}


def option(name):
    if name in sys.argv:
        index = sys.argv.index(name)
        if index + 1 < len(sys.argv):
            return sys.argv[index + 1]
    return None


def main():
    out = option("--out")
    if not out:
        print(__doc__)
        return 2
    apis = [item.strip().lower() for item in (option("--api") or "").split(",") if item.strip()]
    unknown = [item for item in apis if item not in API]
    if unknown:
        print("Unknown --api value: " + ", ".join(unknown))
        return 2

    collected = []
    for item in [part.strip() for part in (option("--collect") or "").split(",") if part.strip()]:
        name, _, flag = item.partition(":")
        collected.append({
            "NSPrivacyCollectedDataType": "NSPrivacyCollectedDataType" + name,
            "NSPrivacyCollectedDataTypeLinked": flag.lower() == "linked",
            "NSPrivacyCollectedDataTypeTracking": False,
            "NSPrivacyCollectedDataTypePurposes": ["NSPrivacyCollectedDataTypePurposeAppFunctionality"],
        })

    manifest = {
        "NSPrivacyTracking": "--tracking" in sys.argv,
        "NSPrivacyTrackingDomains": [],
        "NSPrivacyCollectedDataTypes": collected,
        "NSPrivacyAccessedAPITypes": [
            {"NSPrivacyAccessedAPIType": API[item][0], "NSPrivacyAccessedAPITypeReasons": [API[item][1]]}
            for item in apis
        ],
    }
    with open(out, "wb") as handle:
        plistlib.dump(manifest, handle, sort_keys=False)
    print(f"Wrote {out}")
    if manifest["NSPrivacyTracking"]:
        print("Tracking is on: list the tracking domains by hand and add the App Tracking Transparency prompt.")
    if "--expo" in sys.argv:
        print(json.dumps({"expo": {"ios": {"privacyManifests": manifest}}}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
