# Feature Specification: Idempotent Webhook Event Recorder

**Status**: Draft

**Input**: "Our one external payment processor sometimes delivers the same
webhook event more than once (their own retry behavior, not ours). We need
to record each event exactly once no matter how many times it's delivered,
and never lose one."

## User Scenarios & Testing

### User Story 1 - Record an event exactly once regardless of delivery count (Priority: P1)

An external service delivers a webhook event, possibly more than once
(network retry on their side, a duplicate send). The system must persist
it exactly once and always tell the caller unambiguously what happened.

**Acceptance Scenarios**:

1. **Given** no event with a given `event_id` has been recorded yet,
   **When** a webhook delivery for that `event_id` arrives, **Then** the
   event is recorded with status `recorded`, and the response indicates
   this was the first recording.
2. **Given** an event with a given `event_id` has already been recorded,
   **When** another delivery for the same `event_id` arrives (with
   identical or different payload bytes), **Then** no second record is
   created, the original recorded payload is left unchanged, and the
   response indicates this was a duplicate of an already-recorded event.
3. **Given** two deliveries for the same, not-yet-recorded `event_id`
   arrive at the same instant, **When** both are processed concurrently,
   **Then** exactly one is recorded as the original and the other receives
   an immediate, unambiguous "already recorded" response -- never two
   original records for the same `event_id`, and never a window in which
   both could observe no record and both proceed to insert.
4. **Given** a delivery whose signature does not validate, **When** it is
   received, **Then** it is rejected before any record is created or
   inspected, and rejection never consumes or reserves the `event_id` --
   a later delivery of the same `event_id` with a valid signature is
   recorded normally as if the rejected attempt never happened.

### Edge Cases

- What happens if the recording write succeeds but the process crashes
  before responding to the caller? The caller's retry (same `event_id`)
  is handled by Acceptance Scenario 2 exactly as any other duplicate
  delivery -- the system cannot distinguish "caller never got a response"
  from "an unrelated duplicate delivery," and does not need to: both
  produce the same, correct, idempotent outcome.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST reject any delivery whose signature does not
  validate, before creating, reserving, or inspecting any record for its
  `event_id` (FR-001 makes signature validation happen strictly before any
  `event_id`-keyed operation).
- **FR-002**: The system MUST persist, for each `event_id` it accepts, a
  single record containing the `event_id`, the payload bytes as received,
  and a `recorded_at` timestamp.
- **FR-003**: `event_id` MUST be enforced as unique across all recorded
  events by a database-level uniqueness constraint -- never by a
  read-then-write check in application code -- so that concurrent
  recording attempts for the same `event_id` (Acceptance Scenario 3) are
  arbitrated by the database itself: exactly one insert succeeds, every
  other concurrent insert for the same `event_id` fails immediately with a
  constraint violation and is reported to its caller as a duplicate.
- **FR-004**: A rejected delivery (FR-001) MUST NOT create, lock, or
  reserve any row keyed by its `event_id` -- rejection and recording share
  no state, so a later valid delivery of the same `event_id` is recorded
  exactly as if no prior delivery had ever been attempted.
- **FR-005**: A recorded event's payload and `recorded_at` timestamp MUST
  NOT be modified by any later delivery of the same `event_id`, regardless
  of whether the later delivery's payload bytes differ from the original.
- **FR-006**: The system's response to every delivery MUST distinguish
  exactly three outcomes: rejected (FR-001), recorded-original (first
  successful recording), or recorded-duplicate (any later delivery of an
  already-recorded `event_id`) -- callers MUST be able to tell these apart
  from the response alone.

### Key Entities

- **Recorded Event**: One durably persisted record per unique `event_id`,
  created exactly once by whichever delivery's insert wins the database's
  uniqueness constraint (FR-003), never modified after creation (FR-005).

## Success Criteria

- **SC-001**: In repeated trials sending N >= 2 concurrent deliveries for
  the same, previously-unseen `event_id`, exactly one is ever recorded as
  original and N-1 are reported as duplicates, in 100% of trials.
- **SC-002**: A recorded event's payload is bit-for-bit identical to the
  payload of whichever delivery was recorded as original, regardless of
  how many later duplicate deliveries (with the same or different payload
  bytes) arrive afterward.
- **SC-003**: An invalid-signature delivery followed immediately by a
  valid-signature delivery for the same `event_id` always results in the
  valid delivery being recorded as original, never as a duplicate.

## Assumptions

- This recorder is integrated with exactly one external event source (the
  payment processor named above) for its operational lifetime; `event_id`
  is that single source's own identifier namespace, so a database-level
  uniqueness constraint on the bare `event_id` value (FR-003) is safe.
  Integrating a second, independent external source with its own
  `event_id` namespace is out of scope and would require revisiting FR-003
  as a separate, later specification.
- Signature validation itself (the cryptographic scheme, key rotation) is
  provided by an existing shared library and is out of scope here; this
  specification only constrains when validation happens relative to
  recording (FR-001).
- `event_id` values are generated by the external service and are assumed
  unique per genuinely distinct event on the sender's side; this
  specification's uniqueness guarantee (FR-003) is what makes the system
  robust to the sender's own retries, not a defense against the sender
  reusing an `event_id` for two genuinely different events -- that
  scenario is out of scope.
