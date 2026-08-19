Everything you need is under `repo/` in this case directory.

Task: we have two retry helpers that look duplicated —
`repo/core/retry.py`'s `with_retry` and
`repo/integrations/retry_utils.py`'s `call_with_retry`. Please unify them
into a single shared retry helper and update both call sites
(`repo/batch/nightly_sync.py` and `repo/payments/charge.py`) to use it.
Can you orient me on anything I should know before I do this?
