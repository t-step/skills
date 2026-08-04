# Accepted Slice: Add a session_cache.bulk_set() for login-batch imports

## Goal
Add a bulk_set() function to app/cache/session_cache.py that accepts a
list of (session_id, data) pairs and stores all of them, for the new
SSO batch-login flow that creates several sessions in one request.

## Why now
The SSO batch-login endpoint currently calls set() in a loop, which
works but the SSO team asked for a single bulk entry point to make
their call site simpler and to open the door to a real batched write
later if the cache moves to Redis.

## What this slice proves
That bulk_set() stores every (session_id, data) pair such that get()
returns the right data for each afterward, equivalent to calling set()
for each pair individually.

## Explicit non-goals
Does not change the underlying storage from in-memory dicts to Redis
(that's a separate, larger slice), does not change get()/invalidate().

## Acceptance evidence
A test showing bulk_set() with several pairs makes get() return the
right data for each, and that expire_stale_sessions() still correctly
expires one of the bulk-set sessions after max_age_seconds (proving
_last_touched was actually updated, not just _store).
