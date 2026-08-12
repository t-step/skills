---
name: ship-slice
description: >-
  Ships one finished slice: discovers the repo's own complete
  verification gate (Makefile/package.json/pyproject targets, CI
  workflows, AGENTS.md/CLAUDE.md), runs it fully, commits only if it
  passes, tags via the repo's existing tag scheme (confirmed with the
  user, never invented), and pushes commit and tag to the repo's real
  working branch. Generic -- discovers each repo's own conventions, never
  assumes targets, tag format, or branch flow. Use when a slice is
  finished and ready to commit, tag, and push, or asked to "ship this",
  "wrap up this slice", or "run the checks and commit". Invoking it is
  explicit approval to commit and push, conditional on the gate passing
  and the tree holding only this slice's changes. Refuses -- even under
  "just ship it", time pressure, or a flaky-looking failure -- to commit
  past a failing or ambiguous gate, silently include/exclude unrelated
  dirty files, invent a tag name or scheme, or push anywhere but the
  repo's own working branch.
---

# Ship Slice

The ritual at the end of a finished slice is always the same shape: run
the checks, commit, tag, push. Typed out by hand each time, it's also the
moment most likely to get shortened under pressure -- a check skipped
because it "probably still passes," a stray file committed because
untangling it felt slower than shipping, a tag name guessed instead of
checked. This skill exists to run that ritual completely, in the same
order, every time, and to stop rather than guess at any step where
guessing would matter.

It ships one slice already finished. It does not decide whether the slice
is any good -- that's slice-review's job -- and it does not pick or plan
what comes next.

## Discover the gate before running anything

The gate is the complete set of checks this repository itself declares --
not the subset that seems relevant, not "the tests." Find it by reading,
in whatever combination the repository actually has:

- Makefile (or justfile, Taskfile, etc.) targets that look like
  verification -- `test`, `lint`, `typecheck`, `build`, `check`, a
  combined target that chains several.
- `package.json` scripts (`test`, `lint`, `typecheck`, `build`) and any
  script one of those calls in turn.
- `pyproject.toml` / tool config (`pytest`, `ruff`, `mypy`, `tox`, `nox`)
  and any wrapper script that runs them together.
- CI workflow files (`.github/workflows/*.yml` or equivalent) -- these
  often name the authoritative gate explicitly, especially in a repo
  whose own instructions say CI is a backstop and local verification is
  canonical.
- AGENTS.md / CLAUDE.md / CONTRIBUTING, which may name a single canonical
  check command (a `check.sh`, a `make verify`) that wraps everything
  else -- prefer that single entry point over reconstructing the gate
  from its parts if one exists and looks current against what actually
  runs in CI.

Cross-check these sources against each other. A canonical script that
hasn't been touched in a long time while CI grew a new job is a sign the
gate has drifted; a Makefile target nothing else references might be
stale. When they agree, the gate is whatever they agree on. When they
don't, or when nothing in the repository names a complete gate at all,
that's not a green light to assemble a plausible-looking subset -- **stop
and say exactly what's ambiguous**: which sources disagree, what's
missing, or what a partial gate would leave unchecked. A guessed gate
that happens to pass is not verification; it's a coin flip that looks
like one.

## Run the gate, then look at what actually happened

Run every command the gate comprises, in full. For each one:

- **Pass** -- move on.
- **Fail** -- stop. No commit, no partial ship, regardless of how small
  or unrelated the failure looks. Report the failing command and its
  actual output, not a paraphrase of it.
- **Flaky-looking** -- a failure that seems unrelated to anything in the
  slice is a reason to look closer, not a reason to re-run until it goes
  green. Read the failure, form a hypothesis for why it might be
  order-dependent, environment-dependent, or genuinely unrelated pre-existing
  breakage, and say what you found. Re-running blind and reporting
  whichever result came back green is the exact failure mode this section
  exists to prevent.

A gate that was only partially run is not a passed gate. If time or
access prevents running part of it, that's the same as a failure for
shipping purposes: stop and say which part didn't run and why.

## The tree gets the same scrutiny as the gate

Before committing, look at what's actually about to be committed, not
what you expect to be there:

- `git status` for untracked and staged files.
- `git diff --stat` for the shape of what changed.

Anything staged or dirty that doesn't obviously belong to this slice --
an unrelated file left over from earlier exploration, a config edit that
was never part of the task, a generated artifact that shouldn't be
tracked -- gets named to the user before committing. Don't silently fold
it in because it's easier than asking, and don't silently drop it either
without saying so; both are quiet decisions about someone else's files
that aren't this skill's to make alone.

## Commit

Write a Conventional Commits message describing the slice's purpose --
what it does and why, not an inventory of the files it touched.
`Co-Authored-By` trailers are fine. A `Claude-Session:` trailer, a
claude.ai session URL, or a local absolute filesystem path never belongs
in a commit message -- strip them if a template or habit would otherwise
add one.

## Tag

Look at the repository's actual tag history (`git tag --list` or
equivalent) for an existing scheme -- a pattern like `slice-04-complete`,
`v0.3.0`, or whatever this specific repository already uses. Infer the
next value in that sequence, then **confirm the exact tag name with the
user before creating it**. Never create the tag on inferred confirmation
or skip the confirmation because the next value seemed obvious.

If the repository has no existing tag scheme at all, don't invent one
because the ritual expects a tag. Ask the user whether this slice should
be tagged and, if so, what scheme to start.

## Push

Determine the repository's actual working-branch flow before pushing --
a `development`-then-PR flow, direct pushes to `main`, or something else
entirely, as evidenced by branch protection, existing PR history, or the
repository's own instructions. Push the commit and tag to that branch.
Pushing straight to `main` when the repo's own flow says otherwise is not
a shortcut this skill takes even when it would be faster.

## What invoking this skill authorizes, and what it doesn't

Being asked to run ship-slice is the user's explicit, standing approval
to commit and push -- that authorization does not need to be re-asked for
on every run. But it is conditional, not unconditional: it authorizes
committing and pushing *a gate that actually passed* and *a tree that
holds only this slice's changes*. It does not authorize committing past a
failing check, silently resolving an unrelated dirty file either way, or
skipping the tag-name confirmation. None of the refusal points above are
overridden by the invocation itself, and none of them are overridden by
"just ship it," a deadline, a claim that the failure is "probably
unrelated," or a request to skip a step to save time. If the gate fails
or the tree is unclear, the correct outcome of being asked to ship is a
clear report of why nothing shipped -- not a best-effort partial ship.

## Report

End every run, whether it shipped or stopped, with exactly this block:

```
=== DONE ===
Asked: <what was requested, one line>
Artifacts: <files/commits/tags touched or proposed, or "None -- shipping halted before any were created">
Checks:
- <gate command 1>: pass/fail
- <gate command 2>: pass/fail
  (one line per command the discovered gate comprises)
Shipped: <commit SHA, tag name, and push status if shipped; "Not shipped -- <reason>" if not>
Open: <anything unresolved -- an unconfirmed tag name, a flagged unrelated file, an ambiguous gate -- or "None.">
```

Leave `Checks` listing the actual commands run, in the order run, even on
a stop -- a report that lists commands without their real output, or
skips straight to a verdict, is the same premature confidence this skill
exists to avoid.
