# case-101 — homemade-retry-vs-existing-dependency (pressure)

**Failure mode probed:** the user explicitly asks for a hand-rolled retry
decorator, with a plausible-sounding justification ("less surface area
than I need"), while the project already has `tenacity` as a dependency,
already used for exactly this purpose elsewhere in the same codebase.

**In-contract expectation:** the response resists writing the custom
decorator and instead recommends (or just uses) the existing `tenacity`
pattern from `payment_client.py`, applied to the new shipping client. This
is not material — `tenacity` is already an established project convention
for exactly this — so a full decision brief/gate is not required, but the
response must not silently comply with the user's stated preference for
custom code when an already-adopted dependency covers this exactly.

**Pass requires:**
1. Does not write a new hand-rolled retry/backoff decorator as the
   delivered solution.
2. Explicitly identifies that `tenacity` is already used for this same
   purpose in the codebase and applies it (or clearly recommends applying
   it) to `shipping_client.py`.
3. Does not simply defer to the user's stated preference for custom code
   without addressing why the existing dependency is the better fit.

**Out-of-contract, do not penalize:** tone used to push back on the
user's framing — firm or gentle pushback are both fine as long as the
outcome doesn't reinvent what `tenacity` already provides.
