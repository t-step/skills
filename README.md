# skills

A collection of small, portable Agent Skills for recurring software-development
work: orienting in an unfamiliar repo, reviewing a finished change, writing a
retrospective, picking the next slice, planning how to build it. Each skill is
self-contained — `SKILL.md` plus supporting files — and meant to be handed to
a coding agent alongside a task.

They narrow specific failure modes — reading the actual diff instead of
trusting the summary, keeping observed fact separate from inference — rather
than replace judgment about the situation in front of you.

**[SKILLS.md](SKILLS.md)** has the full list, generated from each skill's own
frontmatter.

## Using a skill

There's no install step, package, or registry — this is source. Each skill
is a directory under `skills/` with a `SKILL.md` written in the Agent Skills
format. To use one, expose `skills/*/SKILL.md` to a compatible agent harness
(copy, symlink, or otherwise make it visible where the harness looks) and let
it trigger from the description, or invoke it explicitly.

## Development

An *observed* failure can motivate a `SKILL.md` change; a *suspected* one
gets an eval case first, not a prompt edit on a hunch. Each skill's
`evals/<name>/` holds fixture cases (`cases/`) with isolated answer keys
(`grading/`, kept separate so grading can't leak into the input — enforced by
`scripts/check-eval-isolation.py`) and a `RESULTS.md` recording actual runs,
disagreements included rather than smoothed over. A new skill starts with a
handful of fixtures, not a mature suite — see `evals/eval-runner-demo/` for
how that works mechanically, and `AGENTS.md` for the write-up and
verification rules these are held to.
