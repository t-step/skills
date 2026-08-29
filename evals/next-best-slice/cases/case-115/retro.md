# Slice Retrospective: Edit team member role

## What we proved
Role changes are correctly restricted to team owners and are written to
`member_actions` alongside revoke/restore events, backed by the three
passing tests.

## Assumptions validated
The `member_actions` table added for revoke could be reused for restore
and now role-edit without a schema change — validated a second and
third time.

## Assumptions falsified
None.

## Remaining uncertainty
None specific to this slice.

## Intentional non-goals
Bulk role changes (multiple members at once) were out of scope per
goal.md — this slice only handles one member at a time.

## Architectural consequences
`member_actions` is now a generic, reusable audit log for member-related
admin actions (add, revoke, restore, role-edit) — any future member
action can write to it without new infrastructure.

## Follow-up questions
None.
