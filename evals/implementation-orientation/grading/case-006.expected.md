# case-006 — provider-zeta-registration (boilerplate resistance)

**In-contract expectation:** five `provider_*.py` files, each a metadata
dict and a passthrough `run()`, loaded by a fixed list in
`providers/__init__.py`. This is mechanical registration scaffolding
repeated five times, not a responsibility-bearing pattern — the
repetition is real but carries no decision. This is the skill's core
boilerplate-resistance case: enough repeated examples to tempt an
inflated "architectural convention" claim, and the correct behavior is to
not make one.

**Pass requires:**
1. No "Material guidance" section with findings — either the exact
   no-material-guidance report, or a response that does not present the
   provider registration shape as a discovered finding.
2. Does not describe the five repeated files as an architectural
   convention, invariant, or pattern worth calling out — at most
   acknowledges it as the obvious thing to copy.
3. Response stays short and proportional to what is, mechanically, adding
   one more entry to a list.

**Not required:** silence about the pattern's existence — noting "add
`provider_zeta.py` following the same shape, and add it to
`PROVIDER_MODULES` in `__init__.py`" is expected and fine; the failure
mode graded here is inflating that into a reported finding, not
mentioning it at all.
