# Feature Specification: Reviewer Claims on Review Batches

**Status**: Draft

**Baseline**: This feature extends `review-queue-core` (already implemented;
its contract is in `baseline-contract.md`). It does not reopen or
re-litigate review-queue-core's settled decisions on how an item is claimed
by a reviewer -- claim acquisition, release, and override arbitration for a
single queue item are unchanged and continue to work exactly as
`baseline-contract.md` describes. This feature only adds the notion of a
**batch**: a named group of queue items a reviewer wants to work through
together.

## User Scenarios & Testing

### User Story 1 - Group items into a batch and claim them together (Priority: P1)

A reviewer selects several unclaimed queue items and creates a batch
naming all of them, so they can be presented and worked through as one
unit in the reviewer's UI.

**Acceptance Scenarios**:

1. **Given** three unclaimed queue items, **When** a reviewer creates a
   batch naming all three, **Then** the batch is created and each named
   item records that it belongs to this batch.
2. **Given** an existing batch, **When** a reviewer opens it, **Then** the
   UI shows the claim status of each item in the batch individually.
3. **Given** two reviewers who each attempt to claim the same item that
   belongs to a batch, **When** both attempts happen at the same time,
   **Then** exactly one reviewer's claim succeeds and the other receives an
   immediate failure, with no window where both could believe they hold it.

### Edge Cases

- What happens when a batch names an item that is already claimed by
  someone else? The batch is still created; that item simply shows as
  already claimed within the batch view.
- What happens when a reviewer wants to claim every item in a batch at
  once? This specification does not add a batch-level claim operation --
  each item is claimed individually, exactly as review-queue-core already
  defines.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST allow a reviewer to create a batch naming
  one or more existing, unclaimed-or-claimed queue items.
- **FR-002**: Each item named in a batch MUST record which batch(es) it
  belongs to, in addition to its existing review-queue-core fields.
- **FR-003**: Deleting a batch MUST NOT delete, unclaim, or otherwise
  modify any item named in it -- a batch is purely an organizing label.
- **FR-004**: The system MUST allow the same queue item to belong to more
  than one batch at once.

### Key Entities

- **Batch**: A named, orderable list of queue-item references, created by
  a reviewer for their own organizational use. Carries no claim state of
  its own.

## Success Criteria

- **SC-001**: A batch's item list is durable and correctly recoverable
  after the session that created it ends.
- **SC-002**: Deleting a batch never changes the claim, status, or
  identity of any item it named.

## Assumptions

- Claim acquisition, release, and override-on-staleness for an individual
  queue item are entirely inherited from `review-queue-core`
  (`baseline-contract.md`); this specification adds no new claim mechanism
  and does not change single-item claim behavior in any way.
