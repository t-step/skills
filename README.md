# skills

A collection of small, portable Agent Skills for recurring software-development
work — orienting in an unfamiliar repository, reviewing a finished change,
writing an honest retrospective, picking the next thing to build, planning how
to build it. Each skill is a self-contained instruction set (`SKILL.md`, plus
supporting files where needed) meant to be handed to a coding agent
alongside a task.

The underlying idea: a lot of what makes an agent (or a person) useful on a
task is a small set of good habits, done consistently — reading the actual
diff instead of trusting the summary, keeping observed fact separate from
inference and speculation, refusing to answer a bigger question than the one
asked. These skills try to write those habits down explicitly enough to be
reused, without turning the work into a rigid procedure. They narrow common
failure modes; they don't replace judgment about the situation in front of
you.

This is also a working repository for figuring out how instructions like
these should be built and revised — with fixtures, adversarial tests, and
recorded results, so changes are driven by observed behavior rather than by
guessing at every possible failure in advance. That process is described
below, but the skills themselves are the point.

## Skills

The table below is generated from each skill's own `SKILL.md` frontmatter —
not hand-maintained — so it can't silently drift the way a hand-edited list
did (two skills once went missing from it). Regenerate it with
`uv run scripts/generate-skill-inventory.py` after adding or changing a
skill; `scripts/check.sh` fails if it's stale. The "Validation" column
reports the honest state of that skill's `evals/<name>/` suite: how many
fixture cases exist, and whether `RESULTS.md` records at least one
actually-executed run or only authored-but-unrun fixtures — see that
script's docstring for the exact detection rule.

<!-- skill-inventory:begin -->
| Skill | What it does | Validation |
|---|---|---|
| [`next-best-product-slice`](skills/next-best-product-slice/) | Recommends exactly one next bounded product slice -- the smallest change that measurably grows what a product's intended users can understand, complete, or rec… | 15 cases · validated (sample) |
| [`next-best-slice`](skills/next-best-slice/) | Recommends exactly one next implementation slice once a completed slice has been reviewed and retrospected — "given what we now know, what's the smallest, high… | 25 cases · validated (sample) |
| [`repo-orientation`](skills/repo-orientation/) | Builds a concise, evidence-backed operating map of a repository before consequential work begins: purpose, governing instructions (root and scoped), major exec… | 22 cases · validated (sample) |
| [`ship-slice`](skills/ship-slice/) | Ships one finished slice: discovers the repo's own complete verification gate (Makefile/package.json/pyproject targets, CI workflows, AGENTS.md/CLAUDE.md), run… | 2 cases · authored, unrun |
| [`slice-plan`](skills/slice-plan/) | Turns one already-accepted implementation slice into an implementation-ready plan: behavioral contract, likely implementation seams, invariants, a verification… | 16 cases · validated (sample) |
| [`slice-retro`](skills/slice-retro/) | Writes a retrospective for one completed implementation slice (a commit, branch, PR, or finished task) — what it actually proved, which assumptions it validate… | 16 cases · validated (sample) |
| [`slice-review`](skills/slice-review/) | Reviews one bounded implementation slice (a diff, PR, or "I finished X" claim) against its stated goal, the repo's own instructions, the actual diff content, a… | 18 cases · validated (sample) |
<!-- skill-inventory:end -->

These bracket an implementation loop rather than complete one: orient before
the work starts; once it's done, review it, ship it (`ship-slice` runs the
repo's own verification gate and commits/tags/pushes only if it passes), and
retrospect on it; decide what's next — by architectural momentum
(`next-best-slice`) or by user-facing product value
(`next-best-product-slice`) — and plan the next slice. The actual
implementing happens in between, outside any of these. Nothing enforces the
order — each skill stands on its own and mostly refuses to do another's job
even when asked.

## How they're built

The development rule for this repository: an observed failure can motivate a
change to a skill's `SKILL.md`; a suspected one gets an eval case first, not
a prompt edit on a hunch. `RESULTS.md` in each eval directory records actual
runs against these fixtures, including disagreements that got written up
rather than smoothed over to hit a clean number.

A new skill does not start with a mature suite. It starts with the smallest
set of fixtures that demonstrates useful behavioral divergence from
baseline and exercises the skill's central failure boundary — often 2-5
cases, not the ordinary-cases-plus-adversarial-pressure-suite shape the
mature skills above have grown into. `scripts/eval-divergence.py` runs a
skill's small fixture set against a fresh baseline (no target skill) and a
fresh skill condition (target `SKILL.md` appended to the system prompt),
captures both, and reports where they diverge — see
`evals/eval-runner-demo/` for a self-contained example. A taxonomy of
possible failure modes, if you have one, is design input for choosing which
2-5 cases to start with — not a checklist requiring one fixture per
category. Regression breadth and an adversarial pressure suite are things a
skill earns over time, grown from observed failures, consequential risks,
and real usage — as every mature skill under `evals/` here in fact did —
not copied wholesale from an existing mature skill's fixture count.

Once a skill does have fixtures: agent-visible fixture inputs live under
`evals/<skill>/cases/`, and isolated answer keys / expected results live
separately under `evals/<skill>/grading/` — so grading can't leak into the
input. `scripts/check-eval-isolation.py` enforces that grading expectations
don't leak into agent-visible fixture content, for any `evals/<skill>/*.json`
manifest shaped like the existing ones.

## Using them

There's no packaging or install step here — this is source, not a
distributed artifact. Each skill is a directory under `skills/` with a
`SKILL.md` written in the Agent Skills format. Using one currently means
exposing `skills/*/SKILL.md` to a compatible agent harness — copied,
symlinked, or otherwise made visible wherever the harness looks — and
letting the harness trigger it from its description, or invoking it
explicitly.

`scripts/skill-usage-report.py` checks, for a local Claude Code install,
whether these are actually getting invoked — a way to notice a skill that's
stopped earning its place, not a feature in its own right.
