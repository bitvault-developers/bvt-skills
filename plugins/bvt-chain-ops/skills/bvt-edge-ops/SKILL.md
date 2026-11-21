---
name: bvt-edge-ops
description: Exposes and troubleshoots BitVault public endpoints through cloudflared tunnels and nginx. Use when adding a hostname to a tunnel, creating DNS routes from the CLI, diagnosing 503 errors or dropped tunnel connections, setting CORS for browser wallets, managing TLS expiry, or deciding between tunnel access and direct localhost access from WSL2.
---

# BitVault Edge / Tunnel Operations

## cloudflared: the failure mode and the fix
Symptoms: `ERR Application error 0x0 (remote)`, `accept stream listener encountered a failure while serving`, `failed to run the datagram handler`, then `no more connections active and exiting`. Cloudflare returns 503 while the origin is healthy.

**Fix: add `protocol: http2` to `/etc/cloudflared/config.yml`.** QUIC runs over UDP and fails in this environment; HTTP/2 runs over TCP and does not.

## Restarting cloudflared
`systemctl restart` is unreliable here. Do: **`stop`, wait 5s, `start`, allow 45s.**
Verify by **counting `Registered tunnel connection` in the journal — expect 4.** `systemctl is-active` reports active even when every connection has dropped, so it is not a health check.

## Adding a hostname (no dashboard needed)
1. Add to `/etc/cloudflared/config.yml`:
   ```yaml
   - hostname: <name>.<your-domain>
     service: http://127.0.0.1:8080
   ```
2. `cloudflared tunnel route dns <tunnel-id> <name>.<your-domain>` — creates the CNAME from the CLI.
3. stop / wait / start.
4. Back up the config first: `~/cloudflared-config.backup-<date>`.

## WSL2 caveat
If the host is WSL2 on a Windows machine, the virtual NIC renegotiates on network change, sleep and WSL restart — so cloudflared loses connections **regardless of transport**, and the service goes down whenever Windows sleeps or reboots. `protocol: http2` reduces this; it does not eliminate it. For anything holding real value this is a migration-to-real-hosting question, not a tuning question.

**Practical shortcut:** WSL2 forwards localhost to Windows. For personal use, hit `http://localhost:<port>` directly and point wallets at `http://localhost:8546`. Cloudflare leaves the path entirely.

## CORS and TLS
- Browser wallets need permissive CORS on the RPC (`--rpc-http-cors-origins=all` on a private chain).
- Track TLS expiry explicitly; a tunnel cert expiring looks identical to a tunnel outage.

## Diagnosing "the site is broken"
Both BitVault front-ends are JS SPAs, so **grepping `index.html` finds nothing** — search the built asset (`bundle.js` / `/assets/index-*.js`) instead. Also confirm which host actually serves the domain: a site on Cloudflare Pages never reaches the nginx vhost, so a stale local build can look live when it is not.
