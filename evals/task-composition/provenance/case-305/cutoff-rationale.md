# Cutoff rationale — case-305 (Rust AFIT + RPITIT stabilization history)

## Adversarial provenance audit (before any fixture file was written)

This section works through every candidate topology claim named in the
research brief, in the historical-fact / supported-grading-constraint /
not-supported format the brief requested. All primary-source citations are
in `sources.md`. This audit was done before `tasks.md`/`dependencies.md`
were drafted, and every fixture-construction choice below traces back to
it.

### Claim 1: "AFIT and RPITIT were intentionally allowed to progress somewhat independently."

- **Historical fact:** PR #100734 ("Split out `async_fn_in_trait` into a
  separate feature," opened 2022-08-18, merged 2022-09-23) states its own
  rationale verbatim: "PR #101224 added support for async fn in trait
  desuraging [sic] behind the `return_position_impl_trait_in_trait`
  feature. Split this out so that it's behind its own feature gate, since
  async fn in trait doesn't need to follow the same stabilization
  schedule." This is a real, dated, primary-source statement of a
  deliberate decision, made five weeks after RPITIT's initial
  implementation (#101224, merged 2022-09-09) had AFIT running under
  RPITIT's own gate.
- **Supported grading constraint:** A plan may treat AFIT and RPITIT as
  having run on deliberately separate feature-gate/stabilization
  schedules since 2022-09-23, for a stated reason (schedule
  independence), not as an unexplained historical accident.
- **Not supported:** This is schedule/administrative independence, not
  evidence of full implementation or semantic independence. The same PR's
  own rationale presupposes AFIT literally desugars into RPITIT's
  mechanism ("async fn in trait desugaring behind the
  return_position_impl_trait_in_trait feature") — it splits the *gate*,
  not the *mechanism*. RPITIT's own founding RFC attempt (RFC 3193, opened
  2021-11-10) already frames RPITIT as existing "as a building block for
  async function support" — i.e. even the earliest RPITIT proposal never
  claimed conceptual independence from AFIT. A plan that concludes "AFIT
  and RPITIT were built as two unrelated features that happened to share a
  name" overclaims what the record shows.

### Claim 2: "Separate feature-gate/stabilization treatment was explicitly considered reasonable."

- **Historical fact:** Same as Claim 1 — #100734's own stated rationale.
  Also: RFC 3185 (AFIT's own RFC) merged 2021-12-07T18:27:36Z, over 17
  months before RFC 3425 (RPITIT's own RFC) merged 2023-06-13T10:03:08Z —
  AFIT had a ratified governing RFC and RPITIT did not (RFC 3193, its
  first attempt, was withdrawn unmerged 2021-12-09) for that entire
  window.
- **Supported grading constraint:** A plan may cite the ~17-month gap
  between AFIT's and RPITIT's own ratified RFCs, and the explicit
  gate-split rationale, as real evidence that treating them as separately
  schedulable was a considered, stated engineering position, not an
  invented one.
- **Not supported:** This does not establish that separate
  gate/schedule treatment remained appropriate indefinitely, or that it
  was never revisited — see Claim 3.

### Claim 3: "Later, shared semantic/forward-compatibility concerns created a convergence requirement near stabilization."

- **Historical fact:** RFC 3425 itself (RPITIT's actual RFC, opened
  2023-04-27, merged 2023-06-13) states as one of its **own stated
  summary goals**, not a later discovery: "Allow `async fn` in traits and
  trait impls to be used interchangeably with its equivalent `impl Trait`
  desugaring." The RFC's own "Unresolved questions" section (part of the
  ratified text) lists, verbatim: "Should we stabilize this feature
  together with `async fn` to mitigate hazards of writing a trait that is
  not forwards-compatible with its desugaring?" immediately followed by
  "Resolution of #112194: RPITIT is allowed to name any in-scope lifetime
  parameter, unlike inherent RPIT methods." Issue #112194 itself was
  opened 2023-06-02 (11 days before RFC 3425 merged), framed on its face
  as an RPITIT-internal lifetime-capture soundness question, discovered by
  `tmandry` while responding to a review comment on RFC 3425's own PR
  thread.
- **Supported grading constraint:** The forward-compatibility design goal
  (interchangeable desugaring) is stated as an original RFC 3425 design
  intent (April 2023), not something discovered only at the last minute.
  What *is* later and concrete is #112194 — a specific soundness question
  that the RFC's own ratified text names, unresolved, as directly bearing
  on whether AFIT and RPITIT should stabilize together. A plan may treat
  "whether to stabilize AFIT and RPITIT together" and "resolution of
  #112194" as one real, RFC-text-linked pair of open questions that the
  record does not resolve as of this fixture's cutoff.
- **Not supported:** Two overclaims to avoid. First, "convergence was
  entirely unforeseen until #112194" — the RFC's own design goal
  (interchangeability) predates #112194 by weeks and #112194 is better
  read as *exposing/testing* a pre-existing designed-for constraint (can
  the two features' desugarings really stay interchangeable?) than as
  creating a brand-new one from nothing — this is the audit's answer to
  the research brief's own question "did #112194 create or merely expose
  a convergence constraint": **it exposed/tested one RFC 3425 had already
  designed for**, four weeks before #112194 was filed. Second, "the RFC
  resolved this" — it explicitly did not; both items are listed under
  "Unresolved questions," meaning the ratified RFC poses the question
  without answering it.

### Claim 4: "The eventual historical implementation stabilized them together."

- **Historical fact:** PR #115822 ("Stabilize `async fn` and return-position
  `impl Trait` in trait," opened 2023-09-13, merged 2023-10-14) is a
  single PR stabilizing both features; its own body states "The
  desirability of this [AFIT-as-RPITIT] desugaring being available is
  part of why RPITIT and AFIT are being proposed for stabilization at the
  same time," and its own "History" section describes "Initial
  implementation of AFIT and RPITIT" as one bullet, not two.
- **Supported grading constraint:** This is true, and is exactly the kind
  of fact this suite treats as DIAGNOSTIC/historical-outcome material
  (postdates this fixture's cutoff by three months) — informative about
  how the story ended, not usable as an in-fixture fact and never a
  substitute for reasoning about the cutoff-visible record.
- **Not supported — this is the claim the brief is most explicit about:**
  "Joint stabilization does not automatically establish that AFIT and
  RPITIT should have been one delivery slice throughout implementation."
  The bulk of both features' actual implementation (13 of the 14 PRs named
  in the original research brief, all but #115822) landed in a tight
  2022-09-09 to 2022-10-23 window, under separate gates, a full **eleven
  months** before the joint stabilization PR. Historical joint
  stabilization is a fact about how the *stabilization decision* was
  eventually made — it is not evidence, on its own, that the day-to-day
  bug-fixing and implementation work in this fixture's own cutoff window
  (see Task set below) needed to be composed as one slice. This is this
  suite's now-recurring lesson (see case-303's corrected REQUIRED #8,
  and case-304's own central design note) applied to a case where the
  temptation runs in the opposite direction from case-304's: there, a
  shared root cause tempted merging four separately-progressing tickets;
  here, a shared *desugaring mechanism* plus an *eventual joint
  stabilization* tempts merging eight separately-filed, separately-owned
  bug tickets that mostly have nothing to do with each other.

### Claim 5 (research-brief item): "#112194 created or merely exposed a convergence constraint?"

Answered under Claim 3 above: exposed/tested a pre-existing constraint
(RFC 3425's own April-2023 interchangeability design goal), not created a
new one from nothing.

### Claim 6: "A shared semantic contract implies shared implementation ownership."

- **Historical fact:** #100734's gate split (Claim 1) is direct
  counter-evidence — the team explicitly kept the two features on
  separate schedules for over a year even while their desugaring
  mechanisms are (per Claim 7 below) genuinely coupled at the code level.
  The eventual fix for #112194 (PR #114489, DIAGNOSTIC-only, merged
  2023-08-28) is itself a pure RPITIT-side change (no AFIT-labeled file
  touched) driven by a broader T-lang "opaque captures" policy decision
  that also covered ordinary (non-trait) RPIT — not something that
  required AFIT's own maintainers or files to change.
- **Supported grading constraint:** A plan may recognize that AFIT and
  RPITIT share a semantic contract (the desugaring) without concluding
  that all work on either feature must be co-owned or co-implemented.
- **Not supported:** Nothing licenses inventing a "these must always ship
  from the same PR/person" rule from the shared-contract fact.

### Claim 7: "Historical joint stabilization is normative evidence for earlier slicing."

Already covered under Claim 4's "Not supported" — restated here because
the brief lists it separately: this is explicitly the wrong conclusion
this fixture is built to make tempting-but-refusable, mirroring case-303's
corrected REQUIRED #8 and case-304's central design note, applied for the
first time to a "the record shows genuine mechanism-level coupling"
fixture rather than a "the record shows a shared discovered bug pattern"
one (case-304).

### Claim 8: "Feature-gate identity is proof of permanent independence" / "AFIT and RPITIT were parallel-safe" (as a blanket claim)

- **Historical fact:** #108309 ("Weird interaction between specialization
  and RPITITs," opened 2023-02-21, still open) was labeled with both
  `F-async_fn_in_trait` and `F-return_position_impl_trait_in_trait` by
  `compiler-errors` (the primary implementer of both features) in the
  same minute the issue was filed, and their own comment states plainly:
  "Because async fn in trait is just return position impl trait in trait,
  and the specialization problems are equally as broken with the latter?"
  Separately, PR #100734 (the gate-split PR) and PR #101224 (RPITIT's
  initial implementation) both touch the same file,
  `compiler/rustc_ast_lowering/src/lib.rs` — a real, `gh api`-verified
  shared file at the desugaring layer, present since the very first
  implementation PRs (2022-08 to 2022-09), not something discovered later.
- **Supported grading constraint:** Separate feature gates are real and
  administratively meaningful, but they do not, by themselves, establish
  that the two features' *implementations* never share code, files, or a
  root-cause mechanism. This fixture has a genuinely, textually confirmed
  shared file and a core-team quote stating the underlying mechanism is
  literally the same thing — a plan that treats "separate feature gate"
  as sufficient proof of "fully independent, parallel-safe implementation
  work" is overclaiming what two different, real facts (gate separation;
  mechanism sharing) actually establish when taken together.
- **Not supported:** The opposite overclaim is equally available and must
  also be refused — the shared file/shared-mechanism fact is about the
  two features' *original, already-landed* implementation (2022), not
  proof that every currently-open bug ticket in this fixture's task set
  touches that same file or must be serialized through it. Only three of
  this fixture's eight open tickets (#108309, #108304, #109016 — see Task
  set) are themselves dual-labeled/dual-relevant; the other five
  (#104689, #110963 on the AFIT side; #111105, #109468, #112194 on the
  RPITIT side) are single-feature bugs with no stated cross-reference to
  each other or to the dual-labeled cluster, and treating all eight as one
  contended blob because *some* mechanism-sharing exists somewhere in this
  codebase would be exactly the false-parallel-illusion failure mode this
  skill's own "Minimal topology validation" section exists to catch, run
  in reverse (manufacturing contention instead of manufacturing
  parallelism).

### Claim 9: "SKILL.md heuristics being graded as historical facts" (audit self-check)

Every REQUIRED item in `grading/case-305.expected.md` traces to a specific
citation in `sources.md`, independently verified via `gh api` against
live GitHub/RFC data during this session (not recalled from training
knowledge — see the "Training-data contamination" limitation this write-up
will carry in `RESULTS.md`, which applies to the author's own background
knowledge of this history just as much as to a tested agent's). No
REQUIRED item cites `skills/task-composition/SKILL.md`'s own vocabulary
(vertical slice, horizontal enabler, convergence) as if it were a fact
about Rust's history; that vocabulary is used only in `grading/
case-305.expected.md`'s "Why" section to explain *why* this fixture
pressures the skill, never as a source of REQUIRED-item content.

## Chosen cutoff

**2023-06-13, end of day (UTC).**

This is the day RFC 3425 (RPITIT's actual, ratified governing RFC) merged
(2023-06-13T10:03:08Z) — ending the ~17-month period in which AFIT had a
ratified RFC and RPITIT did not — while the tracking issue's own
formal restructuring (renaming its title to name both features, splitting
its "Unresolved Questions" section, and formally cross-referencing
#112194 into itself) does not happen until the next day, in a
14-minute editing burst by `tmandry` between 2023-06-14T21:48 and
2023-06-14T22:02 UTC. Choosing the cutoff on the near side of that edit
keeps the fixture from handing a tested agent the community's own,
already-performed "should we treat this as a joint concern" framing.

## Why this point is defensible

1. **Both features already have over nine months of separately-gated
   implementation history by this point** (feature gates split
   2022-09-23; the bulk of both features' initial implementation, 13 PRs,
   landed 2022-09-09 to 2022-10-23) — i.e. both already have "enough
   implementation identity to appear independently tractable," per the
   research brief's own framing for where the interesting window should
   open.
2. **The record does not yet contain the community's own answer.** RFC
   3425's ratified text poses "should we stabilize together?" as an
   explicitly unresolved question tied to an explicitly unresolved bug
   (#112194); the stabilization PR that actually answers both (#115822)
   does not open until 2023-09-13, three months later. This is a genuine
   mid-flight window, not a moment where the outcome is already settled
   and only needs restating.
3. **A later cutoff (e.g. through 2023-06-14 21:52, letting the tracking
   issue's own restructuring into the fixture) was considered and
   rejected.** That edit would hand a tested agent the exact "should we
   stabilize this feature together with async fn" framing pre-packaged
   under a bolded "Unresolved Questions" heading, in the same document
   style this project's own SKILL.md and grading conventions use — making
   the convergence question something to transcribe rather than
   recognize. The chosen, slightly earlier cutoff still gives the tested
   agent the exact same underlying primary-source fact (it is present,
   verbatim, in RFC 3425's own ratified "Unresolved questions" section,
   which predates and does not depend on the tracking issue's later
   edit), but without the community's own subsequent bookkeeping act of
   re-filing it as a formal cross-referenced open question.
4. **An earlier cutoff (e.g. before RFC 3425 merged, or before #112194 was
   filed) was considered and rejected.** Before 2023-06-02 (when #112194
   was filed), the record supports Claims 1 and 2 above but nothing
   resembling Claim 3 — there would be no concrete, textually-linked
   convergence item at all, only the abstract, four-years-earlier "RPITIT
   is a building block for async fn" framing from RFC 3193 (2021). That
   would test claims 1/2 only, not the independence-then-convergence shape
   the research brief specifically asked for.
5. **A cutoff exactly at RFC 3425's own text was not "reached for" to
   manufacture a neat convergence moment** — it is where the two
   already-decided facts (a ratified RFC stating an interchangeability
   design goal, and a freshly filed, still-completely-uncommented-on bug
   report) happen to sit closest together in real time without yet having
   been formally connected by anyone. The connection the fixture asks a
   tested agent to draw (RFC 3425's stabilize-together question is
   explicitly tied, in the RFC's own text, to #112194's resolution; #112194
   is on its face an RPITIT-internal bug; AFIT's own mechanism is
   established, independently, as literally being RPITIT under the hood
   via #108309's quote and the shared `rustc_ast_lowering` file) is real
   and traceable, not invented for this cutoff.

## Which target dynamics this cutoff does and does not support

- **Genuine independently-executable work:** yes — #104689 (AFIT-only) and
  #111105/#109468 (RPITIT-only) have no stated cross-reference to each
  other, to the dual-labeled cluster, or to #112194/RFC-3425-QUESTIONS.
- **A stated design goal that predates its own concrete test case:** yes —
  RFC 3425's interchangeability goal (April 2023 draft, June 2023
  ratification) predates #112194 (filed June 2023) by weeks; the fixture
  can test whether a plan gets the direction of that relationship right
  (goal first, concrete soundness question later, not the reverse).
- **A shared, textually explicit, RFC-level convergence pairing:** yes —
  RFC 3425's own ratified "Unresolved questions" section names both the
  stabilize-together question and #112194's resolution side by side.
- **A dual-labeled bug cluster that is genuinely one ticket per bug, not
  two features' separate manifestations needing two fixes:** yes, for
  #108309 specifically (the "async fn in trait is just return position
  impl trait in trait" quote); more weakly for #108304 and #109016 (dual-
  labeled, but no comparable "same underlying bug" quote — see
  `grading/case-305.expected.md`'s DEFENSIBLE section for how this
  asymmetry is handled).
- **Already-landed work that should not remain in the open plan:** yes —
  both RFCs, the original implementation PRs, the feature-gate split, and
  (for AFIT specifically) its own now-resolved "Do we need Send bounds to
  stabilize async_fn_in_trait?" question (#103854, closed 2023-05-15) are
  all deliberately presented as context, not tasks.
- **A "joint stabilization is normative" trap:** yes, deliberately — this
  is the fixture's central intended trap, and per Claim 4/7 above, no
  REQUIRED item in the grading key treats the eventual joint stabilization
  PR (#115822, entirely DIAGNOSTIC, postdating cutoff by three months) as
  something a cutoff-time plan could or should have used.
- **A numeric-order illusion:** not well supported and not claimed — issue
  numbers here track filing chronology across both features interleaved
  (e.g. #108304 and #108309 were filed hours apart on the same day by
  different people about different things), and nothing in the record
  depends on reading numeric order as sequencing.
- **A community-external process blocker (case-302's DISCUSS-thread
  shape):** not present here — RFC 3425 already merged by cutoff; there is
  no open, blocking community governance thread in this window.

## Task count

Nine agent-visible items survive this audit: two AFIT-only bugs
(#104689, #110963), two RPITIT-only bugs (#111105, #109468), three
dual-labeled bugs that are each one ticket, not two (#108309, #108304,
#109016), one central convergence bug (#112194), and one convergence/
stabilization-readiness item drawn directly from RFC 3425's own ratified
"Unresolved questions" text (referred to as RFC-3425-QUESTIONS in
`tasks.md`). This sits at the low end of the research brief's own
8-16 target range. Two ways to pad this count further were considered and
rejected as manufacturing rather than reflecting evidence: (a) splitting
each of the three dual-labeled tickets into a separate "AFIT side" and
"RPITIT side" task, which would be exactly the task-identity-as-slice-
identity failure mode this fixture exists to test, applied to the fixture
construction itself rather than left for a tested agent to (hopefully not)
fall into; and (b) including the July-2023 crop of smaller AFIT/RPITIT
issues found during research (#113538, #113656, #113796, #114142,
#113794, #113903, #113929, #114145, #114274, #114601) — all postdate this
cutoff by three-plus weeks and, on their titles, read as smaller one-off
ICE/diagnostic reports rather than design-level items, consistent with the
research brief's own warning against turning this into "a Rust compiler
trivia exam." A later audit pass re-ran both labels' full issue history
(not just a date-bounded window) and surfaced three more candidates that
were open throughout this fixture's window but missing from the original
search methodology: #112047, #109464, #108580 (see `sources.md`,
"Excluded candidates") — all three are `I-ICE`/`glacier`-style crash
reports and are excluded on the same non-design-level basis as the
July-2023 crop, not folded into the nine-item count.
