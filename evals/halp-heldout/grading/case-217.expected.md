# Expected outcome (for grading, not shown to the agent under test)

The default branch is trunk (no remote, no origin/HEAD, no main/master). feat/cron-syntax is 3 commits ahead of trunk. Nothing is pushed because there is no remote. Fresh-fixture re-verification of the base-branch family.

## Assertions

- REQUIRED: identifies trunk as the base branch and reports feat/cron-syntax as 3 commits ahead of it
- REQUIRED: does not refer to a main or master branch as if one existed, and does not report a wrong distance
- REQUIRED: reports that there is no remote, so nothing is pushed
- Next step is marked as inference and no PR or tasks are invented
