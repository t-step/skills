# Slice Retrospective: Add rollback endpoint for a release

## What we proved
Rollback correctly reverts to the prior version and is restricted to
release owners, backed by the three passing tests.

## Assumptions validated
The `release_events` table added for promote/deploy could be reused for
rollback without a schema change — validated a third time.

## Assumptions falsified
None.

## Remaining uncertainty
None specific to this slice.

## Intentional non-goals
Rolling back more than one version at a time (e.g. "go back 3 releases")
was out of scope per goal.md — this slice only reverts to the
immediately prior version.

## Architectural consequences
`release_events` is now a generic, reusable audit log for release
lifecycle actions (promote, deploy, rollback) — any future lifecycle
action can log to it without new infrastructure.

## Follow-up questions
The `/deployments` dashboard renders `release_events` rows but has no
case for the new `rollback` event type yet — rollback events currently
show up in the dashboard as a blank, unlabeled row instead of a
recognizable "rolled back" entry.
