# t-step Agent Skills

Source and distribution for t-step's [Agent Skills](https://code.claude.com/docs/en/skills), and a plugin marketplace that publishes a curated subset of them for [Claude Code](https://code.claude.com/docs/en/plugin-marketplaces) and [Codex](https://developers.openai.com/codex/plugins/build).

This is an early release, published to try out normal plugin distribution and release mechanics. Expect the published surface to grow slowly and deliberately.

## Repository layout

- **`skills/`** — canonical, editable source for every Agent Skill. Each `skills/<name>/SKILL.md` is authored and revised here first.
- **`evals/`** — development and evaluation evidence for the skills in `skills/` (cases, grading keys, run summaries, `RESULTS.md`), one directory per skill.
- **`plugins/software-engineering/`** — the curated, installable distribution. `plugins/software-engineering/skills/` holds published copies of the subset of canonical skills that have been deliberately released; `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` both read from it, so Claude Code and Codex install the exact same files. There is no separate Codex copy of a published skill to keep in sync.
- **`.claude-plugin/`** and **`.agents/plugins/`** — the marketplace manifests Claude Code and Codex use to discover the plugin, each pointing at `plugins/software-engineering`.

The plugin directory is a release artifact, not an independent implementation — it's a projection of whichever canonical skills we've chosen to publish, not a second place skills get written. Promotion from `skills/` into `plugins/software-engineering/skills/` is a deliberate, one-at-a-time act; not every skill under `skills/` is published, and a skill can exist in `skills/`/`evals/` for a while before (or without ever) making it into the plugin.

## Published plugin

**`software-engineering`** (v0.2.2) — a plugin with three published skills:

- **`repo-orientation`** — builds a concise, evidence-backed operating map of a repository before consequential work begins: purpose, governing instructions, major execution paths, architectural seams, and honest unknowns.
- **`slice-review`** — reviews one bounded implementation slice (a diff, PR, or "done" claim) against its stated goal, repo instructions, the actual diff, and verification evidence, producing one of four verdicts.
- **`task-composition`** — takes an already-decomposed spec or plan and composes its tasks into coherent, agent-sized execution groupings: vertical by default, a horizontal enabler only when it unlocks real parallel work, convergence points made explicit, and just enough dependency checking to catch cycles or misleading task order — never a priority call, a scheduler, or a durable task graph.

All three `SKILL.md` files use only `name` and `description` frontmatter (the portable Agent Skills subset), so they need no per-harness rewriting — the same three files are installed verbatim by either client.

## Claude Code

### Add the marketplace

```
/plugin marketplace add t-step/skills
```

or from the CLI:

```
claude plugin marketplace add t-step/skills
```

### Install the plugin

```
/plugin install software-engineering@t-step-skills
```

or from the CLI:

```
claude plugin install software-engineering@t-step-skills
```

### Update

```
/plugin marketplace update t-step-skills
/plugin update software-engineering@t-step-skills
```

### Uninstall

```
/plugin uninstall software-engineering@t-step-skills
```

To also stop tracking the marketplace:

```
/plugin marketplace remove t-step-skills
```

## Codex

Repo/team marketplace metadata for Codex lives at [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json), pointing at the same `plugins/software-engineering` directory Claude Code installs from.

### Add the marketplace

```
codex plugin marketplace add t-step/skills
```

### Install the plugin

```
codex plugin add software-engineering@t-step-skills
```

### Update

```
codex plugin marketplace upgrade t-step-skills
codex plugin add software-engineering@t-step-skills
```

### Uninstall

```
codex plugin remove software-engineering@t-step-skills
```

To also stop tracking the marketplace:

```
codex plugin marketplace remove t-step-skills
```

### What this is not (yet)

- **Not published to the public Plugin Directory.** This repository currently supports direct GitHub installation and repo/team marketplace distribution, the mechanisms that are actually configured here.
- **Not a separate skill implementation.** There is no `.agents/skills/` tree or second copy of any `SKILL.md` — Codex reads the same files Claude Code does, from the same plugin directory.

## Stability expectations

This is a first release, published to learn the distribution mechanics rather than to promise a stable surface:

- Only three skills are published. Others exist as canonical source under `skills/` and are promoted deliberately, one at a time, not automatically, into the shared `plugins/software-engineering/skills/` directory that both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` read from.
- Versioning and releases are manual — see [`.github/workflows/`](.github/workflows/) for what's automated (Claude plugin/marketplace manifest validation and a version-bump check on pull requests, tagging and GitHub Releases on merge to `main`) and what isn't (choosing a version, writing release notes). CI does not currently validate the Codex manifests; run `codex plugin marketplace add`/`plugin add` locally (as above) before relying on a change.
- `plugins/software-engineering/.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` are versioned together by convention — bump both to the same value when either changes.
- Breaking changes to a skill's behavior are possible before `1.0.0`.

## Skill development

Skills are authored and evaluated on `main`, under `skills/` and `evals/` — see [Repository layout](#repository-layout). That source tree is not itself installable; only what's explicitly promoted into `plugins/software-engineering/skills/` is distributed by the marketplace.
