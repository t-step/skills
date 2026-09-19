#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# a test log that is OLDER than the latest code changes (one committed, one uncommitted)
new_repo "$out"
put package.json <<'J'
{ "name": "slugify-ts", "scripts": { "test": "vitest run", "lint": "eslint src" } }
J
put src/slug.ts <<'J'
export const slugify = (s: string) => s.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-");
J
put src/slug.test.ts <<'J'
import { expect, it } from "vitest";
import { slugify } from "./slug";
it("lowercases", () => expect(slugify("Hello World")).toBe("hello-world"));
J
commit_all "slugify: initial" "2026-09-08T09:00:00"
put src/slug.ts <<'J'
export const slugify = (s: string) => s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase().trim().replace(/[^a-z0-9]+/g, "-");
J
commit_all "slugify: strip diacritics" "2026-09-14T14:00:00"
sync_mtimes
put src/slug.ts <<'J'
export const slugify = (s: string) => s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
J
mkdir -p logs
put logs/test.log <<'J'
 RUN  v2.0.5 /work/slugify-ts

 ✓ src/slug.test.ts (12)
   ✓ lowercases

 Test Files  1 passed (1)
      Tests  12 passed (12)
   Start at  10:00:01
   Duration  412ms
J
stamp 202609170900 src/slug.ts
stamp 202609101000 logs/test.log
