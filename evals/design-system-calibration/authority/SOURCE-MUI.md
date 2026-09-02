# Material UI authority snapshot — provenance

- **Source URL:** https://mui.com/material-ui/llms.txt
- **Package/scope represented:** Material UI (`@mui/material`) only — the
  core component package. Explicitly **not** MUI X (`@mui/x-*` — data
  grid, date pickers, charts, tree view), not Joy UI, not Base UI. This is
  the Material UI package's own discovery index, served from the
  `/material-ui/` docs section of mui.com, distinct from
  `https://mui.com/x/llms.txt` (MUI X) or a hypothetical Joy UI/Base UI
  equivalent.
- **Fetched:** 2026-09-02 (HTTP `Date: Wed, 02 Sep 2026 14:37:15 GMT`; the
  response carried no `Last-Modified` header)
- **Content:** `mui-material-llms.txt`, 157 lines / 21,589 bytes (matches
  the `Content-Length` response header)
- **Integrity:** ETag `"d1e6e8e4e3010e2efcaa56ecceddeb20-ssl"` (weak
  CDN/SSL-suffixed ETag from Netlify — not a strong content hash);
  MD5 of the stored file: `3ce28d6691af7a96dbf6fb16242642a2`
- **Purpose:** fixed, versioned view of what authoritative Material UI
  guidance is discoverable right now, for the design-system-calibration
  generalization experiment — independent of whatever mui.com serves on a
  later date. Evaluation/experiment material, not skill logic.

## What this is

`llms.txt` is Material UI's own discovery/index file, structurally
parallel to Cloudscape's: a flat list of links into `mui.com`, each with a
one-line description, grouped under `##` headings. It is **not** itself
component documentation — each linked page must be fetched separately by
a future reviewer for the actual guidance. Per the task that created this
snapshot, treat it strictly as a discovery index: do not ingest or locally
mirror the full linked documentation set in this setup pass.

Section headings observed in this snapshot, in order: `Components`,
`Design Resources`, `Discover More`, `Material UI` (a small catch-all —
the "all components" index page, a couple of components added after the
main `Components` section, and a hook), `Getting Started`,
`Customization`, `Guides`, `Integrations`, `Migration`.

## How this differs structurally from the Cloudscape snapshot

See `evals/design-system-calibration/MUI-GENERALIZATION-NOTES.md` for the
full discussion. Summarized here for provenance purposes only: Cloudscape's
`llms.txt` groups links under headings that include an explicit
task/product **pattern** layer (multi-component, task-shaped guidance
distinct from single-component docs). This MUI snapshot's headings are
components, design resources, discovery/marketing links, getting-started,
customization, guides, integrations, and migration — no heading names a
comparable pattern layer. Whether individual component pages nonetheless
carry enough "when to use this vs. that" semantics to substitute is an
open question for the future evaluation, not something this snapshot
setup resolves.

## How this fits the future skill

Same discipline as the Cloudscape snapshot: this file is evaluation/
experiment material only. It exists to test whether the
`cloudscape-native-expression-review` reasoning *operation* generalizes
to a design system supplied with different authoritative material — it is
not itself skill logic, and nothing here should hard-code MUI specifics
into any future generalized skill.
