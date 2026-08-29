# AGENTS

Shared working instructions for this repository, read by every coding agent working in it.

## Repository purpose

This repository develops, evaluates, and distributes portable Agent Skills. Three trees, three distinct jobs — don't blur them:

- `skills/` — canonical, editable Agent Skill source. Every `SKILL.md` is authored and revised here first. This tree is not itself installable.
- `evals/` — evaluation evidence for the skills in `skills/`: agent-visible cases, isolated grading keys, and hand-written run summaries (`RESULTS.md`, `runs/*.md`).
- `plugins/software-engineering/skills/` — a curated, published copy of the subset of canonical skills that have been deliberately released. This is a release projection of `skills/`, not a second authoring location. Claude Code and Codex both install from it via their own manifests (`.claude-plugin/`, `.agents/plugins/`, and `plugins/software-engineering/.claude-plugin/plugin.json` / `.codex-plugin/plugin.json`) — the same files, no per-harness fork.

## Source of truth

- Edit skills under `skills/`. Never treat `plugins/software-engineering/skills/` as the place to make a substantive change — a fix made only there is lost the next time a skill is re-promoted.
- Promotion from `skills/` into the plugin tree is deliberate and one skill at a time, not automatic. Not every canonical skill is published; don't add publication automation without being asked.
- Don't fork a skill into separate Claude and Codex implementations unless a real harness incompatibility forces it. Prefer the portable Agent Skills subset (`name` + `description` frontmatter only) so one file installs verbatim everywhere.

## Scope discipline

Keep changes narrowly scoped to the task in front of you:

- Avoid opportunistic cleanup, migrating unrelated work, or redesigning repository architecture while solving a local task.
- Avoid inventing orchestration, tooling, or infrastructure without a demonstrated need.
- Distinguish an observed defect from a suspected one. An observed failure justifies a direct skill edit; a suspected weakness should usually become eval pressure first (a new case or pressure test), not an immediate rewrite.

## Skill development

A skill earns its place by forcing a specific, recurring reasoning problem or decision boundary to stay explicit — not by restating generic good advice that would apply to any task. When writing or editing one:

- Keep the question or judgment call the skill exists to force front and center; don't let it dissolve into generic advice.
- Prefer deterministic tooling (a script, a check, a calculation) for anything mechanical or verifiable; reserve the skill's own text for interpretation, evidence composition, ambiguity, and judgment a script can't make.
- Match the size of an edit to the size of the problem — a skill is not a style guide, and `AGENTS.md` should never encode any individual skill's internal content.

## Eval expectations

Evals are evidence, not proof:

- Compare skill-assisted behavior against a baseline where that comparison is meaningful, and report it honestly even when the baseline does just as well.
- One successful run is weak evidence. Reserve strong verbs (proves, disproves, confirms) for conclusions the case count and effect size actually support; otherwise say "suggestive" and name what more evidence would be needed.
- An observed failure justifies a skill change. A suspected weakness should usually become eval pressure before a skill rewrite — these are different actions; don't conflate them.
- Keep agent-visible fixtures (`cases/`) isolated from grading material (`grading/`, `expected*` files, answer keys) — a case must never leak the scenario label or verdict it's testing.
- Raw per-run transcripts are local artifacts; commit the hand-written summary, not an ignored raw run directory (see `.gitignore`).
- A small wording edit to a skill doesn't need a full eval campaign — match the evidence effort to the size of the change.

## Verification

Run `bash scripts/check.sh` before any commit or PR touching `skills/` or `evals/`. It's the cheap, deterministic gate over those trees: strict skill-frontmatter lint, eval-isolation/answer-leakage check, and cross-skill dependency validation. This repository is private, so GitHub CI runs rarely — run this locally and confirm it passes; never rely on CI as the first execution of these checks.

Plugin/release validation is a separate concern from `scripts/check.sh`. If a change touches `plugins/software-engineering/` (including its manifests), inspect the existing release/versioning rules — `.github/workflows/validate-release.yml` and `scripts/check-plugin-version-bump.sh` enforce that `plugin.json`'s version is bumped whenever the plugin's runtime contents change — rather than guessing at what's required.

## Git and change safety

- Inspect the current branch/worktree state before editing; don't touch unrelated branches or worktrees.
- Don't commit, push, or merge unless the task or repo convention calls for it.
- Before finishing, inspect the actual diff against the intended base and keep it to what was asked.
- Keep PRs narrowly scoped — one concern per PR, consistent with Scope discipline above.
