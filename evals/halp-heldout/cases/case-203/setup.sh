#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# pnpm monorepo; scoped AGENTS.md; no task artifacts; changes span two packages
new_repo "$out"
put pnpm-workspace.yaml <<'J'
packages:
  - "packages/*"
J
put package.json <<'J'
{ "name": "shop-tools", "private": true, "scripts": { "test": "pnpm -r test" } }
J
put AGENTS.md <<'J'
# AGENTS
- Packages: `core` (pure logic), `cli` and `web` (consumers of core). Run `pnpm -r test` before committing.
J
put packages/web/AGENTS.md <<'J'
# web
- Import only from `@shop/core` public exports. Snapshot tests live in `src/__snapshots__/`.
J
put packages/core/package.json <<'J'
{ "name": "@shop/core", "version": "0.3.0", "main": "src/index.ts", "scripts": { "test": "vitest run" } }
J
put packages/core/src/index.ts <<'J'
export { toCents, formatMoney } from "./money";
J
put packages/core/src/money.ts <<'J'
export function toCents(amount: number): number { return Math.round(amount * 100); }
export function formatMoney(cents: number): string { return `$${(cents / 100).toFixed(2)}`; }
J
put packages/cli/package.json <<'J'
{ "name": "@shop/cli", "version": "0.3.0", "dependencies": { "@shop/core": "workspace:*" }, "scripts": { "test": "vitest run" } }
J
put packages/cli/src/format.ts <<'J'
import { formatMoney } from "@shop/core";
export const line = (name: string, cents: number) => `${name.padEnd(20)}${formatMoney(cents)}`;
J
put packages/web/package.json <<'J'
{ "name": "@shop/web", "version": "0.3.0", "dependencies": { "@shop/core": "workspace:*" }, "scripts": { "test": "vitest run" } }
J
put packages/web/src/Price.tsx <<'J'
import { formatMoney } from "@shop/core";
export const Price = ({ cents }: { cents: number }) => <span>{formatMoney(cents)}</span>;
J
commit_all "Initial monorepo layout" "2026-09-07T09:00:00"
git checkout -q -b feat/money-rounding
put packages/core/src/money.ts <<'J'
export function toCents(amount: number): number { return Math.round(amount * 100); }
export function roundHalfEven(x: number): number { const f = Math.floor(x), d = x - f; return d > 0.5 ? f + 1 : d < 0.5 ? f : f % 2 === 0 ? f : f + 1; }
export function formatMoney(cents: number): string { return `$${(cents / 100).toFixed(2)}`; }
J
commit_all "core: add roundHalfEven helper" "2026-09-14T10:00:00"
put packages/core/src/money.ts <<'J'
export function roundHalfEven(x: number): number { const f = Math.floor(x), d = x - f; return d > 0.5 ? f + 1 : d < 0.5 ? f : f % 2 === 0 ? f : f + 1; }
export function toCents(amount: number): number { return roundHalfEven(amount * 100); }
export function formatMoney(cents: number): string { return `$${(cents / 100).toFixed(2)}`; }
J
commit_all "core: use roundHalfEven in toCents" "2026-09-15T16:00:00"
# working tree: formatMoney gains a required argument in core; cli adapted; web untouched
put packages/core/src/money.ts <<'J'
export function roundHalfEven(x: number): number { const f = Math.floor(x), d = x - f; return d > 0.5 ? f + 1 : d < 0.5 ? f : f % 2 === 0 ? f : f + 1; }
export function toCents(amount: number): number { return roundHalfEven(amount * 100); }
export function formatMoney(cents: number, currency: string): string { return `${currency} ${(cents / 100).toFixed(2)}`; }
J
put packages/cli/src/format.ts <<'J'
import { formatMoney } from "@shop/core";
export const line = (name: string, cents: number) => `${name.padEnd(20)}${formatMoney(cents, "USD")}`;
J
