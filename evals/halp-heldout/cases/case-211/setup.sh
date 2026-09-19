#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# uncommitted edit and an untracked test-output file with the SAME minute-level mtime; no timestamps inside the file
new_repo "$out"
put package.json <<'J'
{ "name": "pricing-utils", "scripts": { "test": "vitest run" } }
J
put src/price.ts <<'J'
export const round = (x: number) => Math.round(x * 100) / 100;
J
put src/price.test.ts <<'J'
import { expect, it } from "vitest";
import { round } from "./price";
it("rounds half up", () => expect(round(1.005)).toBe(1.01));
J
commit_all "pricing-utils: round helper" "2026-09-12T09:00:00"
sync_mtimes
put src/price.ts <<'J'
export const round = (x: number) => Math.round((x + Number.EPSILON) * 100) / 100;
J
put test-output.txt <<'J'
 FAIL  src/price.test.ts > rounds half up
AssertionError: expected 1 to be 1.01

 Test Files  1 failed (1)
      Tests  1 failed | 8 passed (9)
J
stamp 202609161405 src/price.ts test-output.txt
