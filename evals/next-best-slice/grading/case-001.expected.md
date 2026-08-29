# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** dependency-unlock

**Why:** The retro's architectural-consequences section is unambiguous:
any route can now require auth via one decorator, which wasn't possible
before this slice. The backlog's `/api/account` candidate is the direct,
small application of that new capability, and it also happens to close a
real access-control gap the backlog description names explicitly (any
caller can read any account's data today). That combination — dependency
unlock, small size, and a concrete risk it reduces — makes it the clearly
strongest candidate; the RBAC system is the "largest milestone" trap, and
the routing refactor is the "architecture-aesthetic, not evidence-backed"
trap. A good recommendation should identify the account-protection slice
plainly and explain why the other two wait, without treating the
correctness of the pick as requiring elaborate justification — this case
is meant to be the clean, low-ambiguity baseline.
