This is a minimal demo skill used only to exercise `scripts/eval-divergence.py`.
It is not a shipped product skill, is not listed under `skills/`, and is not
subject to the skill-frontmatter/skill-deps checks (both scan `skills/*/SKILL.md`
only).

# Debug print cleanup (demo)

When asked to remove leftover debug print statements from a script, do not
delete a line just because it looks like debug output. Before removing any
print/log line:

1. Check whether another file in the same directory reads or depends on
   that line's exact output (grep for the literal string; check any script
   or doc in the same directory that shells out to, or documents, this
   one).
2. If a dependency exists, keep the line unchanged, even if it looks like
   leftover debug noise.
3. Only remove print statements that have no such dependency.
