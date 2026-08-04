# Expected orientation outcome (for grading, not shown to the agent under test)

**Scenario:** monorepo with two apps (`apps/web`, `apps/api`) and two shared
packages (`packages/core`, `packages/ui`), npm workspaces + Turborepo.

**Why:** The workspace manifest (`package.json` `workspaces` field) plus the
actual import statements (`apps/web/src/index.tsx` imports from
`@acme/ui`/`@acme/core`; `apps/api/src/server.ts` imports from `@acme/core`;
neither package imports from `apps/`) establish the dependency direction:
apps depend on packages, never the reverse. `AGENTS.md` states this
explicitly as a rule, but the orientation should ground the claim in the
imports/manifest, not just repeat the rule as an assertion. Commands come
from the root `package.json` scripts delegating to `turbo run <task>`.
