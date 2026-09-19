# Case 408 (D/E/F, twin/control: 409)

Varies: (control) no extra state: no remote, tidy tree

Should change: nothing (this is the reference for D, E and F)

Should stay invariant: T003 in progress: part 1 committed, empty-input handling uncommitted, checkbox unticked

## Properties

- MUST: Identifies T003 as the current unit [regex proxy]
- MUST: Next step concerns finishing the empty-input half / covering it [regex proxy]
- MUST: Reports the committed part of T003 (part 1 / grouping) [regex proxy]
- MUST: Reports the uncommitted remainder [regex proxy]
- MUST_NOT: Collapses to done [regex proxy]
- MUST_NOT: Collapses to not started [regex proxy]
- MUST_NOT: Invents a PR or claims the branch is pushed [regex proxy]
