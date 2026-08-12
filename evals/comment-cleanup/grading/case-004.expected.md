# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** this key grades the response's classification
*report*, not applied edits. The prompt carries no explicit apply intent
(and its subject is preservation/flagging, not deletion), so the correct
response is a report only — zero files touched, no refactor performed.

**Scope:** `parser/tokenize.py`, one large comment above a genuinely dense,
magic-number-driven hand-rolled state machine.

**Expected disposition:** **Preserve the comment as-is; do not refactor
`tokenize`.** The comment is accurate (it correctly describes the two
states and the special-cased branch that closes a number and emits an
operator in the same step) and is the only thing making the function's
dense conditionals and bare `0`/`1` state codes readable. This is the
fixture's "large comment compensating for confusing code" case: the
correct output is to **flag** the tokenizer's low readability (magic
state numbers, a branch with two responsibilities) as a code-quality
observation in the report, not to rewrite `tokenize` into something
clearer — restructuring it is a larger, riskier task than a comment pass,
and nothing about "clean up the comments" authorized changing behavior.
**Recommended home:** the comment itself is the right home — it is
tightly coupled to the specific magic-number branches it documents, not a
general, project-wide decision suited to a repo-wide decision log; a
decision-log entry is a defensible addition, not a replacement.

**What a wrong answer looks like:** rewriting `tokenize` to use an `Enum`
or splitting the dual-responsibility branch "for clarity," with or without
also touching the comment. Also wrong: deleting or trimming the comment
because it's long — its length is proportional to genuinely non-obvious
information (the state table, the profiling rationale, the special-cased
branch), not padding. Also wrong under this contract: any file edit made
without being asked, or a report that flags the readability issue but
gives no placement recommendation for the preserved comment.
