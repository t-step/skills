# Slice Review: Edit team member role

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
None.

## Out of scope
None.

## Verification evidence
```
$ pytest members/test_roles.py -v
test_owner_can_change_role PASSED
test_role_change_is_logged PASSED
test_non_owner_cannot_change_role_403 PASSED
3 passed in 0.04s
```

## Reasoning
Adds `PATCH /teams/:id/members/:member_id` to change a member's role
(viewer/editor/owner). Every role change is written to the
`member_actions` audit table, the same table `revoke` and `restore`
already write to. Access is restricted to team owners.
