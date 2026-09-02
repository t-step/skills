# MUI generalization round — authority-structure and tooling observations

Status: setup only. These are observations about the **authority corpus**
and the **deterministic tooling**, recorded before any skill adaptation or
skill run. Nothing here evaluates any fixture's MUI usage, and nothing
here should be read as a verdict on whether the existing
`cloudscape-native-expression-review` skill will or won't generalize —
that is next session's question to answer, not this one's to prejudge.

## How MUI's `llms.txt` differs structurally from Cloudscape's

Section headings, in order, from each snapshot (`authority/cloudscape-llms.txt`
vs. `authority/mui-material-llms.txt`):

| Cloudscape | Material UI |
|---|---|
| Get Started | Components |
| Components | Design Resources |
| **Patterns** | Discover More |
| Demos | Material UI *(small catch-all: all-components index, a couple of late-added components, a hook)* |
| Foundations | Getting Started |
| About / Search / Terms / Privacy / Github / Gen Ai / Code Snippets | Customization |
| | Guides |
| | Integrations |
| | Migration |

The material difference: **Cloudscape's index carries an explicit,
separate `Patterns` section** (63 lines / dozens of entries) whose titles
are task-shaped and largely line up with the generic UI-shape categories
this whole experiment is organized around — *Card view*, *Create
resource*, *Delete patterns*, *Details page*, *Details page as a hub*,
*Details page with tabs*, *Attribute editing*, *Edit resource*, *Empty
states*, and more. Cloudscape's index also separates `Demos` from
`Patterns` as a distinct heading — i.e., Cloudscape's own information
architecture already draws the line the skill's "examples and demos are
not authority" rule insists on, rather than the skill inventing that
distinction unaided.

**This MUI snapshot has no heading that plays the same role.** Its
sections are components, design resources (Figma assets), discovery/
marketing links (showcase, roadmap, changelog), getting-started,
customization (theming/tokens/CSS mechanics), guides (bundle size, SSR,
localization, TypeScript, composition), integrations (Next.js, routing,
styled-components), and migration (version upgrades). None of these is a
task-oriented "how to compose components for this recurring product
problem" layer comparable to Cloudscape's `Patterns` section. The closest
adjacent concept, `Guides → Composition`, is about React composition
mechanics (slots, prop forwarding) — a component-API concern, not a
product-pattern one.

## What this could mean for the skill's reasoning procedure (observation only)

Recorded as open questions for the next session, not resolved here:

- **Whether MUI has explicit product-pattern documentation comparable to
  Cloudscape**: at the `llms.txt` discovery-index level, no. Individual
  component pages were not fetched in this setup pass (per the task's
  "treat llms.txt strictly as a discovery index... do not ingest the full
  documentation set" instruction), so whether a given component's own page
  (e.g., the Dialog or Autocomplete page) contains enough "when to use this
  vs. that" or "compose it this way for task X" semantics to substitute for
  a missing pattern layer is unknown and deliberately unverified here.
- **Whether MUI's guidance is primarily component-semantic, customization,
  or layout-oriented**: by section-heading weight alone, the snapshot leans
  component + customization (Components: ~60 entries; Customization: 20
  entries covering theming, tokens, density, breakpoints, z-index,
  transitions) over task/product guidance. This is a structural read of
  the index, not a claim about component-page content, which wasn't
  fetched.
- **Whether important behavior is spread across customization/guides
  rather than pattern pages**: plausible given the heading distribution
  above, but unverified — would require fetching component/guide pages,
  which this setup deliberately does not do.
- **Whether the future skill will need to operate with a weaker explicit
  pattern layer**: if the observations above hold once component pages are
  actually read, a Cloudscape-shaped retrieval priority ("component docs →
  pattern docs → foundations → inference," per `SKILL.md` step 3) may
  degrade gracefully to "component docs → (no comparable pattern tier) →
  inference" for MUI rather than failing outright — but whether that
  degrades usefully or just quietly drops the skill's pattern-composition
  half is exactly the open generalization question, and this setup task
  was explicitly told not to prejudge it.

## Deterministic tooling compatibility

Per the task, the existing scripts were run unmodified against the three
selected MUI fixture surfaces, passing MUI's own package prefix/names as
configuration rather than hardcoding anything MUI-specific into the
scripts.

### `inspect_surface.py --package-prefix '@mui/material' --package-prefix '@mui/icons-material'`

**Works unchanged.** Ran against
`Checkmate/client/src/Pages/Incidents/index.tsx` and produced the same
shape of factual JSX/import inventory it produces for Cloudscape fixtures
— import list, JSX tag counts, native-interactive-element scan,
style/className usage. One MUI-specific import-style observation worth
recording for the future skill (not a tooling defect): MUI code in this
sample mixes **deep per-component subpath imports**
(`import Stack from "@mui/material/Stack"`) **and barrel imports**
(`import { useTheme } from "@mui/material"`) in the same file. The script
already handles both correctly because it matches on source-string prefix
rather than assuming one import shape — this generalized for free — but a
future reviewer reasoning about "which Cloudscape/MUI components are in
play" needs to actually look at both `cloudscape_imports` entries (the
field name is inherited from the Cloudscape-authored script and is
generic in behavior, literal in name) rather than assume one import
convention.

### `resolve_versions.py --root ... --package @mui/material [--package ...]`

**Works unchanged for npm-lockfile projects, degrades gracefully (not a
crash) for the yarn-lockfile project:**

- `Checkmate/client` (npm, committed `package-lock.json`) and `ntfy/web`
  (npm, committed `package-lock.json`) both resolved correctly —
  `@mui/material` declared range and locked version both reported,
  `"resolved": true`.
- `hk-independent-bus-eta` (yarn, committed `yarn.lock`, **no
  `package-lock.json` anywhere in the tree**) reported `"lockfile": null,
  "resolved": false` for every package, even though the version *is*
  actually pinned in `yarn.lock` (`@mui/material@^5.15.11: version
  "5.15.11"`, confirmed by direct inspection). The script's own docstring
  states it reads "an npm package-lock.json... if one is found" — this is
  a **pre-existing npm-only assumption in the script itself**, not
  something that broke because of a Cloudscape-specific assumption baked
  into the calling logic. It is tooling-specific, not reasoning-specific:
  the script fails safe (explicit `"resolved": false"`, no exception, no
  false positive) rather than silently fabricating a version, so a
  reviewer using it would correctly learn "unresolved" and treat the
  version claim with the same "range only, unresolved" caution
  `SKILL.md` step 2 already prescribes for that exact scenario — it just
  arrives at that caution for the wrong underlying reason (missing yarn
  support) rather than the scenario the caution was originally written for
  (no lockfile committed at all). None of the three original Cloudscape
  fixtures happened to use yarn, so this gap was never exercised before
  this setup pass.

**No tooling was modified in this setup task**, per instructions — this
section only records what worked and what didn't.

### Post-setup correction (before the MUI-round freeze)

Before running the generalization evaluation itself, the yarn-lockfile gap
above was fixed with the smallest change that closes it:
`resolve_versions.py` now also looks for `yarn.lock` (after
`package-lock.json`) and, when one is found, matches the exact declared
`name@range` key against yarn v1 lockfile blocks to read the resolved
`version` field — no semver reasoning, same "facts only, fail safe"
discipline as the npm path. Re-run against
`hk-independent-bus-eta`: `@mui/material` now resolves declared `^5.15.11`
→ locked `5.15.11`, `"resolved": true`, matching the value this file
previously reported only via direct manual `yarn.lock` inspection. The npm
path (Checkmate, ntfy, and all three original Cloudscape fixtures) was
regression-tested unchanged. This is a tooling fix only — no skill wording,
retrieval priority, or evaluation semantics changed alongside it.
