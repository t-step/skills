# Simulated projectmem search output

## Search: "agent identity" / "agent-to-agent" / "delegation" / "authentication"

**Project: Valence** (cross-project)
> decision (2026-08-03): configured Auth.js v5 with a GitHub OAuth
> provider and JWT sessions for human contributor sign-in, with
> `attachGithubIdentity`/`exposeGithubIdentity` exported for unit testing.
> This is about verifying a human user's identity when they sign in to a
> web app — there is no autonomous agent, no agent-to-agent delegation,
> and no service-to-service call involved anywhere in this decision.

**Other projects** — no matches.

## Search: "model provenance" / "training data lineage" / "weight attestation"

**Project: bindle** (cross-project)
> note: the repo's CI pipeline runs a software dependency supply-chain
> scan (`pip-audit`/`npm audit`-style tooling) against its own installed
> packages before each release, to catch known-vulnerable dependency
> versions. This is about vulnerability scanning of ordinary software
> package dependencies — it has nothing to do with AI model weights,
> training-data lineage, or fine-tuning history.

**Other projects** — no matches.
