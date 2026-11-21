---
name: bvt-push-privacy
description: Implements transaction, price and order push notifications for crypto apps without leaking wallet addresses or balances to the push infrastructure. Use when adding notifications for incoming transfers, price alerts or order fills, when designing the notification backend, or when handling notification payloads on device.
---

# Push Notifications Without Leaking Addresses

## The threat
A conventional push backend maps `device_token → wallet_address` and receives every balance change. That server becomes a deanonymizing database of who owns which address, and APNs/FCM see the payloads. For a wallet this is a privacy failure even when nothing is stolen.

## Approaches, strongest first
1. **On-device watching (best privacy).** The app subscribes to chain events itself while foregrounded and uses local notifications. Costs: no background delivery guarantee, battery.
2. **Blinded topics.** The device subscribes to a topic derived as `HMAC(server_salt_epoch, address)` truncated. The server publishes to topic hashes without a reverse mapping. Rotate the epoch periodically. Some correlation risk remains via subscription timing.
3. **Silent push + local fetch.** Server sends a **contentless** wake-up; the device fetches details itself and raises the local notification. The server learns *that* something happened, not what — and the payload holds no address or amount.
4. **Plain address→token mapping.** Only acceptable for the custodial products (an exchange or a crypto bank) where the server already knows the account. Never for the non-custodial wallet.

## Payload rules
- **Never** put an address, amount, balance, token symbol tied to an account, or transaction hash in a push payload.
- Notification body is generic until the device decrypts or fetches: "Activity in your wallet", then the local notification carries detail.
- If a payload must carry data, encrypt it to a device key and decrypt in a notification service extension (iOS) / `FirebaseMessagingService` (Android).

## Implementation
- `expo-notifications` for permissions/handling; APNs and FCM under it.
- Ask for permission **in context** (after the user enables an alert), not on first launch — a wallet that prompts immediately gets denied.
- Deep link from a notification goes to a **read-only** screen. A notification must never trigger a signing action directly (see `bvt-deeplinks-walletconnect`).
- Respect the lock: notification content is suppressed on the lock screen for account-specific alerts.

## Price alerts
Price alerts are not account-specific — subscribe to a public topic per pair. Do not bundle them with account events, or the subscription set leaks holdings.
