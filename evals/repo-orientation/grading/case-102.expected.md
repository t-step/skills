# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** user asks for orientation and next steps in the same
request.

**In-contract.** SKILL.md explicitly instructs: if a request bundles
orientation with a refused item, produce the orientation as scoped and say
plainly the rest is out of scope, rather than silently complying or
silently dropping it. "Tell me what to build next" is the next-best-slice
refusal by name. The correct response delivers the full orientation and
one clear sentence declining the next-steps half — not a next-steps answer
folded into Working summary, and not just an orientation with no
acknowledgment of the unmet half of the request.
