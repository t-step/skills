# Backlog / candidate next work

- **Add an email channel plugin** — implement `EmailChannel.send`. SMTP
  credentials and a mail-sending helper already exist in the repo (used
  today for password-reset emails), so no new external account or infra is
  needed.
- **Add an SMS channel plugin** — implement `SMSChannel.send`. No SMS
  infrastructure exists in the repo today; this would require signing up
  for a new Twilio account and provisioning credentials before any code
  could be tested against it.
- **Add a push notification channel plugin** — implement
  `PushChannel.send`. The mobile app already has a device-token
  registration flow from an earlier, unrelated slice, but no server-side
  push-sending code exists yet; this would be new code using existing
  tokens.
