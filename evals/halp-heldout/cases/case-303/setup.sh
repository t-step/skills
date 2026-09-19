#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# monorepo; plan: hand-written validation in web. core already has shared schemas, and web's rules have drifted from them.
new_repo "$out"
put pnpm-workspace.yaml <<'J'
packages:
  - "packages/*"
J
put package.json <<'J'
{ "name": "acct", "private": true }
J
put packages/core/package.json <<'J'
{ "name": "@acct/core", "main": "src/index.ts", "dependencies": { "zod": "^3.23.0" } }
J
put packages/core/src/index.ts <<'J'
export { UserSchema } from "./schemas/user";
J
put packages/core/src/schemas/user.ts <<'J'
import { z } from "zod";
export const UserSchema = z.object({ email: z.string().email(), password: z.string().min(12), phone: z.string().regex(/^\+\d{8,15}$/).optional() });
J
put packages/cli/package.json <<'J'
{ "name": "@acct/cli", "dependencies": { "@acct/core": "workspace:*" } }
J
put packages/cli/src/import.ts <<'J'
import { UserSchema } from "@acct/core";
export const parseUser = (row: unknown) => UserSchema.parse(row);
J
put packages/api/package.json <<'J'
{ "name": "@acct/api", "dependencies": { "@acct/core": "workspace:*" } }
J
put packages/api/src/signup.ts <<'J'
import { UserSchema } from "@acct/core";
export const validateSignup = (body: unknown) => UserSchema.safeParse(body);
J
put packages/web/package.json <<'J'
{ "name": "@acct/web", "dependencies": { "react": "^18.3.0" } }
J
put packages/web/src/SignupForm.tsx <<'J'
export function validate(v: { email: string; password: string }) {
  const errors: string[] = [];
  if (!v.email.includes("@")) errors.push("email");
  if (v.password.length < 8) errors.push("password");
  return errors;
}
J
put docs/PLAN.md <<'J'
# Plan: signup validation

Approach: hand-written checks in `packages/web/src/SignupForm.tsx`.

- [x] 1. Email check in the form
- [x] 2. Password length check in the form
- [ ] 3. Phone number check in the form
- [ ] 4. Inline error messages
J
commit_all "acct: monorepo, signup form with basic validation" "2026-09-12T10:00:00"
git checkout -q -b feat/signup-validation
