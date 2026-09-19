#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# GitHub-looking origin; branch pushed and in sync; a stubbed `gh` reports an open PR with changes requested
new_repo "$out"
put package.json <<'J'
{ "name": "notes-api", "scripts": { "test": "vitest run" } }
J
put src/server.ts <<'J'
export function start() { return "listening"; }
J
commit_all "Initial notes-api" "2026-09-08T09:00:00"
git checkout -q -b feat/rate-limit
put src/rateLimit.ts <<'J'
const hits = new Map<string, number>();
export function allow(ip: string, limit = 100): boolean { const n = (hits.get(ip) ?? 0) + 1; hits.set(ip, n); return n <= limit; }
J
commit_all "add in-memory rate limiter" "2026-09-12T10:00:00"
put src/server.ts <<'J'
import { allow } from "./rateLimit";
export function start() { return allow("0.0.0.0") ? "listening" : "limited"; }
J
commit_all "wire rate limiter into server" "2026-09-12T14:00:00"
make_origin "git@github.com:acme/notes-api.git" main feat/rate-limit
git branch -q -u origin/feat/rate-limit
gh_shim "$out" open
