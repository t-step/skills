# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** one-way-trigger-mistaken-for-sync-need

**Why:** ImportJob and DatasetVersion are both real lifecycles with their
own owners, states, and transition functions -- this is not a false-
lifecycle case. The interaction is exactly one call
(`create_draft_dataset_version` inside `finish()`), fired once, in one
direction, on success only. After that call, `DatasetVersion.publish()`
and `.archive()` never look back at the source job, and nothing in
`import_job.py` ever reads `DatasetVersion`'s state. This is
transition-triggering with no ongoing consistency requirement --
"completed but not yet published" is the intended steady state most of
the time, since publishing is a deliberately separate, manually-timed
curator action. The Slack thread's question ("doesn't that mean the two
systems are out of sync?") is the trap: it assumes coupling exists
merely because one thing caused the other to come into being. A correct
audit distinguishes "A triggered B's creation" from "A and B must track
each other," and declines the proposed `sync_status` mirror field.
