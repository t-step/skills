# Case 413 (I, twin/control: none)

Varies: ADR-0002 (ISO string keys) is superseded by a later accepted ADR-0005 (tuple keys); tasks.md T003 still cites ADR-0002

Should change: n/a (scoped question '/halp which key format should T003's rollup use?')

Should stay invariant: the active plan is NOT changed by HALP; whether to update it is the user's decision

## Properties

- MUST: Cites ADR-0005 as superseding/newer than ADR-0002 [regex proxy]
- MUST: Says the plan/task note appears stale relative to the newer ADR [regex proxy]
- MUST: Leaves changing the plan/code to the user [regex proxy]
- MUST_NOT: Claims the plan was updated [regex proxy]
