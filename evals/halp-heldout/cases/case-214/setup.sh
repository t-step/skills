#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# TS inbox UI built on a pagination assumption the recorded API sample contradicts
new_repo "$out"
put package.json <<'J'
{ "name": "inbox-ui", "scripts": { "test": "vitest run" } }
J
put docs/PLAN.md <<'J'
# Plan: infinite-scroll inbox

Assumptions
- A1: `GET /messages` is cursor-paginated: each page has `items` and `nextCursor` (null on the last page).

Tasks
- [x] 1. `Message` and `Page` types
- [x] 2. `MessageList` component (renders a list of messages)
- [x] 3. `formatDate` helper
- [ ] 4. `fetchMessages(cursor)` client and `useMessages` hook that loads all pages
J
put src/types.ts <<'J'
export type Message = { id: string; subject: string; sentAt: string };
export type Page = { items: Message[]; nextCursor: string | null };
J
put src/lib/formatDate.ts <<'J'
export const formatDate = (iso: string) => new Date(iso).toISOString().slice(0, 10);
J
put src/components/MessageList.tsx <<'J'
import type { Message } from "../types";
import { formatDate } from "../lib/formatDate";
export const MessageList = ({ messages }: { messages: Message[] }) => (
  <ul>{messages.map((m) => <li key={m.id}>{m.subject} ({formatDate(m.sentAt)})</li>)}</ul>
);
J
put fixtures/messages.sample.json <<'J'
{ "items": [ { "id": "m1", "subject": "Hello", "sentAt": "2026-09-01T10:00:00Z" }, { "id": "m2", "subject": "Invoice", "sentAt": "2026-09-02T10:00:00Z" } ],
  "offset": 0, "limit": 2, "total": 143 }
J
commit_all "inbox-ui: types, MessageList, formatDate" "2026-09-14T10:00:00"
put src/api/messages.ts <<'J'
import type { Page } from "../types";
export async function fetchMessages(cursor?: string, fetcher: (u: string) => Promise<any> = (u) => fetch(u).then((r) => r.json())): Promise<Page> {
  const json = await fetcher(`/messages${cursor ? `?cursor=${cursor}` : ""}`);
  return { items: json.items, nextCursor: json.nextCursor };
}
J
put src/hooks/useMessages.ts <<'J'
import { fetchMessages } from "../api/messages";
import type { Message } from "../types";
export async function loadAll(fetcher?: (u: string) => Promise<any>): Promise<Message[]> {
  const all: Message[] = [];
  let cursor: string | null | undefined = undefined;
  while (cursor !== null) {
    const page = await fetchMessages(cursor, fetcher);
    all.push(...page.items);
    cursor = page.nextCursor;
  }
  return all;
}
J
put src/hooks/useMessages.test.ts <<'J'
import { expect, it } from "vitest";
import sample from "../../fixtures/messages.sample.json";
import { loadAll } from "./useMessages";
it("loads all pages", async () => { expect((await loadAll(async () => sample)).length).toBeGreaterThan(0); });
J
