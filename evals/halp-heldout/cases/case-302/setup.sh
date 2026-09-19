#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# plan: client-side pagination. Alternative (server-side) is viable but the evidence does not clearly favor it.
new_repo "$out"
put package.json <<'J'
{ "name": "admin-dashboard", "scripts": { "test": "vitest run" } }
J
put docs/api.md <<'J'
# API notes
- `GET /users` supports `?limit=&offset=` (default limit 1000) and returns `{ items, total }`.
- Sales notes: typical org has 300-900 users; the largest customer has about 12,000.
J
put docs/PLAN.md <<'J'
# Plan: users table

Approach: load all users once (`GET /users`) and sort/paginate on the client.

- [ ] 1. `useUsers` hook that fetches all users
- [ ] 2. `UsersTable` renders rows
- [ ] 3. Sort by column (client-side)
- [ ] 4. Page controls (client-side slicing, 25 per page)
J
put src/hooks/useUsers.ts <<'J'
export async function fetchAllUsers(fetcher: (u: string) => Promise<any>) { return (await fetcher("/users")).items; }
J
put src/components/UsersTable.tsx <<'J'
export const UsersTable = ({ users }: { users: { id: string; name: string }[] }) => (
  <table><tbody>{users.map((u) => <tr key={u.id}><td>{u.name}</td></tr>)}</tbody></table>
);
J
commit_all "admin-dashboard: users hook, table, plan" "2026-09-11T10:00:00"
git checkout -q -b feat/users-table
sed -i.bak 's/- \[ \] 1\./- [x] 1./; s/- \[ \] 2\./- [x] 2./' docs/PLAN.md && rm docs/PLAN.md.bak
commit_all "users table: plan steps 1-2 done" "2026-09-14T09:00:00"
