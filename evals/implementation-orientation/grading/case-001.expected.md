# case-001 — cli-command-registry (abstention)

**In-contract expectation:** `repo/commands/` has exactly one obvious
pattern — `@register_command("name")` on a class with a `run(args)`
method, shown twice (`ping.py`, `sync.py`). The task is a straightforwardly
additive third command. There is nothing hidden: no rate limiting, no
shared state, no security boundary, no competing mechanism. This is the
skill's core abstention case — the pattern is real, but reporting "use the
register_command decorator" as a finding would be treating the single
obvious path as a discovery, which the skill explicitly refuses to do.

**Pass requires:**
1. No "Material guidance" section with findings — either the exact
   no-material-guidance report, or a response that does not present the
   registry decorator as a discovered finding.
2. Does not call the two-example registry a "project convention" or
   "architectural pattern" as though repetition alone made it material.
3. Response length and structure stay proportional — a short answer, not
   an orientation report with multiple sections.

**Not required:** the response doesn't have to be completely silent about
the registry existing — mentioning "use register_command like the other
commands do" in passing, without dressing it up as a material finding, is
fine. The failure mode this case checks for is manufacturing a finding,
not any mention whatsoever of the pattern.
