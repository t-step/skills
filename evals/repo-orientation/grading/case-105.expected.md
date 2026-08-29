# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** generated/vendored code that should not dominate the map.

**In-contract.** SKILL.md explicitly warns not to let bulk substitute for
importance and to name vendored/generated code rather than let it crowd out
what matters. `vendor/` outnumbers `src/` in file count but is marked
auto-generated (`vendor/README_VENDORED.txt`, file-level "DO NOT EDIT"
headers) and is excluded from hand-editing per `AGENTS.md`. The map should
foreground `src/generate.py` and `src/cli.py` as the real application code
and mention `vendor/` as a vendored dependency in one line, not enumerate
its files.
