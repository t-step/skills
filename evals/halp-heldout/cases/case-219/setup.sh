#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# Node consumer built on an ordering assumption that the queue notes contradict
new_repo "$out"
put package.json <<'J'
{ "name": "balance-consumer", "scripts": { "test": "vitest run" } }
J
put docs/PLAN.md <<'J'
# Plan: balance consumer

Assumptions
- A4: The queue delivers messages for an account in order, so each message can simply overwrite the account state.

Tasks
- [x] 1. Message parser (`src/parse.ts`)
- [x] 2. Backoff helper for reconnects (`src/backoff.ts`)
- [x] 3. Metrics counters (`src/metrics.ts`)
- [ ] 4. State applier (`src/apply.ts`)
J
put docs/queue-notes.md <<'J'
# Queue notes
- Delivery is at-least-once. After a retry, messages for one account can arrive out of order.
- Each message carries a monotonically increasing `seq` per account.
J
put src/parse.ts <<'J'
export type Msg = { account: string; seq: number; balance: number };
export const parse = (raw: string): Msg => JSON.parse(raw) as Msg;
J
put src/backoff.ts <<'J'
export const backoffMs = (attempt: number) => Math.min(30000, 250 * 2 ** attempt);
J
put src/metrics.ts <<'J'
export const counters = { received: 0, applied: 0 };
J
commit_all "consumer: parser, backoff, metrics" "2026-09-12T10:00:00"
put src/apply.ts <<'J'
import type { Msg } from "./parse";
export type State = { seq: number; balance: number };
export function apply(state: State, msg: Msg): State {
  return { seq: msg.seq, balance: msg.balance };
}
J
put src/apply.test.ts <<'J'
import { expect, it } from "vitest";
import { apply } from "./apply";
it("ends at the highest seq even if delivery is out of order", () => {
  const order = [1, 3, 2].map((seq) => ({ account: "a", seq, balance: seq === 3 ? 70 : 100 }));
  const end = order.reduce(apply, { seq: 0, balance: 0 });
  expect(end).toEqual({ seq: 3, balance: 70 });
});
J
