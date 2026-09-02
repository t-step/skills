# cloudscape-native-expression-review — eval results

**Run date:** 2026-09-01. **Model:** claude-sonnet-5, fresh `general-purpose`
subagent per run (no fork, no shared context) — 7 baseline + 7 skill + 7
adversarial-verifier runs across six purpose-built pressure cases (A–F) and
one real, unmodified, pinned-SHA fixture reused from
`cloudscape-implementation-audit`'s own eval. Full raw transcripts are local,
untracked artifacts; `runs/*.md` (baseline.md / skill.md / verify.md per
case, plus `baseline-v1.md`/`skill-v1.md` for cases E and F — see "Fixture
contamination and correction" below) are the committed, auditable record
every claim below cites.

The skill's design, its two reused deterministic scripts, all six pressure
cases, and their isolated grading keys were frozen (committed) **before**
any baseline or skill run — see the freeze commit
`feat: add cloudscape-native-expression-review experimental skill + eval`.
No skill wording was tuned after seeing a review's output. The one
after-freeze change made was a fixture correction (documented below), not a
skill-behavior tune.

## 1. Skill reasoning operation and boundary

`cloudscape-native-expression-review` asks one question: **given the user
task a bounded surface expresses, does it use Cloudscape's component
vocabulary and established patterns the way a Cloudscape-fluent implementer
would naturally express that same task?** It deliberately combines
component selection ("was the right component chosen?") and pattern
composition ("does this composition match an established pattern for this
task?") as one operation, with a four-part scope fence: not implementation
correctness (`cloudscape-implementation-audit`'s domain — API usage, props,
tokens, a11y mechanics), not general UX critique, not product redesign
(never invent a different user goal), and an explicit `intent-dependent`
escape hatch when the code doesn't establish enough intent to choose
between two native expressions. Every finding carries a four-point
applicability test (task match, current-implementation-solves-same-problem,
semantics-preserved, materially-different) drawn directly from the task
brief's "Anti-fundamentalism rule."

## 2. Did component selection + pattern composition stay coherent as one skill?

**Yes, on this round's evidence — and the real fixture is the sharpest
demonstration of why.** Three of seven cases (C, real Finding 1, and
implicitly B) produced findings that genuinely needed both halves at once:
Case C's single `combined component + pattern` finding (Table→KeyValuePairs
*and* tab-placement) would have been two disconnected, weaker findings if
split — which is exactly what baseline did, and exactly what the case was
built to catch (rubric question 8). No case produced evidence that the two
reasoning modes actively interfered with each other or that splitting them
would have helped. The one clean counter-signal — Case A's recall miss —
is a coverage gap (the run never generated the pattern-level candidate at
all), not evidence that combining component and pattern reasoning caused a
miss that isolating them would have prevented; nothing in that run's
transcript suggests it would have found the ContentLayout/full-page
tension if it had been running a pattern-only pass instead.

## 3. Pressure cases and why each was diagnostic

Full design rationale: `README.md`. Summary of what each targeted and what
the skill's own applicability discipline had to get right:

- **Case A (`FleetNodes.tsx`)** — right components, wrong pattern
  (`ContentLayout`+`Table variant="container"` vs. the table-view pattern's
  explicit "Don't...Instead" rule), built unambiguous (7 substantive
  columns, zero other page content) specifically to remove the ambiguity
  the real `Identities.tsx` fixture carries.
- **Case B (`EndpointScaling.tsx`)** — wrong component (`Cards` for a
  22-item, explicitly comparison-driven task that Cloudscape's own
  view-resources guidance assigns to `Table`).
- **Case C (`WorkspaceDetails.tsx`)** — combined component+pattern: a
  one-row `Table` standing in for `KeyValuePairs`, misplaced inside a tab
  instead of the details-page-with-tabs pattern's persistent summary
  container — one underlying recommendation, testing whether the skill
  unifies or artificially splits it.
- **Case D (`RecentWorkspaces.tsx`)** — equally valid alternative: a small,
  glanceable, non-comparison `Cards` collection where `Table` would also
  technically work but isn't materially better. Precision test: correct
  answer is no finding.
- **Case E (`CertificatesTable.tsx`+`CertificateDetails.tsx`)** — pattern
  lookalike, wrong intent: a table+per-row-detail shape that superficially
  invites a "use split view" recommendation, which split view's own docs
  explicitly forbid for full single-resource detail ("A split view should
  never replace details pages"). The primary anti-cargo-cult case.
- **Case F (`QuotaRequests.tsx`)** — missing intent: a `Modal` showing a
  medium-detail field set for a resource whose addressability
  (transient log entry vs. persistent resource) is genuinely undetermined
  by the code. Correct behavior: `intent-dependent` or suppress, never a
  confident directional recommendation.
- **Case Real (`Identities.tsx`)** — the real fixture
  `cloudscape-implementation-audit`'s own iteration 2 already exposed the
  exact `ContentLayout`+`container` vs. `full-page` tension on, producing
  an adversarially-confirmed **D-grade overreach** when that
  implementation-only skill tried to make the call. Reused specifically as
  this experiment's flagship real-world validation.

All six synthetic cases were validated against both reused deterministic
scripts (`inspect_surface.py`, `resolve_versions.py`) before any review ran,
confirming both parse every fixture and resolve declared/locked versions
correctly.

## 4. Baseline vs. skill — numeric summary

Every candidate finding from every run was graded A–E by an independent
adversarial verifier per the rubric (`rubric.md`), one verifier per case,
each reading both the baseline and skill review for that case plus the
case's grading key (none for the real fixture) and independently
re-fetching every cited Cloudscape page.

| Grade | Baseline (26 findings) | Skill (7 findings) |
|---|---|---|
| A | 3 (12%) | 3 (43%) |
| B | 7 (27%) | 4 (57%) |
| C | 3 (12%) | 0 |
| D | 12 (46%) | 0 |
| E | 1 (4%) | 0 |

**Read plainly:** across seven cases, the skill's reported findings were
100% A/B (0% C/D/E) — no overreach, no factual error, no routine/low-value
finding survived its own materiality discipline to reach the report. The
unguided baseline's findings were 46% D and 4% E — nearly half of what
baseline reported would not have survived adversarial scrutiny, mostly for
leaking into `cloudscape-implementation-audit`'s territory (missing props,
a11y markup, event-handler wiring) while accurately citing real Cloudscape
documentation, or for asserting confident recommendations on genuinely
underdetermined applicability. This is a stronger, more concrete precision
gap than raw finding count suggests — see "What this does not prove" for
the caveats on reading too much into it.

**Read against materiality, not just precision:** baseline independently
found four of the skill's core "should-be-found" targets (Case A's
designed finding, Case B's core finding, Case C's two underlying
component+pattern facts, Case E's Button-vs-Link finding, the real
fixture's `ContentLayout`/full-page finding) — baseline's core reasoning is
genuinely capable, and on materiality alone this is not a case of an
unguided reviewer producing noise a skill then cleans up. What differs is
scope discipline and structuring: baseline consistently pads a correct
core finding with additional, less-disciplined asides that dilute the
report (Cases A, B, E all show this pattern), and twice fell into the
specific traps the pressure cases were built to expose (Case D: never
engaged the actual test; Case F: confidently recommended the exact
pattern its own cited source explicitly rejects).

## 5. Case-by-case results vs. designed intent

| Case | Designed intent | Skill result | Baseline result |
|---|---|---|---|
| A | Real pattern-tension finding | **Miss.** Found a different, real, B-grade finding (TextFilter→PropertyFilter); never mentioned `ContentLayout`/`full-page` anywhere in Findings, Suppressed, or Orientation notes. | **Partial match.** Found the designed A-grade finding, but buried it among four more findings, all D-graded for leaking into implementation-audit territory. |
| B | Real component-selection finding | **Match.** One A-grade finding, tightest and most thoroughly sourced of either review; correctly suppressed the `ContentLayout` ambiguity as unresolvable from one file. | **Partial match.** Found the same A-grade core finding independently, diluted by three more (D, C, D). |
| C | One unified combined finding | **Match on structure** (exactly one `combined component + pattern` finding, matching the case's central Q8 test) — but the finding's own citations included one fabricated quote and one misquote among ~6, landing it at **B** instead of A on citation-accuracy grounds alone. | **Fails the designed intent.** Split the identical underlying issue into two separate findings (B, B) — precisely the Q8 failure mode the case exists to catch — plus one false-positive D-grade finding on the Activity tab. |
| D | No material finding (Cards vs. Table) | **Match.** Never recommended Table; explicit "checked and cleared" orientation note. Also surfaced an unanticipated, well-reasoned `intent-dependent` finding on a different axis (full-page Card-view shell vs. Dashboard-items pattern, contingent on how the page is mounted) — graded **B** (one of its two branches partially overreaches per the verifier, but the core is sound and correctly hedged). | **Avoided the trap only by omission.** Never engaged the comparison-task/collection-size applicability test at all; its three findings (D, B, D) are implementation-level nitpicks. |
| E | Reject the split-view temptation | **Silent-but-diligent.** Never named split view, but explicitly confirmed `CertificateDetails.tsx` against the Details-page building blocks and the "more than 10 items → hub pattern" threshold — the right kind of diligence, just not the explicit rejection the grading key calls the strongest possible response. One real A-grade finding (identifier-column navigation). | **Also silent**, with no structural evidence split view was ever considered. Four findings (B, B, D, D) — two leak into implementation-mechanics territory. |
| F | Classify intent-dependent / suppress | **Match — the cleanest result in the eval.** Zero findings; explicitly considered and rejected both Split View and Details Page with accurate, verified citations. | **Fails.** Confidently recommended Split Panel — graded **E**, factually contradicted by the same pattern page's own explicit "should never replace details pages" language — plus a dependent D-grade second finding. |
| Real | (no pre-decided answer) | Two findings (**A**, **B**): the `ContentLayout`/`full-page` finding and a Modal-vs-`SplitPanel` finding for activity drill-in, plus two correctly suppressed candidates. | Four findings (**B, A, B, C**) — same core `ContentLayout`/full-page finding independently found and also graded A, plus a filter gap, a Modal-vs-split-view finding, and a low-value pagination finding that should have been suppressed. |

## 6. The real-fixture validation — the central result

`Identities.tsx` is the same surface `cloudscape-implementation-audit`'s
iteration 2 reviewed. That skill's frozen procedure produced a
`violation`-classified finding recommending `Table variant="full-page"`
over `ContentLayout`+`Table variant="container"`, cited the table-view
pattern page — and an independent adversarial verifier graded it **D
(overreach)**, specifically because a pattern-page citation was stretched
to license a page-composition recommendation at implementation-audit
REQUIRED strength, a category that skill's own scope boundary explicitly
excludes (`evals/cloudscape-implementation-audit/RESULTS-ITERATION-2.md`,
§6).

This eval's skill run, given the same file, reached the same substantive
conclusion — and its dedicated verifier explicitly checked it against the
sibling's three named failure vectors:

- **Domain fit:** this skill's actual job is component/pattern selection;
  the finding's own "Boundary check" field states the distinction directly
  rather than blurring it.
- **Strength vs. evidence:** typed `combined component + pattern` (not
  `violation`), with a fully-written four-point applicability argument, not
  a bare citation.
- **Incomplete fix named honestly:** the `AppLayout contentType="table"`
  dependency outside the audited file is called out by name, not silently
  assumed.

The verifier's conclusion: *"this run avoided the sibling skill's exact
overreach failure mode rather than repeating it in a new guise."* This is
the single most direct confirmation the experiment's product hypothesis
was built to test: an agent given an unfamiliar frontend plus authoritative
design-system material can produce evidence-backed, correctly-scoped
native-expression guidance — and a finding that is overreach one layer
down is legitimate, well-evidenced material one layer up, at the layer
built to own it.

## 7. Negative-case performance (D, E, F)

- **Case D (equally valid alternative):** skill correctly declined to
  recommend Table, with an affirmative applicability check, not silence.
- **Case E (pattern lookalike, wrong intent):** skill did not recommend
  split view (neither did baseline) — a pass on the narrow "no false
  positive" bar, though not the strongest possible "explicit rejection"
  the case was designed to reward; see "False positives/overreaches" for a
  candid read on why this is weaker than Case F's result.
- **Case F (missing intent):** clean pass — the one case where the skill's
  discipline and the baseline's failure are both unambiguous and
  independently confirmed (E-grade factual error on baseline's centerpiece
  finding).

**Two D-grade findings among the *baseline* runs directly replay the
"pattern existence/general UX dressed as citation" failure modes the task
asked to watch for** — Case D baseline's missing-header-counter and
missing-`fontSize` findings are real, accurately-cited Cloudscape
guidance applied with no applicability reasoning at all, exactly the
"docs contain another example" shape the skill's anti-fundamentalism rule
targets. **Zero skill-run findings fell into this shape.**

## 8. False positives and overreaches

**Zero D/E grades among the seven skill findings reported to the final
report.** The closest thing to a genuine skill-side weakness this round
surfaced is not an overreach but two calibration issues:

1. **Case A: a flat recall miss**, not a false positive — the skill run
   never generated the designed-intent candidate at all. Cannot be
   distinguished from "correctly didn't consider it" vs. "never looked" by
   this eval's design (the same open question iteration 1 of the sibling
   eval flagged); here it reads more like a genuine coverage gap, since the
   run's own "Orientation notes" explicitly confirm "Table is the right
   macro pattern" and stop one level short of checking the variant choice.
2. **Case C: citation-accuracy problems inside an otherwise A-quality
   finding** — one fabricated quote and one misquote among roughly six
   citations, discovered only because the verifier independently
   re-fetched every cited page rather than trusting the review's
   quotation marks. The finding's structural/substantive correctness
   (unified combined finding, correct applicability reasoning, correct
   boundary check) is real and independently sufficient even discounting
   the two bad quotes — but this is a genuine citation-discipline gap, not
   a rounding error, and it is exactly the failure mode this whole
   family's authority model exists to prevent ("cite the exact source,
   never the index's description").

## 9. Fixture contamination and correction (cases E and F)

Baseline case E's first run (`baseline-v1.md`) surfaced an unintended
construction defect I introduced: both `CertificatesTable.tsx` (Case E) and
`QuotaRequests.tsx` (Case F) originally wrapped `Table variant="full-page"`
in a `ContentLayout` — a self-contradictory composition (the full-page
variant is documented to replace `ContentLayout`, not sit inside it), not
a deliberate part of either case's design. Both fixtures were corrected
(header moved onto the table's own `header` prop, `ContentLayout` wrapper
removed) and both cases' baseline+skill runs were rerun (v2); v1 outputs
are preserved as `runs/case-{e,f}-{baseline,skill}-v1.md` rather than
deleted, per this repo's precedent for informative-but-superseded runs
(`cloudscape-implementation-audit`'s own case-4 v1/v2 correction).

Both v1 and v2 are informative: on Case F specifically, the v1 skill run
(against the still-contaminated fixture) also confidently recommended
Split Panel — the same trap baseline fell into on both v1 and v2 — while
the v2 skill run (clean fixture) correctly suppressed both temptations.
This is not attributable to the one-line fixture fix touching anything
about the Modal/intent question; it reads as ordinary run-to-run variance
under extra, unrelated noise (the same caveat the sibling eval's iteration
2 recorded about its own recall numbers) rather than evidence the fixture
correction changed the underlying judgment call — the v2 result is what
stands as the frozen, valid record either way.

## 10. Component-vs-pattern overlap observed in actual findings

Of the seven skill findings reported: two were typed `component selection`
in substance though the skill itself used `combined component + pattern`
for one of them (Case B, per the verifier's note that a plainer
`component selection` label would have been cleaner, not a scoring
problem); one was a genuine, verifier-confirmed unified `combined
component + pattern` finding (Case C); two were pattern-level compositions
with component-level consequences (Case A's real-fixture analog, Case E);
one was `intent-dependent` spanning both levels at once (Case D). No
finding in this round was cleanly, exclusively one or the other with no
trace of the sibling category — every real finding this round touched both
dimensions to some degree. That is direct, if modest, evidence for keeping
them combined, though a battery of seven cases against one model is not a
powered result.

## 11. Deterministic tooling

Both reused scripts (`inspect_surface.py`, `resolve_versions.py`) ran
unmodified against all seven fixtures, correctly reporting import/JSX
inventories and resolved/unresolved version state in every run (including
the real fixture, correctly resolving a version drift between the
declared `^1.0.55` and locked `1.0.105` for `collection-hooks`). No run's
findings depended on a fact these scripts got wrong. They also didn't
change any run's *conclusion* — every genuine judgment call (applicability,
task inference, whether a pattern fits) remained squarely agentic, as
intended; the scripts earned their keep as fact-gathering, not as
decision-shaping. No concrete failure this round demonstrated a need for
new tooling, consistent with the task's instruction not to expand them
into a decision engine absent such evidence.

## 12. llms.txt + selective retrieval

Sufficient for this round. Every citation independently re-fetched by a
verifier — across all seven cases — resolved to a real, live Cloudscape
page; several verifiers specifically noted that Cloudscape's component and
pattern pages are client-rendered SPAs where a plain `WebFetch` only
returns the pre-render shell, requiring a rendered-browser fetch
(Playwright / `defuddle`) to get the actual usage-tab text — a real
retrieval friction point, but one every run (baseline and skill alike)
worked around successfully, not a discovery-index limitation. The one
verifier-caught citation problem (Case C) was a fabrication/misquote by
the *reviewing* agent, not a retrieval-index failure — the correct source
text was fetchable and was in fact independently confirmed by the same
verifier from the same index-directed page.

## 13. What a manually curated components/patterns/foundations pack would improve

- **A pre-verified quote layer.** Case C's citation problem would not
  survive a calibration pack that ships exact, pre-extracted guidance
  strings rather than asking each run to quote a live-rendered page from
  memory of what it just read — this is the single most concrete,
  evidence-backed case for a curated pack this round produced.
- **An explicit component-comparison layer.** Several of this round's
  strongest findings (Case B, the real fixture's Finding 1) needed to
  synthesize guidance living on *two* separate pages (e.g., the losing
  component's page and the winning component's page, or a component page
  plus its pattern's page) — a curated pack that pre-links "when NOT to
  use X, see Y" relationships would shorten this retrieval path
  measurably.
- **A pre-flagged low-materiality-threshold list**, since a real,
  recurring failure mode this round was baseline (never the skill)
  surfacing real, accurately-cited guidance that a documented volume/count
  threshold elsewhere on the same page would have ruled out (Case D's
  missing counter on 6 always-visible items; the real fixture's pagination
  finding). A pack that pre-annotates these thresholds would make this
  discipline mechanical rather than solely agentic.

## 14. Comparison with the implementation-audit experiment

Where implementation-audit's iteration 2 left an open, adversarially
*confirmed* wound (an overreach on this exact real fixture), this
experiment's skill closed it cleanly on the same file — not by loosening
either skill's scope, but by routing the finding to the layer built to
own it. This is the concrete evidence both experiments' own "how this
composes" sections predicted was needed before either layer's design
could be trusted: implementation-audit's iteration-2 verdict explicitly
argued against building a second, higher-layer skill until its own layer
held up better; this round's real-fixture result is the first piece of
evidence that the higher layer, once built and evaluated on its own
narrow terms, handles the exact case the lower layer couldn't.

## 15. Verdict

**KEEP** — with one flagged, evidence-backed follow-up (Case A's recall
gap), not an ITERATE-forcing defect.

Not RETIRE: zero D/E findings across seven independently verified skill
runs against a battery specifically built to surface overreach, cargo-cult
pattern-matching, and missing-intent guessing; a clean, decisive win on the
hardest negative case (F); and the flagship real-fixture validation this
whole experiment exists to produce.

Not ITERATE (yet): the one concrete shortcoming (Case A's recall miss) is
a single, isolated miss on one pressure case, not a pattern across the
battery — the skill correctly found the parallel comparison-task finding
in Case B and the parallel pattern-tension finding on the real fixture
using the identical reasoning shape Case A needed. Tuning SKILL.md after
one observed miss, per this repo's own eval-expectations discipline, risks
fitting this fixture rather than the underlying gap; the smallest
justified next step (below) is to gather one more data point before
editing.

## 16. Smallest justified next step

**Run the frozen skill against one more synthetic case built specifically
to isolate whether Case A's miss is a genuine "checked Table's macro
pattern and stopped one level short of the variant choice" blind spot, or
ordinary single-run variance** — a second full-page-table-vs-`ContentLayout`
pressure case, structurally distinct from Case A (different resource type,
different column count, no plausible secondary finding like Case A's
PropertyFilter candidate to distract the run), with its own fresh baseline
+ skill + verifier triple. If the miss reproduces, the smallest justified
skill edit is a targeted addition to the "Characterize the current
expression" step naming variant/wrapper choice as its own explicit check,
parallel to the macro-component check the transcript shows the run already
performs — not a rewrite of the applicability or authority sections, which
performed cleanly across every other case this round. Do not build a
higher-layer alignment/synthesis reviewer next regardless of that result;
nothing in this round's evidence establishes this skill's own layer is
solid enough yet to build on top of, and the task brief's own instruction
is not to build one automatically.

**Addendum:** this next step was carried out — see
`RESULTS-ITERATION-2.md` for the isolating pressure cases (A1/A2/A3),
their frozen-skill results, and the resulting verdict
(**KEEP-WITH-KNOWN-LIMITATION**).
