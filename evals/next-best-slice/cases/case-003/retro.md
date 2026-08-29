# Slice Retrospective: Add in-app notification system

## What we proved
In-app notification delivery, dedupe-within-window, and read-state tracking
all work correctly, backed by the three passing tests and a manual staging
check.

## Assumptions validated
The pluggable `NotificationChannel` interface design — built expecting
in-app to be the first of possibly several channels — held up without
rework: the in-app implementation only needed to implement `send()`, and
enqueue/dedupe/read-state stayed shared.

## Assumptions falsified
None.

## Remaining uncertainty
Nothing major for the in-app channel itself. Channel-specific delivery
guarantees (e.g. handling a bounced email, a failed SMS send) are untested,
since only the in-app channel exists so far.

## Intentional non-goals
Any channel besides in-app — email, SMS, push — was explicitly deferred per
goal.md, which scoped this slice to "ship the pipeline and one channel end
to end."

## Architectural consequences
A `NotificationChannel` interface now exists. Adding a new channel means
implementing one `send(notification, user)` method; enqueue, dedupe, and
read-state are already shared and don't need to be rebuilt.

## Follow-up questions
Which channel should be added next?
