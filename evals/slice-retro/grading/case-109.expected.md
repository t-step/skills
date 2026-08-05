# Expected retrospective outcome (for grading, not shown to the agent under test)

**In-contract expectation:** Architectural consequences does not credit
`utils/phone.py`'s `normalize_phone_number()` as an architectural
consequence on the strength of being a generic, reusable, dependency-free
helper -- nothing else in the diff or verification actually calls it yet.
If Architectural consequences names anything, it's grounded in what
`handle_signup()` itself now actually does (phone numbers are validated
and normalized before being stored), not in the helper's own
extractability or the notes' stated intent for future reuse.

**Why:** This fixture directly probes the newly-added distinction in
SKILL.md's Architectural consequences bullet: a helper is not an
architectural consequence merely because it *could* be reused later. Only
one call site (`signup_flow.py::handle_signup`) exists; nothing else in
the repo currently depends on `utils/phone.py`. `notes.md` explicitly
frames the extraction as forward-looking ("so any other part of the app
... can just import it") -- exactly the kind of claim this skill's
evidence discipline should treat as the author's stated intent, not a
proven architectural fact.

**Contract framing:** grounded in the newly-added SKILL.md sentence: "A
helper, an abstraction, or an implementation convenience is not an
architectural consequence just because it's reusable or well-factored...
It becomes one only when the slice establishes a durable production
capability, contract, dependency, or boundary that other, already-real
work actually relies on."
