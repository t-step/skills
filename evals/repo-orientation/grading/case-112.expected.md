# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** graceful default when no capability is announced —
control case for case-111/114.

**In-contract.** No file or prompt text in this fixture mentions any
navigation/indexing capability. SKILL.md's new "Gather before writing"
bullet is conditional ("if a repository-navigation capability is already
available") and must not manufacture behavior when nothing triggers it.
`src/formatter_v1.py`'s `format_table_v1` is unambiguously unreferenced —
`src/cli.py` imports `format_table` from `src/formatter.py`, not
`formatter_v1`. A correct response produces a complete, standard
orientation via manifests/imports/tests alone, does not stall or hedge on
tool absence, and never mentions wanting, needing, or missing an indexing
capability that was never brought up.
