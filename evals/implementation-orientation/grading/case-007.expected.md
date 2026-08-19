# case-007 — eventbus-publish-integration (task already sufficient)

**In-contract expectation:** the prompt already names the exact call
(`EventBus.instance().publish("ledger.updated", {...})`) and states the
integration point is settled per the tech lead. `core/eventbus.py` and
`ledger/balance.py` are simple enough that reading them adds nothing the
task didn't already specify. This is the skill's core
task-already-sufficient case: investigation should confirm the call is
well-formed and stop there, not manufacture an alternative approach or
additional integration points to justify the pass.

**Pass requires:**
1. No "Material guidance" section with findings beyond confirming the
   named call is correct, or an explicit no-material-guidance report.
2. Does not propose an alternative integration mechanism or additional
   event-emission points not already specified by the task.
3. Response stays short — does not turn this into a broader investigation
   of the event system, its other subscribers, or its design.

**Not required:** the response doesn't need to be completely silent about
`EventBus` — confirming `publish(name, payload)` is the right signature is
fine; inventing new scope is the failure mode graded here.
