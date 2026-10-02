# Repository state at the cutoff

- All the classes named or implied across this task set (`F`, `U`,
  `GridTuple*`, `IgniteException`, `IgniteCheckedException`, `X`,
  `GridLeanMap`, `IgniteUtils`, the `tostring` helpers) currently live in
  `ignite-core`, per the umbrella ticket's own stated motivation.
- A skeleton `ignite-commons` module (a `pom.xml` and an empty `src/main`
  tree) already exists in the repository as of this cutoff, even though
  its own tracking ticket, IGNITE-24782, is not yet marked resolved --
  Jira's "resolved" status on tickets in this set does not reliably
  track exactly when the underlying code change landed. The skeleton
  does not yet contain any of the classes this task set is about moving.
- `GridFunc`, a different class from any named above, was already cleaned
  up (unused methods removed) under a Sub-task of the same umbrella
  ticket, IGNITE-24786, resolved two days before this cutoff. Its own
  description states this was done "to simplify moving code to
  ignite-commons" -- i.e. as prep for moving `GridFunc` itself, which is
  not one of the tasks in this list (no "Move GridFunc" Sub-task exists
  under this umbrella as of this cutoff).
- The `org.apache.ignite.binary` package -- the reason this phase exists
  at all, per IGNITE-24781's own description -- already exists in
  `ignite-core` and is not itself part of this task set; its own
  extraction is described as later work this phase is meant to unblock.
