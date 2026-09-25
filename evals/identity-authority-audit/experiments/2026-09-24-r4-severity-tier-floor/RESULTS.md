# identity-authority-audit — R4 severity/tier-floor intervention (2026-09-24)

**Status:** complete. One-paragraph intervention to `SKILL.md`'s Review
mode, targeted validation (n=5, case-102) at 4/5 pass, followed by a
4-case regression subset (n=1 each) since the targeted run cleared the
≥4/5 threshold. **Separate experiment artifact.** Does not overwrite or
supersede `evals/identity-authority-audit/RESULTS.md` (iteration-1),
`../2026-09-24-reliability-baseline/RESULTS.md` (original 80-run
with-skill/baseline experiment), `../2026-09-24-review-findings-fix/RESULTS.md`
(first post-fix rerun, n=5), or `../2026-09-24-case-102-stability-rerun/RESULTS.md`
(post-fix n=10 stability rerun, 2/10, the direct predecessor to this
experiment). All remain authoritative for what they cover.

## Setup

- **Base commit:** `63af571d7f8273d45224abcc1d220f792930e9a5`
  (`fix(identity-authority-audit): route unresolved existence-questions
  out of Findings`), plus one uncommitted working-tree edit to
  `skills/identity-authority-audit/SKILL.md` made in this experiment (see
  "Intervention" below). `git status` confirmed clean except for that one
  file throughout; the file was diffed against the frozen copy after all
  runs and found unchanged.
- **Frozen artifacts:** see `FREEZE-MANIFEST.md` and `CHECKSUMS.sha256`.
  Post-intervention `SKILL.md`, both references, case-102's five fixture
  files plus its grading key, the exact case-102 run prompt (built by
  taking the stability rerun's byte-identical frozen prompt and replacing
  only its embedded `SKILL.md` block — diffed to confirm the only changes
  are the new paragraph and one blank-line correction), and (added after
  Phase 3 passed) four more cases' fixtures, grading keys, and run
  prompts for the Phase 4 regression subset.
- **Isolation:** every run (case-102 ×5, regression cases ×4) was a
  freshly spawned, independent subagent with no shared context with this
  session, each other, or any prior run. Each subagent's prompt is fully
  self-contained (skill text, task, and complete evidence); each was
  instructed not to call any tool for the review itself. No run saw a
  grading key, sibling output, or any prior experiment's summary. Every
  raw response was saved unedited to `runs/`.

## Phase 1 — why the prior failure happened

`../2026-09-24-case-102-stability-rerun/RESULTS.md` found case-102 at
2/10, with **8/10 failures on R4 alone** (downstream-exploitability
consequence not capped at Likely/Ambiguity) and **T3 at 0/10** (the new
Findings/Open-questions admission rule was not implicated — it was doing
its job everywhere it was exercised). Reading the 10 failing transcripts
directly (not re-summarizing that experiment's own grading) showed a
single, consistent mechanism across 5 of the 8 R4 failures (category B,
"tier/severity collapse"):

- `SKILL.md` already had a paragraph (the "splitting has a floor" text,
  unedited by this intervention) that correctly says: if an unresolved
  fact could determine whether the claimed defect exists *at all*, the
  item is an open question, not a hedged finding; but if the unresolved
  fact only affects *how severe, scoped, or exploitable* the already-real
  defect is, Confirmed/Likely tier **remains available** for the
  structural fact.
- That paragraph is correct and was not the leak — every failing run's
  *tier* choice (Confirmed, for the structural code-level fact: no
  audience check present) was itself defensible per that rule.
- The leak was one level down: **nothing constrained the severity label**
  (HIGH/MEDIUM/LOW) attached to that Confirmed tier. HIGH's own
  definition ("a sensitive write reachable without appropriate
  authorization") is itself an exploitability claim — structurally the
  same kind of claim the tier-floor paragraph already polices for tier,
  but the paragraph never said the same floor applies to severity.
- The five failing transcripts show the identical move, verbatim in
  spirit each time: acknowledge, in the finding's own "Unresolved
  uncertainty" line, that reachability/exploitability is unresolved —
  then keep HIGH anyway, reasoning that the *structural* fact ("the
  application layer's own explicit disabling... is directly observed and
  true regardless of that fact") is what's Confirmed, as if that alone
  also confirmed HIGH's separate reachability claim. One run (`102-
  stability-08`) explicitly named MEDIUM as the honest alternative
  ("the practical severity drops... to a missing-defense-in-depth
  issue") and then didn't take it. The passing runs in that same batch
  (`102-stability-03`, `-07`) used almost identical "missing defense in
  depth, independent of whether it's currently exploited" language but
  correctly landed on MEDIUM (or dropped tier to Likely and kept HIGH) —
  the discriminator between pass and fail in that batch was exactly this
  severity-selection step, nothing else.
- This is a leak of **confidence in a premise into confidence in a
  derived consequence**, routed through the severity axis rather than the
  tier axis — exactly the category the task's diagnostic checklist named,
  and distinct from HIGH-vs-evidence-confidence conflation in the
  abstract: severity and tier are two separate scales in `SKILL.md`
  already (a coarse consequence label is explicitly "not... a score" and
  is defined independently of Confirmed/Likely/Ambiguity), but nothing
  in the text stopped severity from smuggling back in exactly the
  uncertainty tier had already correctly excluded from Confirmed.

**Narrowest intervention point identified:** the severity-definition
section itself (where HIGH/MEDIUM/LOW are defined in Review mode), not a
new conceptual subsystem, not the tier-floor paragraph's own wording
(which is correct as written and ungoverning of severity), and not a
case-102-specific rule.

## Phase 2 — the intervention

One paragraph inserted into `skills/identity-authority-audit/SKILL.md`'s
Review mode, immediately before the existing HIGH/MEDIUM/LOW bullet list,
extending the same floor the adjacent tier-selection paragraph already
states to the severity label that follows it:

> The same floor applies here, not only to tier: a severity level's own
> wording can quietly reassert the exact exploitability the paragraph
> above just excluded from Confirmed. HIGH's "reachable... without
> appropriate authorization" is itself an exploitability claim -- don't
> reach for it on the strength of a Confirmed structural fact alone when
> reachability is exactly what's unresolved. Pick the level whose own
> definition matches only what's actually confirmed (often MEDIUM's
> "missing defense in depth"), or keep HIGH by carrying the finding at
> Likely instead, where the tier itself already carries that inference. A
> Confirmed tier and an unearned HIGH are not a shortcut around naming the
> same uncertainty twice -- they're the uncertainty being paid for once
> and spent twice.

Nothing else in `SKILL.md` was changed. `git diff` (below) is the entire
edit:

```
$ git diff --stat skills/identity-authority-audit/SKILL.md
 skills/identity-authority-audit/SKILL.md | 13 ++++++++++++-
 1 file changed, 12 insertions(+), 1 deletion(-)
```

Confirmed untouched: case-102 fixtures, the grading key, the admission
rule and Open-Questions routing (the two paragraphs immediately above the
edit point), and every other rubric item (R1, R2, R3, R5, R6, R7, T3).

### Why this is general, not case-102-specific

- The paragraph names no fixture fact (no `aud`, `verify_aud`, gateway,
  token, audience, MCP, or any case-102 vocabulary). It is phrased
  entirely in the skill's own pre-existing terms: Confirmed, HIGH,
  reachability, exploitability, MEDIUM's own "missing defense in depth"
  wording, Likely.
- It reuses an existing rhetorical/logical pattern already in the file
  (the tier-floor paragraph immediately above it) rather than introducing
  a new kind of rule, dimension, or report section.
- It keeps the four dimensions the task asked to keep separate — evidence
  confidence/tier, severity, exploitability, recommendation priority —
  strictly separate: it does not change what counts as Confirmed, does
  not touch recommendation/next-step language, and explicitly preserves
  two independent ways a finding can carry HIGH (reachability actually
  evidenced, or tier dropped to Likely) rather than banning HIGH outright.
- Phase 4 (below) tests it against four cases with no textual, domain, or
  fixture-author overlap with case-102 (UI-authorization, async-worker
  authority, agent tool-dispatch, and Vault/Postgres credential scoping)
  and it holds in that domain-general form, including one case (112)
  whose grading key had already been independently corrected, before
  this experiment, to state almost exactly this same principle in its
  own words.

## Phase 3 — targeted validation (case-102, N=5)

| Run | Verdict | R4 outcome |
|---|---|---|
| r4-floor-01 | **PASS** | Confirmed/MEDIUM on both findings |
| r4-floor-02 | **FAIL** | Confirmed/HIGH kept despite own hedge conceding reachability unresolved, plus absence-as-proof reasoning in System shape |
| r4-floor-03 | **PASS** | Confirmed/MEDIUM on both findings |
| r4-floor-04 | **PASS** | Confirmed/MEDIUM on both findings |
| r4-floor-05 | **PASS** | Confirmed/MEDIUM on both findings, explicitly citing the new rule's own reasoning |

**Result: 4/5 (80%) pass** — full grading in `grading_out/case-102-r4-floor.md`.
Every other required item (R1, R2, R3, R5, R6/R7) was met in 5/5 runs;
R4 is the only item any run failed, and T3 (admission-rule/Open-Questions
misfire) fired in 0/5 — the mechanism this intervention was told not to
touch was not disturbed.

Per the predeclared bands, 4/5 clears the "sufficient to justify moving
to broader regression testing" threshold. Per instruction, this run was
not repeated or tuned against — one pass at n=5, graded, reported as-is.

### R4 behavior per run

- **r4-floor-01, -03, -04, -05 (pass):** all four used the same path —
  Confirmed tier retained for the structural fact (no audience check /
  no scope check in code), severity capped at MEDIUM, with reachability
  named as an honestly-scoped, separate uncertainty. r4-floor-04 and -05
  independently echo the new paragraph's own reasoning almost verbatim
  ("a missing layer of defense in depth," "HIGH would require confirming
  the mismatched-audience token is actually reachable... which the
  evidence doesn't settle") without having been given that reasoning
  directly — the case prompt embeds the full post-intervention skill, but
  no explanation of *why* the paragraph was added.
- **r4-floor-02 (fail):** reproduces the exact pre-intervention category-B
  signature — Confirmed/HIGH kept while the finding's own "Unresolved
  uncertainty" line states plainly that no evidence establishes
  application-level audience enforcement. It additionally shows a
  category-A (absence-as-proof) move in its "System shape" section,
  claiming evidence completeness "removes the usual 'maybe a gateway
  checks it' hedge" — a distinct failure mode this intervention was not
  designed to touch, and didn't. The run is also internally inconsistent
  (that same claim is contradicted two sections later by its own Open
  Questions entry on the identical fact), independent of the new
  paragraph's presence.

### T3 / other rubric regressions

**T3: 0/5.** No run in this batch demoted a Confirmed structural fact
into Open Questions, and no run smuggled a genuinely unresolved
existence question into Findings under a tier. R1, R2, R3, R5, R6/R7:
5/5 met in every run. No regression on any rubric item this intervention
was not targeting.

## Phase 4 — regression subset (N=4 cases, n=1 each)

### Regression subset selection

Triggered because Phase 3 cleared 4/5. Four existing cases were chosen —
no synthetic fixtures were written — specifically because each is the
highest-risk existing case for the failure mode this phase exists to
catch (a genuinely-Confirmed/HIGH finding wrongly suppressed to MEDIUM or
Likely by the new severity floor), while collectively covering the four
dimensions named in the task:

- **case-105** (`ui-only-authorization-no-server-check`) — a genuine
  Confirmed/HIGH finding where reachability is not merely structural but
  *directly reproduced* (the support engineer's own replay). The single
  cleanest test that the new paragraph does not suppress HIGH when
  reachability is actually evidenced, not just structurally suggestive.
- **case-109** (`read-write-capability-boundary-metadata-only`) — a
  second genuine Confirmed/HIGH finding, this time via a confirmed
  *uniform* gate (the approval step is directly shown to apply identically
  regardless of the `destructive` flag), i.e. reachability established
  through code-level uniformity rather than an observed exploit replay —
  a different evidentiary route to the same "reachability is actually
  shown" test, plus severity independent of confidence (a second,
  distinct capability-boundary finding at MEDIUM in the same report).
- **case-112** (`secret-manager-mechanics-vs-resulting-service-authority`)
  — the case whose own grading key was, independently of this
  intervention, already corrected on this same date to demand almost
  exactly the reasoning this paragraph adds (a prior "HIGH credited by
  analogy to case-105" note was retracted because "reachability is
  exactly the fact HIGH turns on here"). The single highest-risk case in
  the entire repository for this specific change, since it's the case
  most textually entangled with the exact distinction being tightened —
  and a different domain (secrets/database-privilege scoping) than
  case-102's network/audience pattern, testing generality.
- **case-108** (`user-to-workload-authority-frozen-at-enqueue`) — the
  case that historically motivated the adjacent tier-floor paragraph this
  intervention builds on (see that paragraph's own history in
  `evals/identity-authority-audit/RESULTS.md`'s "SKILL.md correction"
  section). Chosen to check whether the canonical Likely/HIGH-or-MEDIUM
  answer this case calls for is still reachable post-intervention.

Not run: the full 13-case suite (unnecessary per instruction — this
selection already targets the highest-risk cases directly) and any
synthetic addition (none needed; four real, pre-existing cases already
cover the four required dimensions).

### Results

| Case | Verdict | Detail |
|---|---|---|
| 105 | **PASS, no regression** | Confirmed/HIGH kept, unhedged, where reachability is directly proven; sibling finding correctly uses Likely (not a MEDIUM downgrade) to carry an inferred-but-unproven instance of the same pattern. |
| 108 | **MISS, not attributable to this intervention** | Confirmed/HIGH kept where the key wants Likely — a **tier** miss (governed by the pre-existing, unedited admission-rule paragraph), not a severity miss. Reproduces the identical failure shape this case exposed against the *pre*-admission-rule skill in the original iteration-1 suite. |
| 109 | **PASS, no regression** | Confirmed/HIGH kept, matching the key exactly, where reachability is established via a confirmed uniform gate; two further Confirmed/MEDIUM findings correctly non-HIGH. |
| 112 | **PASS, exact match** | Confirmed/MEDIUM, matching the key's own (independently, previously corrected) verdict, with reasoning that echoes the new paragraph almost verbatim in a non-network domain. |

Full detail in `grading_out/regression-subset.md`.

**No case showed a genuinely-Confirmed/HIGH finding wrongly suppressed to
MEDIUM or Likely** — the specific damage pattern this phase exists to
check for did not occur in this subset. The one miss (case-108) sits on
the tier axis the pre-existing admission-rule paragraph governs, not the
severity axis this intervention edited, and reproduces a previously
documented, case-specific fragility rather than a new one.

## Comparison

| Stage | Skill state | Case | n | Pass rate |
|---|---|---|---|---|
| Original reliability experiment | pre-fix | 102 | 10 | 8/10 (80%) |
| First post-fix rerun | post-fix (admission rule) | 102 | 5 | 3/5 (60%) |
| Stability rerun | post-fix (admission rule), same SHA | 102 | 10 | 2/10 (20%) |
| **This intervention** | post-fix + severity floor | 102 | 5 | **4/5 (80%)** |
| This intervention, regression subset | post-fix + severity floor | 105, 108, 109, 112 | 1 each | 3/4 pass (108 a pre-existing-shape miss) |

Pooled post-admission-rule-fix, pre-this-intervention record on case-102:
5 passes / 15 runs (33%). This intervention's 4/5 sits back at the
pre-fix 80% baseline, on the same rubric, under the same isolation
method, at a fifth of the pre-fix experiment's sample size — a single
n=5 batch is not proof at that resolution, but it directly reverses the
2/10 credible-regression signal the prior experiment flagged, on the
exact rubric item (R4) that signal was about.

## Recommendation

**Keep.**

- The targeted case-102 result (4/5) clears the predeclared band and
  reverses the specific R4 degradation the prior stability rerun
  documented, without touching T3 or any other rubric item (0/5 and 0/5
  regressions respectively across Phases 3 and 4).
- The regression subset shows no instance of the specific damage pattern
  this phase was built to catch (a genuine Confirmed/HIGH wrongly
  suppressed), across two different evidentiary routes to "reachability
  is actually established" (case-105's direct reproduction, case-109's
  confirmed-uniform-gate) and one case (112) where the new paragraph's
  reasoning was independently, externally validated by the case's own
  (previously corrected) grading key in a different domain.
- The one miss (case-108) is on a different axis than the one this
  intervention edited, reproduces a previously documented failure shape
  on that specific case, and is reported here as an open, un-addressed
  fragility in the existing tier-selection (admission-rule) text — not
  evidence against this change, and not something this intervention was
  scoped to fix.
- This was a single, ~90-word, non-case-specific addition to an existing
  rule, reusing existing vocabulary — the smallest defensible
  intervention point identified in Phase 1, with no new conceptual
  subsystem introduced.

**Not revert. Not further revise at this time** — n=5 plus a 4-case
regression subset is enough to justify keeping this change and carrying
it forward, but is not itself proof at a resolution that would justify
declaring the underlying R4 fragility fully closed; a future,
independent n=10 rerun of case-102 (mirroring the stability rerun's own
methodology) would be the natural next check before treating this as
settled, and case-108's tier-axis miss is worth a dedicated look as a
separate, distinct piece of work.

## Did this improve the underlying epistemic rule, or merely make
## case-102 easier to grade correctly?

**The former, with real but bounded evidence.** Three facts support this
over the "made case-102 easier" alternative:

1. **The paragraph contains no case-102 vocabulary** — it was written
   from the general failure mechanism (severity smuggling back in a
   reachability claim the tier floor already excluded), independently of
   any specific fixture fact, and was checked for case-specific language
   before being finalized (Phase 2's "why general" section).
2. **It generalizes to a structurally different domain under the same
   reasoning.** Case-112 tests network-audience reasoning not at all —
   it's about database-privilege over-scoping — and the post-intervention
   run lands on the correct answer using language that mirrors the new
   paragraph's own phrasing almost exactly, independently arrived at by
   the model from the general rule, not from anything case-102-shaped.
   That the correct answer for case-112 was *already*, independently
   corrected in its own grading key (before this experiment ran) to state
   nearly the same principle is external confirmation this is a real,
   general epistemic distinction the skill was under-specifying — not an
   artifact invented to make one fixture pass.
3. **It did not touch case-102's own admission-rule mechanism at all**,
   and case-105/109's genuinely-Confirmed/HIGH findings still land
   correctly post-intervention — if this were merely a case-102-shaped
   patch, the more likely failure mode would be collateral suppression of
   legitimate HIGH findings elsewhere, which Phase 4 was specifically run
   to check for and did not find.

The bound on this conclusion: n=5 on the target case and n=1 per
regression case is real evidence, not proof, of the underlying rule
being sound at scale — and case-108's tier-axis miss shows at least one
adjacent piece of the skill's tier-selection discipline (not the piece
this intervention edited) remains fragile on its own, independent
history. This experiment answers "did this specific change generalize
and avoid the specific damage it was checked for" — yes — not "is
case-102's or this skill's tier/severity discipline now fully reliable,"
which it does not claim.

## PR hygiene

This experiment adds only its own directory
(`evals/identity-authority-audit/experiments/2026-09-24-r4-severity-tier-floor/`)
plus the one `SKILL.md` edit described above. No case-102 fixture, no
grading key (case-102 or the four regression cases), the admission rule,
Open Questions routing, or any unrelated eval file was modified, moved,
or deleted. No prior experiment's `RESULTS.md` or `runs/` content was
touched.
