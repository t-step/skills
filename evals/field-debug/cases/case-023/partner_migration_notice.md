# Fulfillco Partner Notice: Auth Migration (sent 2 weeks ago)

**Effective Sept 22, 00:00 UTC: legacy API-key authentication is
retired.**

All requests to the order-ingestion endpoint must be signed:

1. Compute a SHA-256 hash of your request payload.
2. Sign that hash with your account's HMAC signing secret using
   HMAC-SHA256.
3. Send the signature in the `X-Fulfillco-Signature` header, and the
   payload hash you signed in `X-Fulfillco-Payload-Hash`.

Your account's signing secret (rotated as part of this migration):

```
fc_live_secret_7f3a9c2e
```

Requests still using the old `Authorization: Bearer <api-key>` header
will be rejected with `401 Unauthorized` starting at cutover. This
migration only concerns authentication -- it does not affect the request
or response payload format.

-- Fulfillco Partner Integrations
