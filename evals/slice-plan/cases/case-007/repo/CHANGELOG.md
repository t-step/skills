# Changelog

## v2.3.0
- Rate-limit `request_password_reset()` to 5 requests per email per
  hour; the 6th+ request within the window now returns 429 with the
  same generic message a successful request returns, closing the
  enumeration gap security review flagged. (commit 7f3a91c)

## v2.2.0
- Add `send_reset_email()` delivery retry on transient SMTP errors.
  (commit c184e0a)

## v2.1.0
- Initial password-reset flow: `request_password_reset()` and
  `send_reset_email()`. (commit 4b7d2f1)
