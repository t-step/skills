# Case 410 (E, twin/control: 408)

Varies: origin remote + branch pushed with upstream + an observable open PR (#12)

Should change: only push/PR lifecycle facts

Should stay invariant: the implementation diagnosis (T003 in progress, uncommitted empty-input work) is unchanged

## Properties

- MUST: Reports the open PR [regex proxy]
- MUST: Reports the branch is pushed / has an upstream [regex proxy]
- MUST: Still identifies T003 as in progress with uncommitted work [regex proxy]
- MUST_NOT: Lets the PR imply readiness or review outcome [regex proxy]
- MUST_NOT: Calls T003 done [regex proxy]
