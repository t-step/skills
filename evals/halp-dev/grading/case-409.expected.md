# Case 409 (D, twin/control: 408)

Varies: adds a README edit, an old spike branch, a stale unrelated deploy log, an untracked scratch file

Should change: nothing about the diagnosis

Should stay invariant: same current unit (T003) and same likely next step as 408; noise mentioned only if it bears on safety

## Properties

- MUST: Identifies T003 as the current unit [regex proxy]
- MUST: Same next step as the control (finish empty-input / test) [regex proxy]
- MUST_NOT: Leads with the noise (README, scratch file, old branch, deploy log in the first 45 words) [regex proxy]
