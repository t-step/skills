# Feature Specification: Manual Override for Bundle Readiness

**Status**: Draft

**Input**: "Normally a review bundle is ready for human sign-off once all
its child tasks are done. Sometimes a lead wants to fast-track a bundle
for review before every child task is finished -- give them a way to do
that without breaking the normal computed check for everyone else."

## User Scenarios & Testing

### User Story 1 - Bundle becomes ready once all children are done (Priority: P1)

The ordinary path: once every child task under a bundle reaches a
terminal status, the bundle is considered ready for review.

**Acceptance Scenarios**:

1. **Given** a bundle with two child tasks, one still open, **When**
   readiness is computed, **Then** the bundle is not ready.
2. **Given** the same bundle once both children reach a terminal status,
   **When** readiness is computed, **Then** the bundle is ready.

### User Story 2 - A lead fast-tracks a bundle (Priority: P2)

A lead marks a bundle ready for review even though a child task is still
open, to unblock a time-sensitive review.

**Acceptance Scenarios**:

1. **Given** a bundle with an open child task, **When** a lead sets the
   bundle's manual-ready flag, **Then** the bundle can be moved into review
   despite the open child task.

### Edge Cases

- What happens if a lead sets the manual-ready flag and then a previously
  open child task later completes normally? The bundle was already
  fast-tracked; nothing about this specification requires the flag to be
  cleared.
- What happens if a lead sets the manual-ready flag on a bundle whose
  children are all already done? This is harmless -- the bundle was ready
  anyway.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST compute a bundle's ordinary readiness as
  true exactly when every child task attached to it has reached a terminal
  status (`done` or `superseded`), and false otherwise.
- **FR-002**: The system MUST allow a lead to set a manual-ready flag on
  any bundle, independent of its computed readiness.
- **FR-003**: A bundle MAY be moved into `review` status when either its
  computed readiness (FR-001) is true, or its manual-ready flag (FR-002)
  is set.
- **FR-004**: Clearing the manual-ready flag MUST be possible and MUST NOT
  affect any child task's own status.
- **FR-005**: The system MUST record, for any bundle moved into `review`
  via the manual-ready flag rather than ordinary computed readiness,
  which path was used, so a reviewer can see whether a bundle was
  fast-tracked.

### Key Entities

- **Review Bundle**: Carries both a computed-readiness fact (FR-001,
  derived fresh from its children's statuses) and a manual-ready flag
  (FR-002, an independently settable field). Both can permit entry into
  `review` (FR-003).

## Success Criteria

- **SC-001**: A bundle with all children terminal is always computed as
  ready, regardless of the manual-ready flag's value.
- **SC-002**: A bundle can always be moved into review once either FR-001
  or FR-002's condition holds, per FR-003.
- **SC-003**: Whether a given `review`-status bundle got there via
  computed readiness or the manual-ready flag is always determinable
  after the fact (FR-005).

## Assumptions

- Only a lead (not an ordinary agent) may set or clear the manual-ready
  flag; who counts as a lead is determined by existing repository
  permissions, out of scope here.
