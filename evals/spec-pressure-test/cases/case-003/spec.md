# Feature Specification: Stale Claim Report

**Status**: Draft

**Input**: "Operators need a way to see which claimed work items look
abandoned, so they can decide whether to release them."

## User Scenarios & Testing

### User Story 1 - List claims that look abandoned (Priority: P1)

An operator runs a command and gets a list of every currently claimed work
item whose claim looks stale (its recorded worktree or branch no longer
exists), so they can decide which ones to release.

**Acceptance Scenarios**:

1. **Given** three claimed items, two with deleted worktrees and one with
   an intact worktree, **When** an operator requests the stale claim
   report, **Then** the report lists exactly the two items with deleted
   worktrees.
2. **Given** no claimed items have a deleted worktree, **When** an
   operator requests the report, **Then** the report states plainly that
   no stale claims were found.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST determine, for every currently claimed item,
  whether its recorded worktree or branch still exists.
- **FR-002**: The system MUST produce a report listing every item found
  stale by FR-001, including at minimum: the item's identifier, its
  claimed-by owner, and the missing worktree/branch path that made it
  stale.
- **FR-003**: The report MUST NOT modify any claim, item status, or
  blocking relationship -- generating it is read-only.
- **FR-004**: When no stale claims exist, the report MUST say so explicitly
  rather than printing nothing.

### Key Entities

- **Stale Claim Report**: A point-in-time, read-only listing of stale
  claims, intended for an operator to read directly at a terminal (or pipe
  through a tool like `grep` to filter by owner or item id) while deciding
  what to release. No other part of this system consumes the report's
  output; releasing a claim remains a separate, explicit operator action
  taken after reading it.

## Success Criteria

- **SC-001**: Every claim whose worktree/branch is missing at the moment
  the report is generated appears in it exactly once.
- **SC-002**: No claim with an intact worktree/branch ever appears in the
  report.

## Assumptions

- The report is a human-facing, interactive artifact. No other command,
  script, or downstream system in this specification's scope reads the
  report's output and acts on its structure or ordering; every field FR-002
  requires is present as text an operator (or a text filter like `grep`
  they choose to pipe it through) can read, but the exact layout, column
  order, and formatting of the report are left to the implementer.
