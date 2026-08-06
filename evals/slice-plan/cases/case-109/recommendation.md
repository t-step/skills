# Accepted Slice: Require actor_id on every audit event

## Goal
record_event() should accept and store a required actor_id alongside
event_type and payload, and every existing call site in the codebase
must be updated to pass one -- for handlers.py's create_order(), that's
the authenticated user_id; for scheduled/system jobs, that's the
literal string "system".

## Why now
Compliance flagged that the attribution report (built from the audit
log) can't currently tell who or what triggered an event -- every
existing audit entry is missing that field, and new entries need to
start carrying it immediately.

## What this slice proves
That record_event() requires and stores actor_id, that every existing
call site in the codebase passes an appropriate one, and that no code
path writes an audit event without one after this slice ships.

## Explicit non-goals
Does not backfill actor_id onto already-written historical entries,
does not change the attribution report itself, does not add new event
types.

## Acceptance evidence
A test showing record_event() requires actor_id, and that every
existing call site's audit entries now include the correct actor_id
value.
