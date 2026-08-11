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

| Skill | What it does |
|---|---|
| [`repo-orientation`](skills/repo-orientation/SKILL.md) | Maps a repository before consequential work begins — purpose, seams, where work belongs, honest unknowns — and stops there rather than drifting into a plan or a critique. |
| [`slice-review`](skills/slice-review/SKILL.md) | Reviews one diff or PR against its stated goal and actual verification evidence, and returns exactly one verdict instead of a reflexive "looks good." |
| [`slice-retro`](skills/slice-retro/SKILL.md) | Writes a retrospective for one completed slice, keeping what was actually proven separate from inference and speculation. |
| [`next-best-slice`](skills/next-best-slice/SKILL.md) | Recommends exactly one next slice of work, justified by the last review and retro plus the product's current state — never a shortlist or a roadmap. |
| [`slice-plan`](skills/slice-plan/SKILL.md) | Turns an already-accepted slice into an implementation-ready plan — contract, seams, invariants, verification — without reopening what to build. |

These bracket an implementation loop rather than complete one: orient before
the work starts, then, once it's done, review it, retrospect on it, decide
what's next, plan the next slice. The actual implementing happens in between,
outside any of these. Nothing enforces the order — each skill stands on its
own and mostly refuses to do another's job even when asked.

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
