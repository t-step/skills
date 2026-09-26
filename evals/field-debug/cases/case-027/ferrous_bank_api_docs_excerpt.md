# Ferrous Bank Gateway API -- Batch Submission (excerpt)

**POST /v1/ach/batches**

Accepts a NACHA-formatted batch file. On success, returns
`{"confirmation_id": "...", "status": "queued"}`.

**Idempotency.** Callers may optionally supply an `Idempotency-Key` header.
When present, a retried POST with the same key and identical body returns
the original `confirmation_id` without creating a second batch. **When
absent, every POST to this endpoint is treated as a new, independent batch
submission, even if the file content is identical to a prior submission.**

**Checking batch status.** Once submitted, a batch's processing status
(received / validated / settled / rejected) can be checked two ways:

- The Ferrous Merchant Portal (`portal.ferrousbank.example`), which shows
  real-time status per batch ID. Access requires a Ferrous-issued
  hardware token, provisioned per merchant account to designated Treasury
  contacts only.
- The settlement webhook, which Ferrous calls back to the merchant's
  registered URL once a batch settles -- typically **T+1 business day**,
  not real-time.

There is no other way to query batch status from outside Ferrous's
systems.
