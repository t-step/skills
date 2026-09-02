# MUI generalization round — candidate-pool reconnaissance

Status: setup only, pre-skill-adaptation. This records fixture-suitability
reconnaissance for the Material UI generalization round of the
design-system-calibration experiment (see `SETUP.md`). Every note below is
about whether a repository is a *usable evaluation fixture* — recency,
scale, independence, MUI-vs-MUI-X composition, boundedness. None of it is
an assessment of whether any repository's MUI usage is good, idiomatic, or
correct; the whole point of this setup pass is to leave that question
untouched for the future generalization run.

Discovery method: `gh search repos` (topics `material-ui`/`mui`, sorted by
stars), `gh search code` for `"@mui/material"` in `package.json`, and
targeted lookups of specific real-world open-source products recalled to
use Material UI, cross-checked against each repo's actual committed
`package.json`/lockfile via the GitHub API and (for the three selected
repos) a full local clone. 11 candidates were investigated — comfortably
past the required minimum of 6 — before narrowing to 3.

## Accepted (final selection — see `SETUP.md` for full fixture record)

| Repo | Why accepted as a fixture |
|---|---|
| `bluewave-labs/Checkmate` | Actively maintained (commits same day as this snapshot), real self-hosted uptime/incident-monitoring product, 10.8k stars, single standalone Vite+React+TS frontend (`client/`) alongside an unrelated `server/`, npm with a committed lockfile resolving `@mui/material` to an exact version, and its `Pages/Incidents` surface has no `@mui/x-*` imports even though the app declares `@mui/x-charts`/`@mui/x-date-pickers` elsewhere. |
| `binwiederhier/ntfy` | Very actively maintained, 34k stars, real production pub/sub notification service (not built by the MUI team), single standalone frontend (`web/`), npm with a committed lockfile, and — uniquely among the strong candidates — declares no `@mui/x-*` package at all anywhere in `web/package.json`, the cleanest MUI-only authority boundary of the pool. |
| `hkbus/hk-independent-bus-eta` | Actively maintained, real production PWA used by real transit riders (not a demo), single standalone frontend at the repo root (a `src-tauri/` desktop wrapper sits alongside it but doesn't touch the selected pages), yarn with a committed `yarn.lock`, and its selected pages have no `@mui/x-*` imports even though the app declares `@mui/x-date-pickers` for an unrelated settings feature. |

## Rejected or set aside — reasons are fixture-suitability only

| Repo | Stars | Last push | Declared `@mui/material` | MUI X? | Why not selected |
|---|---|---|---|---|---|
| `Sekai-World/sekai-viewer` | 520 | active (same day) | `^5.18.0` | Yes — `@mui/x-data-grid` + `@mui/x-date-pickers` declared, and this is a data-heavy game-database viewer where table/grid surfaces are the obvious bounded surfaces, so DataGrid is plausibly load-bearing for exactly the shape (collection/management) this experiment wants from `@mui/material` alone. Kept as a pool entry, not pursued further, rather than spend time proving whether a DataGrid-free surface exists in this repo when two cleaner MUI-only candidates were already in hand. |
| `harryho/react-crm` | 523 | active (dependabot bumps) | `^7.3.11` (current MUI v7) | No | Its own README self-identifies it as "React Ecom Demo," a "proof of concept" spun off the author's personal Storybook boilerplate, with **no backend API** (data is mocked via MSW). This is exactly the "official templates / tutorial-flavored" profile the task asks to avoid as a primary fixture, despite otherwise-reasonable size and very current MUI version. |
| `batnoter/batnoter` | 2.4k | 2022-10-01 (stale) | `^5.5.3` | No | Real, independent, non-trivial note-taking webapp, but untouched for 3+ years and pinned to an MUI v5 release from the same era — fails "actively maintained or at least reasonably recent." Would be a plausible deliberate version-stress case if this round wanted one; not needed given three fresher candidates. |
| `CromwellCMS/Cromwell` | 752 | 2024-07-12 (stale) | `5.10.17` (pinned) | No `@mui/x-*`, but ships legacy `@mui/styles` (JSS) alongside modern `@mui/material` | Large multi-package monorepo (`system/admin`, `system/core/*`, `plugins/*`, `themes/*`, `toolkits/*` — 20+ `package.json` files), over a year stale, and mixes a deprecated styling API into the same admin package — a bounded surface here would need extra scaffolding just to orient, which the task's "reasonably bounded" criterion argues against. |
| `meshery/meshery` | 11.6k | active (same day) | `^9.1.2` (current MUI v9) | Yes — `@mui/x-date-pickers` + `@mui/x-tree-view`, the latter plausibly load-bearing for its navigation-heavy admin UI | Real, actively maintained CNCF project with a genuine `ui/` Next.js frontend workspace, but the **whole repository is ~5.7 GB** (`size: 5712038` KB via the GitHub API) — servers, providers, docs, and a large non-frontend tree ship in the same repo. Even isolating `ui/` as "the frontend root" doesn't change what has to be cloned/oriented-around locally; rejected on scale, not on its MUI usage. |
| `coder/coder` | — | active | — | — | `site/package.json` at current `main` has **no `@mui/*` dependency at all** — the project has migrated off Material UI since whatever point-in-time recollection suggested it as a candidate. Confirmed via direct fetch before spending further time on it; not a live MUI fixture today. |
| `minio/console` | — | — | — | — | `GET /repos/minio/console` returns 404 at the time of this reconnaissance — the repository is not resolvable at that path (likely merged/retired into another MinIO repo). Not clonable as an independent target; dropped without further investigation. |
| `franklioxygen/MyTube` | 1.2k | active (same day) | `^7.3.5` (current MUI v7) | No | Genuinely viable — real, actively maintained, single `@mui/material` dependency, no MUI X. Investigated as a fourth "detail/navigation" alternative to `hk-independent-bus-eta`; not selected because (a) three UI-shape slots were already filled by stronger-fitting candidates and (b) several of its page components are large and less atomized (`SettingsPage.tsx` ~40 KB, `SubscriptionsPage.tsx` ~55 KB) compared to `hk-independent-bus-eta`'s more evenly bounded page files, making a small, self-contained surface marginally harder to isolate without reading deep into unrelated logic. Recorded here in case a future round wants a fourth/alternate fixture. |

## Notable pattern across the rejected pool

Several strong-looking candidates by star count or topic match
(`react-admin`, `mui-treasury`, most of the `topic:material-ui`/`topic:mui`
top results not listed above) are themselves **libraries, component kits,
boilerplates, or admin-dashboard templates** built to showcase or extend
MUI — precisely the "official templates / demos" category the task asks
to exclude, just published by third parties rather than MUI itself. They
were noticed during the `gh search repos` pass and set aside without
individual write-ups above because they were disqualified on the same
"template/showcase, not an independent application" ground as the
official-MUI-template exclusion, not on any MUI-usage judgment.
