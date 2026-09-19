#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# plan: TanStack Query; repo already standardizes on it (ADR-003) and the plan needs caching and invalidation
new_repo "$out"
put package.json <<'J'
{ "name": "recipes-app", "dependencies": { "@tanstack/react-query": "^5.0.0", "react": "^18.3.0" } }
J
put docs/adr/ADR-003-server-state.md <<'J'
# ADR-003: Server state
Status: accepted. Server state uses TanStack Query. Do not hand-roll fetch effects.
J
for pair in favorites:Favorites tags:Tags users:Users search:Search; do
f="${pair%%:*}"; F="${pair##*:}"
put "src/features/$f/use$F.ts" <<J
import { useQuery } from "@tanstack/react-query";
export const use$F = () => useQuery({ queryKey: ["$f"], queryFn: () => fetch("/$f").then((r) => r.json()) });
J
done
put docs/PLAN.md <<'J'
# Plan: recipes list

Approach: TanStack Query for the recipes list (`useQuery`), invalidating after a recipe is created.

- [ ] 1. Mount `QueryClientProvider`
- [ ] 2. `useRecipes` via `useQuery`
- [ ] 3. Invalidate the list after `createRecipe` succeeds
- [ ] 4. Loading and error states
J
put src/main.tsx <<'J'
export const boot = () => "app";
J
commit_all "recipes-app: baseline, ADR-003, plan" "2026-09-11T10:00:00"
git checkout -q -b feat/recipes-list
put src/features/recipes/useRecipes.ts <<'J'
import { useQuery } from "@tanstack/react-query";
export const useRecipes = () => useQuery({ queryKey: ["recipes"], queryFn: () => fetch("/recipes").then((r) => r.json()) });
J
sed -i.bak 's/- \[ \] 1\./- [x] 1./; s/- \[ \] 2\./- [x] 2./' docs/PLAN.md && rm docs/PLAN.md.bak
commit_all "recipes: useRecipes via useQuery (plan steps 1-2)" "2026-09-15T10:00:00"
