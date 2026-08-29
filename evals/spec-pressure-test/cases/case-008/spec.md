# Feature Specification: Child Tasks Under a Review Bundle

**Status**: Draft

**Input**: "Group several small tasks under one review bundle that a human
signs off on as a whole. Once the bundle is under review, stop letting new
tasks get added to it -- the reviewer should be looking at a fixed set."

## User Scenarios & Testing

### User Story 1 - Add tasks to an open bundle (Priority: P1)

An agent adds a task to a review bundle while the bundle is still being
assembled (before a human starts reviewing it).

**Acceptance Scenarios**:

1. **Given** a bundle in `open` status, **When** an agent adds a task
   naming that bundle as parent, **Then** the task is created and attached
   to the bundle.
2. **Given** a bundle in `review` status, **When** an agent attempts to add
   a task naming that bundle as parent, **Then** creation is rejected and
   no task is created -- the reviewer must see a fixed set of tasks.

### Edge Cases

- What happens if the bundle named as parent doesn't exist? Creation is
  rejected and no task is created.

## Requirements

### Functional Requirements

- **FR-001**: Creating a task with a given bundle as parent MUST check
  that the named bundle currently has status `open`; if it does not (e.g.,
  it is `review`, `accepted`, or doesn't exist), creation MUST be rejected
  and no task row MUST be written.
- **FR-002**: A bundle transitions from `open` to `review` when a human (or
  agent acting on the human's behalf) explicitly moves it into review,
  once every task currently attached to it has reached a terminal status.
- **FR-003**: Once a bundle is in `review` status, the set of tasks
  attached to it MUST be exactly what the reviewer sees -- FR-001 is what
  keeps that set fixed going forward.
- **FR-004**: A human reviewing a bundle in `review` status MUST see every
  task that was attached to it, with no task silently excluded or added
  after the review began.

### Key Entities

- **Review Bundle**: A group of tasks with a status (`open`, `review`,
  `accepted`). Accepts new child tasks only while `open` (FR-001).
- **Task**: A unit of work belonging to exactly one bundle, named at
  creation time.

## Success Criteria

- **SC-001**: In no test scenario does a bundle in `review` status end up
  with more tasks attached to it than it had at the moment it entered
  `review`.
- **SC-002**: A reviewer's view of a bundle's task set is always exactly
  the set that was attached when review began, for the duration of the
  review.

## Assumptions

- Only one bundle status transition (`open` -> `review`) is relevant to
  this specification; what happens during or after a human's review
  decision is covered elsewhere.
- Task creation and bundle status transitions are both ordinary,
  independently-initiated operations -- there is no single human or agent
  workflow step that performs both together.
