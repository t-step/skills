# Tasks: Admin Endpoint Signing

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add `verify_signed_request(req)` in `auth/hmac_verifier.py` --
  validates the `X-Signature` header via HMAC-SHA256 against the shared
  admin signing secret, raising `Unauthorized` on a missing or mismatched
  signature.
- T2: Add `POST /admin/purge-cache` in `api/admin_cache.py`, calling
  `verify_signed_request` before purging the cache.
- T3: Add `POST /admin/reindex` in `api/admin_search.py`, calling
  `verify_signed_request` before triggering a reindex.
- T4: Add `POST /admin/rotate-keys` in `api/admin_keys.py`, calling
  `verify_signed_request` before rotating signing keys.
- T5: Add test `tests/test_admin_cache.py` for T2 (valid signature
  purges; missing/invalid signature is rejected and nothing is purged).
- T6: Add test `tests/test_admin_search.py` for T3 (same shape as T5,
  for reindex).
- T7: Add test `tests/test_admin_keys.py` for T4 (same shape as T5, for
  key rotation).

All three admin endpoints (T2, T3, T4) call `verify_signed_request`
before doing anything else. If the HMAC check were implemented
separately inside each of `api/admin_cache.py`, `api/admin_search.py`,
and `api/admin_keys.py` instead of once in `auth/hmac_verifier.py`, the
signature-checking logic would exist in three places, and any future
change to the signing scheme (e.g. rotating to a new HMAC key format)
would require editing all three independently rather than one shared
function. No priority is stated between the three admin endpoints, and
none of them shares a file with either of the other two.
