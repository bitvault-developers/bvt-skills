# Connectors: letting Claude start builds and read logs

Without a connector the loop still works: the user starts the build and pastes the log. Connectors remove the copy and paste.

## Expo connector (bundled with this plugin)

Address `https://mcp.expo.dev/mcp`, sign-in with the Expo account. It is listed on the plugin's Connectors tab; the user connects it there once.

| Job | Tool |
|---|---|
| List builds, see one build | `build_list`, `build_info` |
| Read a build log | `build_logs` |
| Start a build | `build_run` (needs a GitHub repo linked to the Expo project) |
| Send a finished build to the store | `build_submit` |
| Start, check and read an EAS Workflow | `workflow_run`, `workflow_info`, `workflow_logs`, `workflow_validate` |
| Crashes and tester feedback | `testflight_crashes`, `testflight_feedback` |
| Cloud simulator and screenshots | `simulator_start`, `automation_*` (billed by Expo) |

Rules:

- Use the tools only when they are present in the session. If they are not, say the Expo connector is not connected and continue by paste.
- Ask before `build_run`, `workflow_run` and `build_submit`. They use the user's build quota or send a build to Apple.
- Ask before starting a cloud simulator. It is billed.
- Some tools need a paid Expo plan. If a tool refuses, tell the user what it said.

## GitHub

This plugin does not bundle a GitHub connector. Use whatever the session has:

- If GitHub tools that can read Actions runs and logs are present, use them to read the failed job log.
- If not, the user runs the GitHub CLI on Windows (`winget install GitHub.cli`, then `gh auth login`):

```
gh workflow run tauri-ios.yml                 # start a workflow
gh run list --limit 5                         # recent runs
gh run watch                                  # wait for the newest run
gh run view --log-failed > build-log.txt      # save only the failed steps' log
gh run download --name xcode-build-log        # get the full Xcode log artifact
gh secret set ASC_KEY_ID                      # add a secret (asks for the value, not shown)
```

The user then attaches or pastes `build-log.txt`.

## Mac-only tools (only on a rented or owned Mac)

Apple's Xcode tools for agents (`xcrun mcpbridge`) and XcodeBuildMCP run on macOS only. Mention them only when the user is working on a Mac.
