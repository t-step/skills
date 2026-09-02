# Archive: frozen historical evidence

This directory preserves, byte-for-byte, the skill and eval files that the
historical evals under `evals/cloudscape-native-expression-review/` (and, by
citation, `evals/design-system-native-expression-review/`) reference. Those
historical documents cite paths that no longer exist in this repository's
tree — `skills/cloudscape-native-expression-review/SKILL.md`,
`skills/cloudscape-implementation-audit/SKILL.md`, and
`evals/cloudscape-implementation-audit/RESULTS-ITERATION-2.md` — because the
squashed PR that introduced this eval history intentionally excludes the
`evals/cloudscape-implementation-audit/` tree and the pre-rename
`skills/cloudscape-native-expression-review/` skill directory. This archive
lets a reader inspect that cited evidence without reconstructing deleted
branch history.

**These are frozen evidence snapshots only. They are not active canonical
skills and are not wired into any skill-loading mechanism.** The active,
maintained skill is [`skills/design-system-native-expression-review/`](../../../skills/design-system-native-expression-review/).

## Files and provenance

| Archived file | Original path | Source commit |
| --- | --- | --- |
| `cloudscape-native-expression-review/SKILL.md` | `skills/cloudscape-native-expression-review/SKILL.md` | `2745d971f7de653cd05113aa9de3e6ff83ca5401` — "chore: retire cloudscape-implementation-audit as an active skill" (last commit to touch this content before the directory was renamed and rewritten into `skills/design-system-native-expression-review/` at `85e1b368d02c304fe85b0661b3afc2a0a8f8d799`) |
| `cloudscape-native-expression-review/scripts/inspect_surface.py` | `skills/cloudscape-native-expression-review/scripts/inspect_surface.py` | `2745d971f7de653cd05113aa9de3e6ff83ca5401` |
| `cloudscape-native-expression-review/scripts/resolve_versions.py` | `skills/cloudscape-native-expression-review/scripts/resolve_versions.py` | `2745d971f7de653cd05113aa9de3e6ff83ca5401` |
| `cloudscape-implementation-audit/SKILL.md` | `skills/cloudscape-implementation-audit/SKILL.md` | `db46d43` — "feat: cloudscape-implementation-audit iteration 2 — escalation pressure test (ITERATE)" (last commit that authored this content; content is unchanged in the parent of `2745d97`, the commit that deleted the file) |
| `cloudscape-implementation-audit/RESULTS-ITERATION-2.md` | `evals/cloudscape-implementation-audit/RESULTS-ITERATION-2.md` | `db46d43` — same commit; this is the run that documents the D-grade pattern-selection overreach that `cloudscape-native-expression-review`'s own eval (section 6 of `evals/cloudscape-native-expression-review/RESULTS.md`) cites as the reason `cloudscape-implementation-audit` was retired |

Each file's content was extracted with `git show <commit>:<original path>` and
verified byte-identical to the source blob via `git hash-object`. None of
this text was paraphrased or reconstructed from memory.

These commits live on `backup/design-system-calibration-mui-generalization-pre-pr`
(and `backup/design-system-calibration-mui-generalization-with-fixups`), the
unsquashed history this PR's single commit was squashed from. They are not
ancestors of `main` or of this branch's own commit.

## Historical path references

Historical documents under `evals/cloudscape-native-expression-review/` and
`evals/design-system-native-expression-review/` were written when
`skills/cloudscape-native-expression-review/SKILL.md`,
`skills/cloudscape-implementation-audit/SKILL.md`, and
`evals/cloudscape-implementation-audit/RESULTS-ITERATION-2.md` existed at
those paths in the working tree. Those references are left as originally
written — they are historically truthful record of what was true at the time
— and are not rewritten to point here. Any reader following one of those
paths today should look for the corresponding file in this archive instead.
