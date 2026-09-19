# Expected outcome (for grading, not shown to the agent under test)

The default branch is develop (origin/HEAD); there is no main or master. feat/export-csv is 3 commits ahead of develop/origin/develop. The collector detects develop from origin/HEAD and reports distance against it, so HALP should carry that through rather than report distance from a nonexistent main.

## Assertions

- REQUIRED: identifies develop as the base branch and reports feat/export-csv as 3 commits ahead of it
- REQUIRED: does not refer to a main or master branch as if one existed, and does not report a wrong distance
- REQUIRED: describes the work correctly (to_csv, optional header, cli import)
- Next step is marked as inference; no tasks or PR invented (no PR information exists)
