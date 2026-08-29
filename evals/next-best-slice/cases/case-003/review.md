# Slice Review: Add in-app notification system

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- The `NotificationChannel` interface doesn't yet support attachments or
  rich content, only plain text. Fine for launch; worth knowing before a
  channel with richer formatting is added.

## Out of scope
None.

## Verification evidence
```
$ pytest notifications/test_pipeline.py -v
test_enqueue_and_deliver PASSED
test_dedupe_within_window PASSED
test_mark_read PASSED
3 passed in 0.11s
```
Manually verified in staging: triggering a test event shows the
notification badge incrementing and the notification appearing in the
in-app tray within a few seconds.

## Reasoning
Goal was to ship the notification pipeline (enqueue, dedupe, read-state)
plus exactly one delivery channel (in-app) end to end, with the channel
implementation behind a small interface so more channels could be added
later. Both are met and verified.
