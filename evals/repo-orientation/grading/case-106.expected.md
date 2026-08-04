# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** obsolete path that looks current.

**In-contract.** SKILL.md's "prioritize by what's wired in, not what's
present" rule is being tested directly, in its harder direction: unlike
case-106's counterpart (misleading names), `src/notifications/
push_service.py` has an unremarkable name, a docstring, and its own test
file — every surface signal of being real, maintained, current code. But
`AGENTS.md` states the notification entry point is
`src/main.py:notify_activity`, and that function only calls
`email_service.send_email`; nothing calls `push_service.send_push`. A
careful orientation should trace the actual entry point's call graph, not
infer liveness from code quality or test presence.
