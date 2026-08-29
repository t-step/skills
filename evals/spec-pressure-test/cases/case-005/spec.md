# Feature Specification: Offline-Friendly Work Item Browser

**Status**: Draft

**Input**: "Give agents a fast local browser for work items that doesn't
need to hit the server on every keystroke, but never let it show
something blocked as available."

## User Scenarios & Testing

### User Story 1 - Browse available work items quickly (Priority: P1)

An agent opens the local browser to see which work items are safe to
start. The browser should feel instant -- no network round trip per
screen -- while still being trustworthy about what's actually available.

**Acceptance Scenarios**:

1. **Given** the browser has synced a snapshot of work items at some point
   in the last hour, **When** an agent opens it, **Then** the list of items
   shown as available renders immediately from the local snapshot, with no
   network call required to display the initial screen.
2. **Given** an item is blocked on another item that has not yet reached a
   terminal status, **When** the browser renders its available-items list,
   **Then** that blocked item MUST NOT appear as available.

### Edge Cases

- What happens when the local snapshot is more than an hour old? The
  browser still renders from it; a background sync refreshes it when
  possible, and the UI shows the snapshot's age.

## Requirements

### Functional Requirements

- **FR-001**: The browser MUST maintain a local, periodically-synced
  snapshot of work items sufficient to render the available-items list
  without a network call.
- **FR-002**: The browser MUST NOT render any item as available if it is
  currently blocked on an unresolved item.
- **FR-003**: The local snapshot MUST be refreshed opportunistically in
  the background (e.g., every few minutes, or when network connectivity is
  detected after being offline) without blocking the UI.
- **FR-004**: The browser MUST display the age of the snapshot currently
  being shown, so an agent can judge how current the view is.

### Key Entities

- **Local Snapshot**: A periodically-refreshed local copy of work-item
  status and blocking relationships, synced from the server on the cadence
  described in FR-003. The server remains the sole authoritative source of
  current status and blocking state; the snapshot is a read cache with no
  independent authority.

## Success Criteria

- **SC-001**: The browser's initial screen renders from the local snapshot
  in under 100ms, with no network call in the critical path.
- **SC-002**: No item ever renders as available while it is actually
  blocked, as observed by the authoritative server state at render time.

## Assumptions

- The server-side blocking computation itself (which items are blocked on
  which) is unchanged by this feature and is out of scope here.
- Network connectivity for background sync (FR-003) is intermittent by
  design assumption -- the browser is meant to remain usable while offline.
