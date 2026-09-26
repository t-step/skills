# Runbook: ACH export timeout (last updated 8 months ago)

> **ACH export job timed out / connection reset?** Just re-run
> `ach_batch_export.py` manually from the on-call laptop -- it's safe,
> Ferrous dedupes batches on their end so a duplicate submission is a
> no-op.

This entry has not been touched since it was written. It does not mention
`Idempotency-Key`, and it predates the current `bank_gateway_client.py`
(git blame: rewritten 5 months ago to move off the old SFTP-based
submission path onto the current HTTP gateway).
