#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# TypeScript storefront; Markdown checklist plan; feature branch with WIP
new_repo "$out"
put package.json <<'J'
{ "name": "storefront", "private": true, "scripts": { "test": "vitest run", "build": "tsc -b && vite build" },
  "dependencies": { "react": "^18.3.0" }, "devDependencies": { "typescript": "^5.5.0", "vitest": "^2.0.0" } }
J
put src/App.tsx <<'J'
export function App() { return <main>storefront</main>; }
J
commit_all "Scaffold storefront (Vite + React + TS)" "2026-09-08T09:00:00"
put docs/PLAN.md <<'J'
# Plan: coupon support

- [ ] 1. `Coupon` type and code parser (`src/features/cart/coupon.ts`)
- [ ] 2. Percent coupons in `totals()`
- [ ] 3. Fixed-amount coupons (cents) in `totals()`
- [ ] 4. Coupon line in `CartSummary`
- [ ] 5. Reject expired coupons. Open: does "expired" use UTC or the store's timezone? Waiting on product.
J
commit_all "docs: plan for coupon support" "2026-09-09T10:00:00"
git checkout -q -b feat/coupons
put src/features/cart/coupon.ts <<'J'
export type Coupon = { kind: "percent"; value: number } | { kind: "fixed"; cents: number };
export function parseCoupon(code: string): Coupon | null {
  const m = /^(PCT|FIX)-(\d+)$/.exec(code);
  if (!m) return null;
  return m[1] === "PCT" ? { kind: "percent", value: Number(m[2]) } : { kind: "fixed", cents: Number(m[2]) };
}
J
sed -i.bak 's/- \[ \] 1\./- [x] 1./' docs/PLAN.md && rm docs/PLAN.md.bak
commit_all "cart: Coupon type and parser (plan step 1)" "2026-09-11T11:00:00"
put src/features/cart/cartStore.ts <<'J'
import type { Coupon } from "./coupon";
export type Item = { sku: string; cents: number; qty: number };
export function subtotal(items: Item[]): number { return items.reduce((s, i) => s + i.cents * i.qty, 0); }
export function totals(items: Item[], coupon?: Coupon) {
  const sub = subtotal(items);
  if (coupon?.kind === "percent") return { subtotal: sub, total: sub - Math.floor((sub * coupon.value) / 100) };
  return { subtotal: sub, total: sub };
}
J
put src/features/cart/cart.test.ts <<'J'
import { describe, expect, it } from "vitest";
import { totals } from "./cartStore";
const items = [{ sku: "a", cents: 1000, qty: 2 }];
describe("totals", () => {
  it("sums line items", () => expect(totals(items).total).toBe(2000));
  it("applies percent coupons", () => expect(totals(items, { kind: "percent", value: 10 }).total).toBe(1800));
  it("rounds percent discounts down", () => expect(totals([{ sku: "a", cents: 999, qty: 1 }], { kind: "percent", value: 10 }).total).toBe(900));
});
J
sed -i.bak 's/- \[ \] 2\./- [x] 2./' docs/PLAN.md && rm docs/PLAN.md.bak
commit_all "cart: percent coupons in totals (plan step 2)" "2026-09-12T15:30:00"
# working tree: fixed-coupon stub + new failing test + an unexplained package.json edit
put src/features/cart/cartStore.ts <<'J'
import type { Coupon } from "./coupon";
export type Item = { sku: string; cents: number; qty: number };
export function subtotal(items: Item[]): number { return items.reduce((s, i) => s + i.cents * i.qty, 0); }
export function totals(items: Item[], coupon?: Coupon) {
  const sub = subtotal(items);
  if (coupon?.kind === "percent") return { subtotal: sub, total: sub - Math.floor((sub * coupon.value) / 100) };
  if (coupon?.kind === "fixed") throw new Error("fixed coupons: not implemented");
  return { subtotal: sub, total: sub };
}
J
cat >> src/features/cart/cart.test.ts <<'J'
describe("fixed coupons", () => {
  it("applies fixed coupon in cents", () => expect(totals(items, { kind: "fixed", cents: 500 }).total).toBe(1500));
});
J
sed -i.bak 's/"typescript": "^5.5.0",/"prettier": "^3.3.0", "typescript": "^5.5.0",/' package.json && rm package.json.bak
