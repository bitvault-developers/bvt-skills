# What stays hard without a Mac, and what to do

## Hard without a Mac

| Task | Why | Way around |
|---|---|---|
| Step-by-step debugging on a real iPhone | Needs Xcode's debugger | Logs, crash reports from TestFlight, Sentry. Rent a Mac if a native crash cannot be found |
| iOS Simulator on the desk | Simulator is part of Xcode | Appetize.io / BrowserStack, or a real iPhone |
| SwiftUI Previews | Xcode only | Screenshot tests on the cloud Mac; real device |
| Instruments (speed and memory tools) | Xcode only | Rent a Mac |
| First setup of push notifications, App Groups, Keychain sharing, Associated Domains | Many small switches that must agree | Possible from the web portal + config files, but slow by trial and error. A rented Mac day can save many failed builds |
| Xcode Cloud | First workflow must be made inside Xcode | Rent a Mac for one day to set it up, or use GitHub Actions instead |
| Checking a Mac app opens cleanly | Needs macOS | Run `spctl` on the runner; ask one tester with a Mac |

## Renting a Mac

- Cloud Mac hosts have a 24-hour minimum, because of Apple's licence. The cheapest found in November 2026 was a Scaleway Mac mini at about 0.22 euro per hour, so about 5 to 6 euro for the day. AWS and others cost much more. Check prices before quoting them.
- The user connects by remote desktop and uses Xcode there.
- On a rented Mac, Claude can also use Mac-only tools: Apple's Xcode MCP (`xcrun mcpbridge`) and XcodeBuildMCP.

## When buying a Mac is cheaper

If the user rents more than about four days a month, or pays for a dedicated cloud Mac every month, a used Apple-silicon Mac mini costs less within a year and gives the Simulator, the debugger and Instruments.

## Do not use for releases

- macOS virtual machine on a PC, or a Hackintosh: against Apple's licence.
- xtool, theos, zsign, ldid, osxcross: useful for learning, not accepted routes to the App Store.
- AltStore / Sideloadly: only for the user's own test phone.
