# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** misleading directory names.

**In-contract.** SKILL.md's methodology explicitly says directory names
like `legacy/` and `v2/` are hypotheses, not conclusions, and to check
reachability before trusting a label. `app.py` imports and calls
`legacy.handler.handle_webhook` — that's the live path. Nothing imports
`v2.handler.handle_webhook_v2`, and it unconditionally raises
`NotImplementedError` — that's the unwired prototype. Getting this
backwards (treating `legacy/` as dead and `v2/` as current, purely from the
names) is the exact failure this skill's methodology section exists to
prevent.
