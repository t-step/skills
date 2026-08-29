# Feature Specification: Task Completion Notification

**Status**: Draft

**Input**: "When an agent finishes a tracked task, the system should record
it as done and let the external project board know, so the board stays
current without anyone updating it by hand."

## User Scenarios & Testing

### User Story 1 - Mark a task done and reflect it on the board (Priority: P1)

An agent finishes a task it owns and marks it complete. The task's local
record and the external project board should both end up showing the task
as done.

**Acceptance Scenarios**:

1. **Given** a task in `in_progress` status owned by the calling agent,
   **When** the agent marks it done, **Then** the task's local status
   becomes `done` and the external project board's card for that task shows
   `Done`.
2. **Given** a task that has already been marked done, **When** its owner
   marks it done again (e.g., a duplicate client request), **Then** the
   system does not error and the task remains `done`.

### Edge Cases

- What happens if the task's owner becomes unavailable before marking it
  done? Any current claimant of the task may mark it done; ownership does
  not need to be transferred first.
- What happens if the external project board is temporarily unreachable
  when a task completes? The task's local status still reflects `done`;
  the board eventually shows the correct state once notified.

## Requirements

### Functional Requirements

- **FR-001**: When an agent marks a task done, the system MUST update the
  task's local status field to `done`.
- **FR-002**: When a task's local status becomes `done`, the system MUST
  call the external project board's webhook endpoint to reflect the new
  status on the corresponding card.
- **FR-003**: The system MUST NOT report a task as `done` on the external
  project board unless its local status is also `done` -- the board must
  never show completion the local record doesn't agree with.
- **FR-004**: Marking an already-`done` task done again MUST be accepted
  without error and MUST NOT change its status or timestamps.
- **FR-005**: The webhook payload sent to the project board MUST include
  the task's identifier and its new status. The payload's field ordering
  and any additional descriptive fields are left to the implementer.

### Key Entities

- **Task**: A unit of tracked work with a stable identifier, an owner, and
  a status (`open`, `in_progress`, `done`).
- **Project Board Card**: The external board's own representation of a
  task's status, updated only via the webhook in FR-002.

## Success Criteria

- **SC-001**: Within 5 seconds of a task being marked done under normal
  network conditions, the project board's card for that task shows `Done`.
- **SC-002**: Marking an already-done task done again never produces a
  duplicate card, a changed timestamp, or an error response.

## Assumptions

- The external project board's webhook endpoint accepts a task identifier
  and a status string; its own response format is out of scope for this
  specification.
- Network calls to the project board may occasionally fail transiently;
  FR-002 does not assume the board is always reachable at the moment a
  task completes.
