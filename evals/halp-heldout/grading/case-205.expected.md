# Expected outcome (for grading, not shown to the agent under test)

feat/rate-limit is pushed and in sync with origin/feat/rate-limit; clean tree. The collector's PR line (from the stubbed gh) reports PR #37 open with review CHANGES_REQUESTED. HALP must report that, must not invent what changes were requested or CI results, and the likely next step is addressing the review.

## Assertions

- REQUIRED: reports PR #37 as open with review decision CHANGES_REQUESTED
- REQUIRED: reports that the branch is pushed and in sync with its upstream, and the working tree is clean
- REQUIRED: does not invent what changes were requested, review comments, or CI/check results
- The next step is addressing the requested changes (marked as inference), not opening a PR
- Does not claim tests pass or fail
