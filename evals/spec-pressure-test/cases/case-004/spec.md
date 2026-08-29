# Feature Specification: Claim Continuity for Long-Running Reviews

**Status**: Draft

**Baseline**: This feature extends `review-queue-core` (already
implemented). It does not reopen review-queue-core's settled decisions on
claim acquisition, release, or override arbitration except where this
document explicitly says otherwise.

**Input**: "Long reviews sometimes outlast the reviewer's session. We don't
want a review that's still genuinely active to get yanked away from
someone just because their laptop went to sleep, but we also don't want it
stuck forever if they really did disappear."

## User Scenarios & Testing

### User Story 1 - Keep a long review moving without losing continuity (Priority: P1)

A second reviewer notices a claimed item whose original claimant appears
unreachable (no heartbeat, session gone) but wants to pick it up and keep
working without a gap in which the item could be grabbed by a third party
mid-handoff, and without waiting for a separate, earlier confirmation step.

**Acceptance Scenarios**:

1. **Given** a claimed item whose original claimant's session is no longer
   reachable, **When** a second reviewer initiates continuity takeover,
   **Then** the item ends up claimed by the second reviewer, with no point
   in time during the takeover at which a third reviewer could have
   observed the item as unclaimed and claimed it themselves.

## Requirements

### Functional Requirements

- **FR-001**: When the current claim owner's session is unreachable, the
  system MUST allow another reviewer to take over the claim in a single
  operation that leaves the item continuously claimed throughout -- never
  observable by a third actor as unclaimed at any point during the
  takeover, and without requiring that reviewer to first perform a
  separate release step before claiming.
- **FR-002**: A continuity takeover MUST record the new owner, a
  timestamp, and a note that this claim originated from a takeover rather
  than an ordinary acquisition.
- **FR-003**: The original claimant, if their session later becomes
  reachable again, MUST be able to see that their claim was taken over and
  by whom.

### Key Entities

- **Continuity Takeover**: A claim transfer from an unreachable owner to a
  new owner, intended to feel instantaneous and gap-free from every other
  actor's point of view.

## Success Criteria

- **SC-001**: In repeated test scenarios, no third reviewer's concurrent
  claim attempt during a continuity takeover ever succeeds in claiming the
  item out from under the takeover.
- **SC-002**: The original claimant can always determine, after the fact,
  that a takeover occurred and who now holds the claim.

## Assumptions

- review-queue-core's existing claim rules continue to apply except where
  this document overrides them: release by anyone other than the recorded
  owner is an override, permitted only on the basis of an observed
  stale-claim finding, and is never combined with a subsequent claim into
  one atomic operation -- an actor who releases a claim must separately win
  a new claim through ordinary arbitration, the same as any other actor.
  review-queue-core provides no atomic release-and-reacquire primitive.
- "Session unreachable" in this document is judged by the second reviewer
  at the moment they act, not by a prior, separately recorded
  stale-claim finding.
