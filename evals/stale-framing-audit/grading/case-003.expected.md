# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** readme-omits-newly-authoritative-permissions-component

**Why:** The README explicitly scopes itself ("Console's authorization is
made up of two services") and then omits permissions_service.py, which is
the only component admin_actions.py actually calls to gate admin actions.
This clears all three bars this skill's omission test requires: the
README's own stated scope should cover it, a reader following the README
would materially misjudge where to add a permission check (into
ProfileService's vestigial is_admin/can_export columns, which nothing
reads on the authorization path), and there's a concrete component
(permissions_service.py) to name. A correct audit characterizes this as
Omission specifically -- not Contradicted, since the README doesn't state
anything false about ProfileService's flags existing -- and answers the
engineer's question directly: the new check belongs in
permissions_service.py.
