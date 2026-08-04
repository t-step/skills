# AGENTS

- This is an npm-workspaces monorepo. Run commands from the repo root via
  `npm run <task>` (delegates to Turborepo), not inside individual package
  directories.
- Shared code goes in `packages/`. Application code goes in `apps/`.
  Packages must never import from `apps/`.
