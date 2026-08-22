# t-step Claude Code skills

A [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces) distributing Claude Code skills.

This is an early release, published to try out normal plugin distribution and release mechanics. Expect the published surface to grow slowly and deliberately.

## What's here

**`software-engineering`** (v0.1.2) — a plugin with four skills:

- **`next-best-slice`** — recommends exactly one next implementation slice once a completed slice has been reviewed and retrospected, weighing dependency unlocking, user value, learning value, size, reversibility, risk, and architectural momentum against the evidence — never a ranked shortlist or a roadmap.
- **`repo-orientation`** — builds a concise, evidence-backed operating map of a repository before consequential work begins: purpose, governing instructions, major execution paths, architectural seams, and honest unknowns.
- **`slice-plan`** — turns one already-accepted implementation slice into an implementation-ready plan: behavioral contract, likely implementation seams, invariants, a scoped verification strategy, explicit non-goals, and completion evidence — without redesigning or expanding the work.
- **`slice-review`** — reviews one bounded implementation slice (a diff, PR, or "done" claim) against its stated goal, repo instructions, the actual diff, and verification evidence, producing one of four verdicts.

## Add the marketplace

```
/plugin marketplace add t-step/skills
```

or from the CLI:

```
claude plugin marketplace add t-step/skills
```

## Install the plugin

```
/plugin install software-engineering@t-step-skills
```

or from the CLI:

```
claude plugin install software-engineering@t-step-skills
```

## Update

```
/plugin marketplace update t-step-skills
/plugin update software-engineering@t-step-skills
```

## Uninstall

```
/plugin uninstall software-engineering@t-step-skills
```

To also stop tracking the marketplace:

```
/plugin marketplace remove t-step-skills
```

## Stability expectations

This is a first release, published to learn the distribution mechanics rather than to promise a stable surface:

- Only four skills are published. Others exist in development and are promoted deliberately, one at a time, not automatically.
- Versioning and releases are manual — see [`.github/workflows/`](.github/workflows/) for what's automated (manifest validation and a version-bump check on pull requests, tagging and GitHub Releases on merge to `main`) and what isn't (choosing a version, writing release notes).
- Breaking changes to a skill's behavior are possible before `1.0.0`.

## Development

Skill development, evals, and internal tooling happen on the `development` branch, which is not distributed here. `main` only ever contains what's safe to install.
