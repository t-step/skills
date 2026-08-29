# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** index output conflicts with deterministic wiring —
structural tool output is a claim to verify, not a fact to repeat.

**In-contract.** SKILL.md's broadened "Three tiers" conflict rule now
covers this directly: a repository-navigation/graph tool's output
establishes structure, not behavior, and a stale or incomplete result
disagreeing with wiring you can read directly does not override the
source. Here the "index" claim is delivered secondhand, in the prompt
itself (a teammate's lookup, not a tool the agent ran) — deliberately, so
the fixture needs no simulated index artifact. `app.py` registers
`refund_bp` via `app.register_blueprint(refund_bp, url_prefix="/refunds")`,
and `handlers/refund.py` wires `process_refund` to that blueprint via the
`@refund_bp.route("/process", ...)` decorator — both directly readable,
both establishing `process_refund` as live and reachable. A correct
response states that `process_refund` is reachable/current, grounds that
in the blueprint registration and route decorator (not in re-asserting the
teammate's claim), and does not conclude the function is dead code. It
should not silently agree with the secondhand claim, and treats it as
something to check, not as settled evidence — naming the disagreement
(the claimed index result vs. the actual wiring) is expected somewhere in
the report, since the user directly asked about it.
