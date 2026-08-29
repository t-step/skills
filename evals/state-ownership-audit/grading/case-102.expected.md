# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** guarded-lifecycle-scoped-transfer-not-a-hazard

**Why:** Two components writing the same field is the pattern this skill
is tuned to flag as a hazard (see case-005) -- the trap here is applying
that pattern reflexively without checking whether the transfer is
actually guarded. Both `ProvisioningService`'s write functions check
`device.status` and raise `AuthorityError` once active, and
`DeviceManagementAPI.update_config()` raises `NotYetProvisioned` unless a
device is already active -- so a naive pass that flags "two writers of the
same field" without reading the guards at all fails this case. This is
exactly the "transferable authority" shape the skill names explicitly.

**Update after first with-skill run:** the fixture's guard, as actually
written, is a check-then-act pattern -- a `SELECT status` followed by an
`UPDATE devices SET config = ...` with no `status` condition on the
`UPDATE` itself -- not a single atomic operation. The graded run correctly
found this: the `SELECT`-then-`UPDATE` sequence is not fenced against a
`status` change landing between the two, so a `ProvisioningService` write
that read `status = 'provisioning'` can still commit its `UPDATE` after
`on_heartbeat_success` has since flipped the device to `active`, silently
overwriting a `DeviceManagementAPI` write. This is a genuine, narrower
TOCTOU hazard the fixture actually contains, not a flaw in the skill's
reasoning -- the skill's own instruction to "check for a fencing or
validity guard on every write path that could execute under a stale claim
to authority" is precisely what should catch this. Treat a report that
identifies this race (rather than accepting the status check as a fully
atomic guard) as the correct, higher-quality answer. The bar for this case
is: correctly identifies the transferable-authority shape and names Device
as a lifecycle-audit candidate; does not flag the two writers as a hazard
merely because both touch the same field without reading the guard logic;
and does not stop at "a guard exists" without checking whether that guard
is actually atomic with the write it's meant to protect.
