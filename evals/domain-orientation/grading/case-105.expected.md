# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** generated-boilerplate-tempts-full-enumeration

**Why:** `generated_events.py` contains twelve structurally identical
dataclasses -- same three fields, no validation, no rule, nothing
domain-specific beyond a type name -- sitting in the same directory as
`ingestion.py`, which holds the fixture's actual domain logic (session
grouping by time gap, an anomaly threshold on failed logins). The bait
is that each generated class *looks* like it deserves its own entry the
same way `Session` and `Anomaly` do -- they're dataclasses with fields,
same as everything else in this skill family's other fixtures. The
correct answer applies "Selecting what belongs in the map" and names the
twelve collectively as generated, artifact-level event wrappers, giving
full first-class treatment only to `Session` and `Anomaly`, which is
where this fixture's actual invariants (`SESSION_GAP_MINUTES`,
`FAILED_LOGIN_ANOMALY_THRESHOLD`) live.
