# design-system-calibration — experiment setup

Status: **pre-skill**. `skills/design-system-calibration/` does not exist
yet. This directory records only the fixtures, authority snapshot, and
observations needed to make the next session reproducible — no skill
content, no recommendations, no expected findings, no golden answers.

The experiment: whether an agent can inspect an unfamiliar frontend and,
using authoritative Cloudscape guidance, identify material
implementation-level opportunities to express that frontend more correctly
and idiomatically in Cloudscape. Cloudscape/AWS is the proving ground for a
more general design-system-calibration mechanism (a manually curated
calibration pack an FDE supplies); nothing here should hard-code a
Cloudscape URL or Cloudscape-specific path into future skill logic.

## Cloudscape authority snapshot

`authority/cloudscape-llms.txt` — see `authority/SOURCE.md` for full
provenance (fetched 2026-09-01, ETag `27d274e60f5f6aa9d8ab0e874ff7f6f5`).
Treat it as a discovery/index file (links + one-line descriptions), not
component documentation itself — the linked pages are the actual guidance.

## Fixture repositories

Cloned read-only, **outside this repo**, at:
`/Users/thomasestep/Developer/cloudscape-eval-fixtures/`

This path is a local sibling checkout, not tracked by this repo. Re-clone
at the pinned SHA below to reproduce; do not modify these checkouts.

| Repo | Pinned SHA | Frontend root | Cloudscape packages (declared) |
|---|---|---|---|
| [aws-samples/sample-bedrock-spend-budget-guardrails](https://github.com/aws-samples/sample-bedrock-spend-budget-guardrails) | `588b62598a842896583d1ef516ae38597e00dc4e` | `web/` | `@cloudscape-design/components@^3.0.1340` (locked `3.0.1340`), `collection-hooks@^1.0.55`, `global-styles@^1.0.45` |
| [aws-samples/sample-knowledge-acquisition-skill](https://github.com/aws-samples/sample-knowledge-acquisition-skill) | `c3fa938d6c9f98973e64269e02d406c1017af628` | `webapp/` | `@cloudscape-design/components@^3.0.0` (locked `3.0.1326`), `board-components@^3.0.0` (locked `3.0.202`), `collection-hooks@^1.0.0` (locked `1.0.101`), `global-styles@^1.0.0` (locked `1.0.62`) |
| [aws-samples/webapp-form-builder](https://github.com/aws-samples/webapp-form-builder) | `15ab594c930c536ed7097de3221876cab5f7a489` | repo root | `@cloudscape-design/components@^3.0.693` (no lockfile committed — range only, not resolved), `global-styles@^1.0.31` |

All three repos are single-frontend (no monorepo/workspace split) once you
account for `sample-bedrock-spend-budget-guardrails`, which is a CDK app
with `web/` as its one browser frontend alongside `infra/` and `lambda/`.

### Reclone commands

```
git clone https://github.com/aws-samples/sample-bedrock-spend-budget-guardrails.git
git -C sample-bedrock-spend-budget-guardrails checkout 588b62598a842896583d1ef516ae38597e00dc4e

git clone https://github.com/aws-samples/sample-knowledge-acquisition-skill.git
git -C sample-knowledge-acquisition-skill checkout c3fa938d6c9f98973e64269e02d406c1017af628

git clone https://github.com/aws-samples/webapp-form-builder.git
git -C webapp-form-builder checkout 15ab594c930c536ed7097de3221876cab5f7a489
```

## Bounded surfaces identified per fixture

Identification only — no assessment of whether the Cloudscape usage on any
surface is good or bad. Line counts are the page component only, not its
full subtree.

### sample-bedrock-spend-budget-guardrails (`web/src/pages/`)

19 page components, `AdminBudgets.tsx` (818 loc) down to `MyActivity.tsx`
(68 loc). Shapes observed across the set: collection/resource pages backed
by `Table` + `useCollection` + `CollectionPreferences` (`Identities.tsx`,
`AdminUsers.tsx`, `AdminBudgets.tsx`), a dashboard (`SpendDashboard.tsx`),
a multi-step form flow (`Enrollment.tsx`), and a docs/reader page
(`Docs.tsx`).

### sample-knowledge-acquisition-skill (`webapp/src/pages/`)

11 page components; 4 are 12-line stub re-exports of a shared list-page
component (`ComparisonsPage.tsx`, `ConceptsPage.tsx`, `EntitiesPage.tsx`,
`QueriesPage.tsx`), so the real surface count is smaller than the file
count suggests. Shapes observed: a dashboard (`DashboardPage.tsx`), a
collection/list page (`KnowledgeListPage.tsx`), a detail page
(`DetailPage.tsx`, breadcrumbs + `ColumnLayout` + markdown body render),
and a navigation-heavy visualization page (`GraphPage.tsx`, Cloudscape
`Table`/`TextFilter`/`Pagination` around an embedded `react-force-graph-2d`
canvas).

### webapp-form-builder (`src/pages/`)

3 route-level pages (`home/Home.tsx`, `form/Form.tsx`,
`error/Error.tsx`), each a thin `AppLayout` shell around a `components/`
subtree. `form/Form.tsx` (36 loc) composes `AppLayout` +
`Breadcrumbs`/`Navigation` (custom wrappers) + `FormContent.tsx` (89 loc),
which drives a custom `FormBuilder`/`FormElement` abstraction over
Cloudscape form fields (`InputField`, `SelectField`, `DatePicker`,
`TilesSelect`, etc. under `src/forms/components/`). This is the whole
app's reason for existing — a config-driven form-builder demo — so the
"surface" and "the app" are nearly the same thing here.

## Selected surface per fixture (for variety)

| Fixture | Selected surface | UI shape |
|---|---|---|
| sample-bedrock-spend-budget-guardrails | `web/src/pages/Identities.tsx` (+ `components/Principal.tsx`, `components/PrincipalActivityModal.tsx` it composes) | Collection/resource page: table with filtering/preferences, row-level drill-in via modal |
| sample-knowledge-acquisition-skill | `webapp/src/pages/DetailPage.tsx` | Detail page: breadcrumbs, key-value layout, rendered document body |
| webapp-form-builder | `src/pages/form/Form.tsx` + `src/pages/form/components/FormContent.tsx` (+ `src/forms/`) | Form flow: multi-field form driven through a custom field-abstraction layer, with a help panel |

Rationale: this trio spans three distinct UI shapes (collection/resource,
detail, form flow) rather than three variations on the same shape, and each
selected surface is self-contained enough (under ~300 loc for its direct
page file, with a small, enumerable set of composed components) to be
reviewed from source in one pass. `Identities.tsx` was chosen over
`AdminBudgets.tsx`/`AdminUsers.tsx` in the same repo specifically for size
(290 loc vs. 818/644) while still exercising the same collection-page
component set (`Table`, `useCollection`, `CollectionPreferences`,
`Select`-based filtering). `DetailPage.tsx` was chosen over `GraphPage.tsx`
because the graph page's dominant surface area is a third-party canvas
library, not Cloudscape usage.

## Observations relevant to running/inspecting the fixtures

- None of the three fixtures were `npm install`ed or run — this setup is
  source-only inspection. Package manager: all three use `npm`
  (`package-lock.json` present for the first two; `webapp-form-builder` has
  no committed lockfile, so its Cloudscape version is a semver range, not a
  resolved version).
- `sample-bedrock-spend-budget-guardrails` is the largest/most
  infrastructure-heavy fixture (CDK + Lambda + web), but the frontend root
  (`web/`) is a normal standalone Vite React app independent of the
  `infra`/`lambda` trees — no need to touch those to review `web/`.
- `sample-knowledge-acquisition-skill` ships its own `SKILL.md` at the repo
  root (it *is* itself a published Claude/Codex skill for
  paper/knowledge acquisition, unrelated to Cloudscape). That file is
  irrelevant to this experiment and should not be confused with anything
  produced here.
- All three fixtures pull Cloudscape from npm at broadly current 3.0.x/1.0.x
  major versions (no pre-3.0 legacy component usage observed at the
  package.json level) — component-version drift relative to the current
  llms.txt snapshot is unlikely to be a major confound for this round, but
  it was not verified page-by-page.

---

## Material UI (MUI) round — generalization setup

Status: **pre-adaptation**. This round exists to answer one question,
later: does the reasoning *operation* that proved useful for Cloudscape
(`skills/cloudscape-native-expression-review/SKILL.md`) generalize to a
substantially different design system, given that system's own
authoritative documentation? This setup task deliberately did **not**
adapt the skill, run it, or write any expected findings for the MUI
fixtures below — see `MUI-CANDIDATE-POOL.md` and
`MUI-GENERALIZATION-NOTES.md` for the full reconnaissance and authority
comparison this round is based on.

**Authority boundary for this round**: Material UI (`@mui/material`)
documentation only, via `authority/mui-material-llms.txt` (see
`authority/SOURCE-MUI.md` for provenance — fetched 2026-09-02, ETag
`"d1e6e8e4e3010e2efcaa56ecceddeb20-ssl"`). Explicitly excluded from this
round's authority: MUI X, Joy UI, Base UI, Google Material Design / M3
guidance, and any third-party tutorial/blog material. Treat the llms.txt
snapshot strictly as a discovery index, same discipline as the Cloudscape
round — the linked pages, not the index's one-line descriptions, are the
actual guidance a future reviewer would selectively fetch.

### Fixture repositories

Cloned read-only, **outside this repo**, at:
`/Users/thomasestep/Developer/mui-eval-fixtures/`

Not tracked by this repo. Re-clone at the pinned SHA below to reproduce;
do not modify these checkouts. Full candidate-pool reconnaissance (11
repos investigated, why each was accepted or rejected on fixture-
suitability grounds only) is in `MUI-CANDIDATE-POOL.md`.

| Repo | Pinned SHA | Frontend root | Package manager | `@mui/material` (declared → locked) | MUI X involved? |
|---|---|---|---|---|---|
| [bluewave-labs/Checkmate](https://github.com/bluewave-labs/Checkmate) | `d347e29a286873541397fdcc4c79fa24cf0ee248` | `client/` (repo also has unrelated `server/`) | npm (`client/package-lock.json`) | `7.3.7` → `7.3.7` (pinned exact in `package.json` itself) | Declared elsewhere in the app (`@mui/x-charts@7.29.1`, `@mui/x-date-pickers@7.29.4`), **not imported** in the selected surface |
| [binwiederhier/ntfy](https://github.com/binwiederhier/ntfy) | `10cb6506f836dbb00bb77e3b52669f6ace37f555` | `web/` | npm (`web/package-lock.json`) | `^9.1.2` → `9.3.1` | No `@mui/x-*` dependency anywhere in `web/package.json` |
| [hkbus/hk-independent-bus-eta](https://github.com/hkbus/hk-independent-bus-eta) | `cb5b1fcbed5f9f7cb14635ee29507084b9de2578` | repo root (a `src-tauri/` desktop wrapper sits alongside it, untouched by the selected pages) | yarn (`yarn.lock`, **no `package-lock.json` in the tree** — see tooling note below) | `^5.15.11` → `5.15.11`, `"resolved": true` via `resolve_versions.py` (yarn.lock support added as the pre-freeze infrastructure correction — see `MUI-GENERALIZATION-NOTES.md`) | Declared elsewhere (`@mui/x-date-pickers@^6.5.0`), **not imported** in the selected surface |

Licenses: Checkmate AGPL-3.0, ntfy Apache-2.0, hk-independent-bus-eta
GPL-3.0 — all suitable for local, read-only evaluation use.

### Reclone commands

```
git clone https://github.com/bluewave-labs/Checkmate.git
git -C Checkmate checkout d347e29a286873541397fdcc4c79fa24cf0ee248

git clone https://github.com/binwiederhier/ntfy.git
git -C ntfy checkout 10cb6506f836dbb00bb77e3b52669f6ace37f555

git clone https://github.com/hkbus/hk-independent-bus-eta.git
git -C hk-independent-bus-eta checkout cb5b1fcbed5f9f7cb14635ee29507084b9de2578
```

### Selected surface per fixture (for shape diversity)

Identification only — no assessment of whether the MUI usage on any
surface is good or bad, and the native-expression skill was never run
against any of these surfaces.

| Fixture | UI shape | Selected surface | Composed files |
|---|---|---|---|
| Checkmate | Collection/management | `client/src/Pages/Incidents/index.tsx` | `Components/{CardDetails,CardSummary,ControlsIncidentFilter,DialogIncidentDetails,DialogResolution,IncidentTable}.tsx`, `utils.ts` — incident table with filtering controls, summary cards, and two dialogs (details, resolution) |
| ntfy | Form/workflow | `web/src/components/SubscribeDialog.jsx` (+ `PublishDialog.jsx` as a second, related form) | `ReserveTopicSelect.jsx`, `DialogFooter.jsx`, `AttachmentIcon.jsx`, `EmojiPicker.jsx` for structure; both dialogs also pull in app-service modules (`app/Api`, `app/SubscriptionManager`, `app/AccountApi`, `app/Session`, `app/Prefs`, etc.) that a future reviewer only needs to know exist, not read deeply |
| hk-independent-bus-eta | Detail/navigation/interaction | `src/pages/RouteEtaPage.tsx` (+ `StopEtaListPage.tsx`, `BookmarkedStopPage.tsx`) | `components/route-eta/{RouteHeader,StopAccordionList,StopDialog,RouteUpdateNotice}.tsx`, `context/AppContext`, `context/DbContext` — route search → per-stop ETA list → stop detail dialog, with bookmarking |

Rationale for shape diversity: a resource-table collection page
(Checkmate), a dialog-driven creation/configuration form pair (ntfy), and
a search → list → contextual-detail navigation flow
(hk-independent-bus-eta) are three structurally distinct interaction
shapes drawn from three fully independent, actively maintained real
products — not three surfaces of one repo, and not an official MUI
example standing in for an independent application.

### Observations relevant to running/inspecting the fixtures

- None of the three fixtures were `npm`/`yarn install`ed or run — source-
  only inspection, same discipline as the Cloudscape round.
- Package manager diversity was incidental, not sought: Checkmate and
  ntfy both use npm with committed lockfiles; hk-independent-bus-eta uses
  yarn with a committed `yarn.lock`. This exercised a real gap in
  `resolve_versions.py` (npm-only lockfile parsing) at setup time — see
  `MUI-GENERALIZATION-NOTES.md` for the full account. The script was not
  modified during this setup pass; it was given yarn.lock support as a
  small, targeted infrastructure fix immediately before the generalization
  round's freeze (`MUI-GENERALIZATION-NOTES.md`, "Post-setup correction").
- See `MUI-GENERALIZATION-NOTES.md` for how MUI's `llms.txt` structure
  differs from Cloudscape's (no explicit product-pattern section) and for
  the full deterministic-tooling compatibility results.
