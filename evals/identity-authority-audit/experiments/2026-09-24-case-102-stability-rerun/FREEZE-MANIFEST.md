# Freeze manifest — case-102 stability rerun (N=10)

**PR:** #58 (`identity-authority-audit`)
**Head SHA tested:** `63af571d7f8273d45224abcc1d220f792930e9a5`
**Head commit:** `fix(identity-authority-audit): route unresolved existence-questions out of Findings`
**Frozen at:** 2026-09-24, working tree clean at this SHA (verified via `git status`)

All files under `frozen/` are byte-identical copies of the repo state at
the SHA above (verified against `skills/identity-authority-audit/` and
`evals/identity-authority-audit/` directly, not reconstructed from
memory). None were edited before, during, or after the 10 runs below.
The run prompt (`prompts/case-102-with-skill.md`) is byte-identical to
the frozen prompt already used in the prior
`2026-09-24-review-findings-fix` experiment's n=5 case-102 rerun (that
prompt already embeds this exact post-fix `SKILL.md` verbatim — confirmed
by diff, not reused blind) — the same instrument, not a new one authored
for this pass.

See `CHECKSUMS.sha256` for exact hashes of every frozen artifact and the
run prompt.
