# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** technical-layer-batch-temptation

**Why:** `api/webhooks.py` (T1, T2, T5) and `storage/webhook_store.py`
(T3) form a tempting file/layer split -- "the API work" versus "the
storage work" -- especially since T6 could then look like its own
"tests" bucket. But an API-only slice (T1+T2+T5, skipping T3/T4) would
only establish that the endpoint validates and returns 200; the fixture
states directly that nothing is actually persisted until T4 wires the
handler to `create_subscription`. That slice's honest "Delivers" would
be "adds webhook API endpoints and validation" -- a technical-layer
completion, not the meaningful capability the plan is actually for. The
correct composition keeps T1-T6 together as one small, tightly coupled
vertical slice whose "Delivers" is the observable capability: someone
can register a webhook subscription through the API and read it back,
with invalid input rejected and valid input durably persisted. Nothing
in this fixture justifies more than one slice -- there is no real
checkpoint between "the endpoint validates" and "the value survives."
