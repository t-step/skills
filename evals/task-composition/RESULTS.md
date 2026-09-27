# task-composition — eval results

**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per run, default settings.
**Harness:** one subagent per run, cwd'd into an isolated scratch copy of the case fixture (so it can't see this repository, any other case, or the skill unless directed to it); with-skill runs additionally instructed to read and follow `skills/task-composition/SKILL.md`; graded by the orchestrating session against `evals/task-composition/evals.json`, `pressure-tests/pressure_evals.json`, and (new in iteration 2) `triggering-tests/triggering_evals.json`. Raw outputs are saved verbatim under `runs/<date>-iteration-<n>/`; every claim below cites one of those files.

This skill has had three eval iterations. Iteration 1 established the skill and its core eval suite. Iteration 2 (2026-08-26) strengthened the shared-file/parallelism wording based on iteration-1 evidence, added the deferred eval categories, fixed one under-specified answer key (case 006) and one overly rigid one (case 010), and repeat-sampled the adversarial pressure case. Iteration 3 (2026-08-26) sharpened the skill's core definition of a vertical delivery slice around "what independently meaningful behavior becomes true and is verifiable," added four new eval cases targeting that distinction, and — based on evidence from those new cases — made two further SKILL.md wording refinements mid-iteration, both re-verified. See "What this does and does not prove" at the end before treating any of this as validation — this remains an experimental skill.

## Iteration 1 (2026-08-25) — summary

7 regression cases (one per required scenario category from the design brief) + 1 pressure case, 1 run per case per condition. All 8 with-skill runs met their written expectations (29/29 regression expectations + 5/5 pressure expectations). Full case-by-case detail is preserved in git history for this file; the short version:

- A capable baseline (same model, no skill) reached substantively similar slice boundaries to the with-skill run on 6 of 8 cases (001, 002, 003, 005, 006, 007's core pick) — not a failure, but it means the skill's iteration-1 evidence was concentrated in explicit structure, explicit enabler/risk justification, naming numeric-order mismatches explicitly, and refusal discipline under pressure, not in "baseline gets the topology wrong."
- Case 101 (pressure) was the cleanest single with/without contrast: the baseline reasoned well but partially complied with a "maximize agent utilization" request by inventing an unstated branch-isolation-plus-merge workaround to make 3-way same-file editing look safe; the with-skill run declined the framing and reported the real (near-zero) safe parallelism.
- Case 006 (risk boundary) surfaced a genuine answer-key defect: the original key implicitly required downstream slices to gate on the risk-boundary slice's *verification*, but the source plan doesn't actually settle that (the interface is stated to stay the same) — flagged then, fixed in iteration 2 (see below).

## Iteration 2 (2026-08-26)

### Skill wording change: shared-file parallelism nuance

Iteration 1's case 101 showed a baseline (not the skill) treating "isolated branches + a later merge" as sufficient justification for parallelizing same-file, same-class edits. The skill's own text didn't yet make explicit that shared files are a *signal to look closer*, not an automatic serialize-or-allow verdict either way, and didn't name branch isolation's actual limit (it defers a conflict to merge time, it doesn't remove it).

Added to `SKILL.md`'s "Assess safe parallelism" section: shared files/interfaces are a signal, not a verdict — two slices touching the same file in independent, stable, extension-point regions with a predictable merge can still be parallel-safe; two slices touching the same file or contract where the interface is unsettled or the changes overlap in meaning are not parallel-safe regardless of branch isolation. Added one refusal-list bullet naming branch/workspace isolation plus a later merge as insufficient justification on its own for parallelizing semantically overlapping work. No other wording was changed — the existing "vertical slice," "horizontal enabler," "convergence," and report-format vocabulary was left as-is, since none of it was made misleading by the rename or this addition.

**Direct evidence the wording is load-bearing, not decorative:** both new case-101 with-skill samples in this iteration cite it near-verbatim while refusing the utilization request — "Isolation plus a later merge doesn't remove that conflict, it just moves it to merge time — and per the skill's parallelism criteria..." (`case-101-skill-sample1.md`) and "this is contention, not independence, so splitting them would violate the same-file-unsettled-region rule even under branch isolation" (`case-101-skill-sample2.md`).

### New eval coverage (cases 8–11 + triggering suite)

All four deferred categories from the design brief were added, plus a triggering suite (no existing repo framework for one was found; this suite reuses the existing case/manifest/grading shape rather than inventing a new one — see `triggering-tests/README.md`).

| Case | Scenario | With-skill | Baseline |
|---|---|---|---|
| 8 | shared-file, genuinely safe (positive contrast) | 4/4 met | Also correct — reached the same 2-slice, parallel-safe conclusion independently |
| 9 | shared-file, genuinely unsafe (negative contrast) | 4/4 met | Also correct — serialized, no branch-isolation workaround proposed |
| 10 | actual dependency cycle | 4/4 met (revised key, see below) | Named the cycle too (and a sharper defect — see below), but oversteps scope |
| 11 | mixed realistic plan (5 dynamics at once) | 5/5 met | Also correct — matched the with-skill shape closely, including the easy-to-miss S4/queue independence |
| 101 (pressure) | repeat sample 1 of 2 | 5/5 met | (baseline not re-sampled; iteration-1 baseline result stands) |
| 101 (pressure) | repeat sample 2 of 2 | 5/5 met | — |

**Case 8 (`case-008-skill.md` / `case-008-baseline.md`):** both runs proposed export (T1+T3) and import (T2+T4) as two slices despite both touching `cli/commands.py`, both explicitly named the shared file, and both grounded parallel-safety in the fixture's stated extension pattern rather than in branch isolation. This and case 9 are both cases where a capable baseline handled the shared-file nuance correctly on its own — the failure mode this eval category targets (treating isolation-plus-merge as sufficient justification) showed up in iteration 1's baseline only under direct "maximize utilization" pressure (case 101), not from shared-file structure alone. Worth stating plainly: this narrows, but doesn't erase, the case's value — the with-skill run's reasoning is more explicit and structurally consistent (`Kind: vertical delivery`, named criteria) even where the baseline's conclusion matches.

**Case 9 (`case-009-skill.md` / `case-009-baseline.md`):** both runs correctly kept T1/T2 in one slice, grounded in the fixture's stated fact that T2's value depends on T1's result, and neither proposed isolated branches as a workaround. Clean pass for both; same "baseline already competent here" pattern as case 8.

**Case 10 (`case-010-skill.md` / `case-010-baseline.md`):** the with-skill run named the T1/T2 cycle explicitly under Topology issues, presented no false cross-slice ordering, and resolved it by keeping T1+T2+T3 in one slice — while noting a further concern (the descriptions look like literal infinite recursion at runtime, not just a build-order problem) as a risk to flag, explicitly declining to fix it ("This skill's scope is grouping the given tasks, not rewriting them... task content is left as-is"). The baseline noticed the same deeper defect (independently, and described it in more operational detail — "RecursionError / stack overflow") but then crossed a real scope line: it proposed an actual design fix (a new non-circular base value) and treated implementing that fix as part of the deliverable ("that resolution is part of the slice's work, not a separate follow-up"). This is a genuine, useful differentiator: the with-skill run surfaced the same problem while staying inside "compose already-decomposed work," which is exactly the boundary this skill exists to hold; the baseline, with good intentions, redesigned the plan.

The original case-10 answer key required the skill to "refuse to produce a credible execution composition until the cycle is resolved." Iteration-2 evidence showed that requirement was too rigid for a cycle this small: co-locating two tightly-coupled tasks into one slice (with the cycle still named, not silently absorbed) is a legitimate, non-over-conservative resolution, not a dodge — refusing to produce any plan at all for two tasks this size would itself be the over-conservative failure mode the evaluation standard warns against. The key was revised to grade on three required properties (name the cycle; no false cross-slice ordering; cycle visible under Topology issues) plus one explicitly-defensible, not-pass/fail choice (co-location vs. refusal), rather than mandating refusal as the only correct outcome. This is a fix to the eval specification, not a skill change — the skill's actual behavior (name it, don't invent an order, don't redesign) was already correct against the more honest standard.

**Case 11 (`case-011-skill.md` / `case-011-baseline.md`):** the with-skill run correctly composed all five dynamics at once — signing as a horizontal enabler (justified against all three of the skill's own criteria), Slack/email as parallel-safe verticals depending on the enabler, the delivery queue as a risk-boundary slice correctly recognized as *independent* of the enabler (the fixture's intended trap — it's easy to wrongly serialize "infrastructure" behind other "infrastructure"), dispatch as a three-way convergence, and the T1/T2-reference-T4 numeric-order mismatch named explicitly. The baseline reached an equivalent structure independently, including the queue's independence. As with cases 8/9, this shows a capable baseline can assemble a correct shape even for a plan combining several dynamics at once — the with-skill run's value here is again explicitness (each slice's "why grouped" ties back to one of the skill's own named criteria) rather than a different conclusion.

**Case 6, re-run against the updated skill (`case-006-skill-rerun.md`):** under the revised, honestly-scoped answer key (see "Revisited: case 6" below), this run bundled T1+T5 into one horizontal-enabler slice and explicitly hard-gated T2/T3/T4 on it, including its verification ("treat 'T5 passes' as a hard gate, not a formality") — a different bundling choice than iteration 1's with-skill run (which split T1 and T5 into two slices and gated migrations only on T1's implementation), but both choices fall inside the revised key's defensible range, and both were explicit about the choice made rather than silent about it. Read together, the two runs are evidence the skill reliably produces *an* explicit, reasoned choice on this ambiguous point rather than a consistent single answer — which is what the revised key now actually asks for.

### Revisited: case 6

See above — the answer key was under-specified (conflated "T2/T3/T4 depend on T1's implementation," which the source plan requires, with "T2/T3/T4 must wait for T5's verification to pass," which it doesn't settle). Fixed by splitting the expectations into required / defensible-either-way-but-must-be-stated / wrong, matching this repository's `slice-review`-style discipline of not crediting a brittle key over the actual source material. Not a skill change.

### Repeated sampling: case 101 (adversarial pressure)

3 total with-skill samples now exist for this case (1 from iteration 1, 2 new in iteration 2). All three declined the "one agent per task" framing, all three reported the real available parallelism as zero (or effectively one branch), and none proposed a branch-isolation-plus-merge workaround to manufacture the requested parallelism. This is a small sample (3), sufficient to say the refusal behavior looks stable rather than a one-run accident, not sufficient to claim a rate with any statistical confidence — see "What this does not prove."

### Triggering suite (new)

6 cases, 1 run each, graded against `triggering-tests/triggering_evals.json` and `grading/triggering-results.expected.md`. Methodology: a fresh agent is given only `candidates.md` (task-composition's, next-best-slice's, slice-plan's, and repo-orientation's frontmatter descriptions — nothing else) and one natural-language request, then asked which skill it would invoke.

| Case | Request | Result |
|---|---|---|
| 201 | "How should these tasks be grouped into agent assignments?" | Selected task-composition. Pass. |
| 202 | "Which of these tasks can run in parallel?" | Selected task-composition. Pass. |
| 203 | "Turn this task plan into agent-sized work packages/sessions." | Selected task-composition. Pass. |
| 204 | "Which task should I do next?" | Selected "none" (reasoned that next-best-slice's own stated precondition — a just-reviewed/retrospected slice — isn't established either). task-composition correctly NOT selected: pass on the axis this suite actually tests. The manifest's `expected_trigger: next-best-slice` was this skill-author's prediction of the "natural" real-world answer, not itself the pass/fail criterion for task-composition's own evaluation; noted as a fixture nuance, not a failure. |
| 205 | "Plan the implementation of T024." | Selected slice-plan. Pass. |
| 206 | "Break this spec into tasks." | Selected "none," citing task-composition's own explicit "does not decompose a spec into tasks." Pass. |

6/6 on the core axis (task-composition triggers on 201–203, does not on 204–206). All raw outputs in `runs/2026-08-26-iteration-2/triggering-201-206.md`.

## Iteration 3 (2026-08-26)

### Skill wording change: "meaningful behavior becomes true," not technical-layer completion

Iterations 1–2 established that this skill reasons soundly about dependencies, parallelism, horizontal enablers, convergence, risk, and checkpoint boundaries. What its prose didn't yet make explicit was the *test* for what makes a grouping a real vertical delivery unit in the first place — several sections still leaned on "coherent," "layer," and "files touched" language without first asking what the grouping actually delivers. Per an explicit design brief, this iteration sharpened that definition around one question: **what independently meaningful behavior, capability, or system property becomes true once this grouping lands and passes verification?**

Five sections of `SKILL.md` were revised (see the file's git history for exact diffs):

1. **Introduction** — added a paragraph stating the "what becomes true" framing directly: a slice is defined by what someone can now rely on, verify, or build on top of, not by which files or layer it touches.
2. **"Task IDs are not session boundaries"** — the "right size" sentence now names the become-true/verifiable framing instead of only "coherent, independently verifiable unit of behavior."
3. **"Prefer vertical slices"** — gained two new subsections: **"The vertical grouping test"** (three questions: what becomes true, can it be verified independently, would a reviewer understand why it matters without being told only the technical layer) with worked examples matching the design brief's own ("the runtime can now select and reject execution-provider configuration correctly" vs. "adds config schema and validation"), and **"Not every grouping needs to be user-facing"** (isolation guarantees, validated configuration behavior, provider dispatch capability, lifecycle correctness, authorization boundaries, compatibility guarantees, integration contracts, and recovery behavior are all named as valid, non-product-facing "becomes true" claims — explicitly warning against forcing artificial product wording onto genuinely internal work).
4. **"Allow horizontal enablers, narrowly"** — added the absorbable-enabler diagnostic: *could this work be absorbed into one downstream vertical grouping without duplication, unsafe coupling, or materially reducing useful parallelism? If yes, it probably shouldn't be a standalone horizontal enabler* — framed as judgment guidance, not a hard rule, per the design brief's explicit instruction.
5. **Report format's `Delivers:` line** — now asks for "the independently meaningful behavior, capability, or system property that becomes true... phrased as what can now be relied on or verified, not which technical layer or files changed."

Sections the brief asked to preserve — safe parallelism, same-file nuance, convergence, risk/checkpoint boundaries, bounded topology validation, scope/refusal discipline, and the closed report format's other fields — were left unchanged, since none of them centered on layer/file language in a way the brief flagged.

**Two further refinements were needed mid-iteration, both driven by first-run evidence from the new eval cases below, not speculation:**

- **Verifiability-folding rule.** The first version of the vertical grouping test named the *questions* but didn't say what to do when a proposed sub-grouping fails question 2 (independent verifiability). Two fresh with-skill samples of the new case-014 fixture (2/2, see below) and the existing case-006 fixture's rerun exploited that gap: a migration task with only one real downstream feature got elevated to a standalone horizontal enabler by counting two *mechanically* separable but *unverifiable-alone* pieces of that one feature as two "downstream consumers." Added: a grouping that fails question 2 gets folded into whichever grouping actually establishes and verifies the combined behavior, and doesn't count as a second consumer for horizontal-enabler purposes. Reran case-014 and case-006 fresh against the fix: both now match their keys exactly (case-014: one coherent slice, explicitly citing the new wording; case-006: T1 re-bundles with its own verification T5). Spot-checked case-002 and case-013 (both legitimate, real two/three-consumer enablers) and reran case-011 fresh to confirm the fix didn't over-correct — all three still isolate their enablers correctly.
- **"Predicted to fail" carve-out.** The verifiability-folding rule, applied too broadly, then caused case-010 (the actual-dependency-cycle case) to refuse producing any slice plan at all — correctly diagnosing that T1/T2's described computation has no valid base case (`Order.total = Order.total + tax + fees`, textually grounded in the fixture), but total refusal directly contradicts that case's own already-revised answer key, which explicitly names refusal as the over-conservative failure mode for a cycle this small. Added a clarifying sentence: the verifiability question is about whether the plan *specifies a verification path*, not whether that verification is *predicted to pass* — a plan pairing tasks with a test that would exercise them together should be composed normally, with a suspected defect named as a risk, never used to block producing a plan. Reran case-010 fresh: now composes T1+T2+T3 into one slice, names the cycle under Topology issues, and flags the recursion concern as a risk — matching the key on all points.

This mid-iteration correction loop is itself evidence worth stating plainly: the first version of a verifiability principle can be simultaneously under-specified (case-006/014) and, once patched, over-broad (case-010) in the same small evidence set. Both corrective edits were verified by fresh reruns before being treated as settled, and no eval fixture or grading key needed to change to accommodate them — both keys were already correct; only the skill's wording was.

### New eval coverage (cases 12–15)

Four new regression cases were added, one per requested failure mode, following the existing `cases/`/`grading/` isolation convention (numeric-only directory names; scenario labels live only in `evals.json` and `grading/*.expected.md`, never in agent-visible `tasks.md` files — reverified by `scripts/check-eval-isolation.py`, which passed with 175 case directories across 12 skills, no leakage).

| Case | Scenario | With-skill | Baseline |
|---|---|---|---|
| 12 | technical-layer-batch-temptation | 5/5 met | Fell into the fixture's designed trap |
| 13 | legitimate-horizontal-enabler-behavior | 5/5 met (original + post-fix spot-check) | Also correct, independently |
| 14 | internal-capability-not-user-facing | 2/5 required points failed on 2/2 pre-fix samples; 5/5 met post-fix | Fell into a different, sharper trap (full fragmentation) |
| 15 | absorbable-pseudo-enabler | 5/5 met | Partially fell into a softer version of the same trap |

**Case 12 (`case-012-skill.md` / `case-012-baseline.md`):** a webhook-subscription plan (API handler + validation + storage write + wiring + read endpoint + combined test) where an API-layer/storage-layer split is tempting — and where the fixture itself states that before the wiring task lands, the API "returns success without writing anything." The with-skill run kept all six tasks in one slice, explicitly reasoning that a layer split would leave the API-only grouping "a known-incomplete, not-yet-trustworthy state, not a checkpoint worth shipping or verifying on its own," and phrased its `Delivers:` line as the observable capability (create-and-retrieve-with-validation), not "adds webhook API endpoints." The baseline fell precisely into the trap the fixture was built to test: it split into 5 slices and explicitly cited the fixture's own "returns success without writing" sentence as if the plan's author had "pre-approved" shipping that intermediate, non-persisting state as its own deliverable slice — a clean, reproducible illustration of layer-completion being mistaken for a real checkpoint.

**Case 13 (`case-013-skill.md` / `case-013-baseline.md`, spot-check `case-013-skill-postfix-spotcheck.md`):** three admin endpoints (cache purge, reindex, key rotation) all gated by one shared HMAC-signature verifier. The with-skill run correctly isolated the verifier as a horizontal enabler, named all three downstream consumers by name (not just one), grounded the justification in the fixture's own stated duplication/drift-risk cost, and marked the three endpoint slices parallel-safe with each other. The baseline reached the same shape independently and unprompted — this fixture's genuine-enabler contrast, unlike case-12's trap, is one a capable baseline also gets right, consistent with this project's recurring finding (iterations 1–2) that baseline competence on non-adversarial cases doesn't diminish the skill's value in explicit, criteria-traceable rationale.

**Case 14 (`case-014-skill-sample1.md`, `case-014-skill-sample2.md`, `case-014-skill-postfix.md` / `case-014-baseline.md`):** a purely internal worker-crash-recovery feature (heartbeat column, periodic heartbeat writes, a reclaim function, wiring it into startup, one end-to-end test) with no user-facing surface at all. This case did double duty: it validated the intended principle (a non-user-facing system property is valid vertical delivery) and, on its first two samples, surfaced the verifiability-folding gap described above (both samples elevated the migration to a 2-consumer horizontal enabler and split heartbeat-writing into its own "vertical delivery" slice despite that slice admitting, in its own risk field, that nothing in the plan tests it independently). The post-fix rerun corrected this while the parts that were already right stayed right: one coherent slice, `Delivers:` phrased as "a worker that crashes mid-job no longer loses that job... reclaimed and reprocessed," explicit recognition that this is valid vertical delivery "despite having no user-facing/product surface," and no invented dashboard/UI framing anywhere across all three with-skill samples. The baseline's failure mode was sharper than case-12's: it fragmented the five-task plan into five single-task slices, explicitly reasoning "I did not find a good reason to merge any two of them" — the "one slice per task" anti-pattern this skill's "Task IDs are not session boundaries" section exists to name, reproduced verbatim by an unguided baseline on internal, non-obviously-vertical work.

**Case 15 (`case-015-skill.md` / `case-015-baseline.md`):** a small PDF-export feature (renderer interface, its one implementation, an endpoint, a test) where the interface+implementation pair looks architectural enough to tempt standalone-enabler treatment, but the fixture states plainly there's only one consumer. The with-skill run kept all four tasks in one slice, explicitly applying the absorbable-enabler question ("only one downstream consumer (T3) exists, so isolating them unlocks no additional parallelism and avoids no duplication") and declining to give the interface split independent status. The baseline split into three layer-based slices (renderer foundation / endpoint / test) — not quite the full standalone-enabler trap case-12/14 targeted, but the same underlying instinct to separate by technical layer even inside a fully linear, single-consumer chain.

### Repeated sampling: case 101 (adversarial pressure)

A fourth with-skill sample (1 from iteration 1, 2 from iteration 2, this one) again declined the "one agent per task" framing and reported zero available slice-level parallelism, this time citing the new vertical-grouping-test wording directly: "every task in this list fails the vertical grouping test's verifiability question when considered alone." 4/4 with-skill samples across iterations now hold the same line.

### Triggering suite

Rerun in full (6 cases) for completeness against this iteration's validation checklist, though the frontmatter `description` — the only thing this suite exercises — was not touched by any of this iteration's edits. Result: 6/6 on the core axis, identical to iteration 2's result including the case-204 nuance.

## Cumulative numeric summary (all three iterations, recomputed from the manifests at write-up time)

- Regression suite: 66 expectations across 15 cases in `evals.json` (46 across the original 11 + 20 across the 4 new iteration-3 cases). With-skill runs against the final SKILL.md exist for all 15; all 15 cases' expectations were met on their final run (case-006, case-010, and case-014 required a mid-iteration SKILL.md fix and a fresh rerun before matching — see above; cases 1–5, 7–9, 11–13, 15 matched on their first iteration-3 run).
- Pressure suite: 5 expectations, 4 with-skill samples total (1 + 2 + 1), all 4 met all 5.
- Triggering suite: 9 expectations across 6 cases, all met on the core axis in every iteration re-run, including this one.

## What this does and does not prove

**What it's suggestive of, across all three iterations:** in 15 regression scenarios (covering all 8 required categories from the original design brief plus the four meaningful-behavior-vs-technical-layer categories added in iteration 3), 1 pressure scenario sampled 4 times, and 6 triggering scenarios, the with-skill runs consistently (a) produce the skill's full report structure with explicit vertical/horizontal/convergence labeling that an unguided baseline never produces, (b) explicitly apply the skill's own named criteria (the vertical grouping test, the three-part enabler test plus the absorbable-enabler question, the risk-boundary properties, the shared-file signal-not-verdict distinction) rather than reaching a similar shape by unstated instinct, (c) name numeric-order mismatches, dependency cycles, and information gaps explicitly rather than silently working around them, (d) hold the stated capability boundary even when a defensible-sounding fix is available (case 10: naming a likely spec defect without redesigning it), (e) hold firm under repeated, direct pressure to manufacture parallelism (4/4 case-101 samples), and (f) — new in iteration 3 — group around independently meaningful, verifiable behavior rather than technical-layer or file-based batching, including on plans with no user-facing surface at all (case 14) and plans where a technically-architectural-looking piece has only one real consumer (case 15).

**The pattern that held across all three iterations, stated plainly:** a capable baseline (same model, no skill, no instruction) reaches *substantively similar or identical* slice boundaries to the with-skill run on most straightforward-to-moderate cases — 6 of 8 in iteration 1, cases 8/9/11 in iteration 2, and case 13 in iteration 3. This is consistent with this skill's own stated evaluation standard (baseline may already find sensible boundaries; the skill should improve consistency and make rationale explicit, not necessarily beat baseline on every case) and should not be read as a weaker finding than it is. Iteration 3 sharpens *where* the skill's distinct value shows up: not on cases where the correct grouping is visually obvious, but specifically where a plan's own text offers a plausible-looking, layer-shaped, or architecture-sounding alternative to the behavior-complete grouping — case 12 (a fixture sentence that reads like pre-approval for a non-persisting checkpoint), case 14 (task-ID fragmentation on purely internal work), and case 15 (an interface split that looks architectural but has one consumer) all produced a baseline miss that the with-skill run avoided.

**What it does not prove:** each case has still been run once per condition except case 101 (4 with-skill samples) and case 14 (3 with-skill samples, 2 of them pre-fix) — this is not a statistically powered benchmark, and a single additional sample of most other cases could look different. Cases 1–5, 7–9, 11, 12, 13, and 15 were verified against the SKILL.md state after iteration 3's first round of edits (or, for 2/11/13, also spot-checked after the verifiability-folding fix); they were not individually rerun a third time against the final "predicted-to-fail" clarification, on the judgment that this clarification only changes behavior for a plan combining (a) a grouping whose verification is specified but suspected to fail and (b) pressure to refuse producing a plan over it — a combination none of those cases present. This is a reasoned inference, not a directly observed result, and is named here rather than silently assumed. No case mixes more than the "mixed realistic" case's five dynamics with a *second* independent complication. No case tests a plan larger than ~10 tasks. The case-204 triggering nuance (see iteration 2) suggests the "positive/negative" triggering frame could be sharpened in a future iteration. No comparison against `slice-plan` or `next-best-slice` operating on the same fixtures was attempted. The mid-iteration case-006/010/014 correction loop is itself evidence that hand-authored expectations *and* first-draft principle wording for ambiguous, judgment-call-shaped fixtures both need active maintenance — a further such case is plausible in a future iteration and should be treated as eval-spec or wording-refinement work, not automatically as a skill defect in the abstract sense.

## Real-world fixture iteration (2026-09-26)

Everything above this section is the author-designed synthetic suite (cases 1–15, 101, 201–206). This section adds three fixtures built from completed public Apache open-source engineering work instead of author-designed plans, on the theory that a synthetic plan — however carefully designed — can be too clean to pressure-test the specific judgment calls this skill exists to make. **SKILL.md was not modified during this work and none of the findings below argue for changing it now** — see "Does this change the SKILL.md verdict?" at the end.

### Method, briefly

Each case (`evals/task-composition/cases/case-30{1,2,3}/`) reconstructs a point-in-time snapshot of a real, already partially-decomposed Jira initiative, cut off before the outcome was known. A first research pass built the agent-visible fixture, a hindsight-safe `provenance/case-30x/` record (sources, actual PRs, historical outcome, cutoff rationale), and a draft REQUIRED/DEFENSIBLE/DIAGNOSTIC grading key (`grading/case-30x.expected.md`). A second, independent reviewer agent then audited each fixture against live Apache Jira/GitHub data specifically for hindsight leakage and unsupported grading claims, with authority to fix defects directly. All three cases had genuine defects found and fixed at that stage (see each case's `provenance/case-30x/cutoff-rationale.md`): case-301's fixture was rebuilt entirely after its first draft (centered on IGNITE-28717/28819) turned out too thin (5 tasks) to test the intended dynamics; case-302 had three post-cutoff Jira edits (two ticket titles, one added sentence) that had leaked into the agent-visible text; case-303 had two tickets whose full descriptions were added days-to-months after the cutoff and needed trimming back to what was actually filed, plus one wrongly-included item in a shared-area cluster and one wrong date. A third pass, after the first live test run, found and fixed a different class of defect the second pass had missed: sentences in `source-notes.md`/`dependencies.md` for cases 301 and 303 that referenced the fixture's own construction process (a "methodological note for whoever maintains this fixture next," a reference to "the provenance PR search," the phrase "than a typical synthetic fixture") — fourth-wall breaks that would tell a tested agent it was in a constructed exercise. One baseline run (case-303) had already been graded against the pre-fix text; it was discarded and both conditions were rerun fresh once the fix landed, per this project's own stated protocol for a fixture defect found mid-run.

One fresh baseline (no skill) and one fresh with-skill sample were then run per case, using the same isolated-subagent harness as the rest of this suite, with explicit instructions not to use web tools and not to rely on memorized/trained knowledge of the real project's actual history (a limitation discussed below, not a guarantee). Full transcripts are under `runs/2026-09-26-real-world-iteration-1/`; the manifest is `real-world-tests/real_world_evals.json`.

### Case 301 — Apache Ignite, IEP-119 Phase 1 ("move common classes to ignite-commons")

**Source and cutoff:** IGNITE-24781 and its 12 Sub-tasks (found via the tracker's actual `parent` field, not the `IEP-119` label, which misses several of them), cutoff 2025-03-30. 13 tasks total.

**What the record establishes:** two real, bidirectional Jira "blocks" links (IGNITE-24846 and IGNITE-24848 both block IGNITE-24850); a real inferable enabler (IGNITE-24782, module creation, unlocking at least 7 other "move X" tasks, with no formal link to any of them); a task that sounds foundational but is actually gated, not gating (IGNITE-24850); two same-class pairs with no stated link (IGNITE-24941/-24850 both touch `IgniteUtils`; IGNITE-24946/-24846 both touch `F`); and one pair (IGNITE-24957/-24851) whose own ticket text points in both directions at once and never resolves.

**Baseline:** Correctly handled the two stated "blocks" links, the two same-class pairs (flagged as inferred, not stated), and — notably — treated IGNITE-24782 as a real slice ("Establish ignite-commons module... don't treat this as create-from-scratch — verify/close out"), reading `repository-state.md`'s note about an existing module skeleton as a scoping detail rather than a reason to drop the slice. On the tangled pair, baseline acknowledged both directions explicitly, then went further than either grading requirement asked for: it invented a three-part F1/F2/F3 sub-decomposition of the two tickets not present in the source material, flagging this as "an inference on my part... worth confirming with the filer" rather than presenting it as settled.

**With-skill:** Correctly handled the two stated links and the two same-class pairs (same treatment as baseline). On the tangled pair, it explicitly declined to invent a resolution — "This plan does not pick a direction; it flags this as unresolved and recommends a human/architect decision" — with no invented sub-decomposition. On IGNITE-24782, it read the same repository-state note (skeleton already exists) and concluded the practical prerequisite was "already satisfied," dropping it from the slice list entirely rather than giving it its own (lighter-scoped) slice.

**Substantive difference, and where the skill did *worse*:** IGNITE-24782's own ticket text calls for creating the module "with several super simple classes in it" — content the skeleton (`pom.xml` + empty `src/main`) does not yet contain, per `repository-state.md`'s own wording ("does not yet contain any of the classes this task set is about moving"). Baseline's reading (verify what exists, still give it a slice, scope it appropriately) tracks the fixture's own language more carefully than the with-skill run's (treat the prerequisite as satisfied, drop it). This is a genuine miss traceable to a specific with-skill inference, not to a SKILL.md instruction telling it to do this — nothing in SKILL.md says "treat an existing scaffold as equivalent to a resolved ticket." It's evidence that the skill's structure doesn't automatically protect against a plain misreading of a repository-state fact.

**Substantive difference in the skill's favor:** the invented F1/F2/F3 split is a real instance of "silently redesigning already-decomposed work" (flagged, not silent, but still an instance of re-decomposing tickets the input didn't decompose) — directly the failure mode SKILL.md's "Input boundary: the work is already decomposed" section exists to prevent ("Don't invent tasks the source material doesn't contain, even to fill a gap you can see. Name the gap as a topology problem instead"). The with-skill run named the same gap as a topology problem instead of inventing content to fill it. This is directly attributable to that specific instruction.

**Net for this case:** a wash on the letter of the grading key (6/7 REQUIRED items for both), with the misses landing on different items — a genuinely mixed result, not a clean skill win.

### Case 302 — Apache Cassandra, CEP-7 / SAI (CASSANDRA-16052)

**Source and cutoff:** 13 open tickets under the SAI component as of 2023-05-15, mid-Phase-3.

**What the record establishes:** CASSANDRA-18112 is blocked by an unresolved community mailing-list DISCUSS thread — external to the task set, not an ordinary engineering dependency; CASSANDRA-18345 reaches into shared, non-SAI-owned SSTable streaming machinery, corroborated by an already-observed rebase precedent; CASSANDRA-18490 cannot deliver its streaming-checksum leg until CASSANDRA-18345 lands (a real convergence, later confirmed by actual reviewer comments that deferred checksum work from 18345 into 18490, though that confirmation is DIAGNOSTIC, not the basis for the requirement); CASSANDRA-18067 is the one stated priority signal, with no ranking stated among the other twelve tickets; CASSANDRA-18166 has no named downstream consumer despite sounding architectural ("IndexContext code model").

**Baseline and with-skill:** Both runs met all 6 REQUIRED items. Both correctly separated CASSANDRA-18112's external blocker from an ordinary internal dependency, named CASSANDRA-18345's shared-machinery risk explicitly, established the 18345→18490 dependency, avoided serializing the eight smaller cleanup tickets behind CASSANDRA-18067, declined to promote CASSANDRA-18166 to enabler status, and respected the single stated priority signal without inventing a ranking among the rest.

**Substantive difference:** none on topology. The with-skill run used the skill's exact report format (`Kind:`, `Delivers:`, `Why grouped:`, named parallel-safety and risk fields per slice); baseline used a free-form structure of comparable thoroughness reaching the same conclusions independently. Consistent with this suite's established iteration-1–3 finding: a capable baseline already handles a well-defined mix of internal/external dependencies and convergence correctly. This case's real-world grounding adds evidence that this finding holds on a genuinely messy, real backlog — not just on synthetic fixtures — but it doesn't show new skill-specific value here.

### Case 303 — Apache Hudi, metadata-table initiative (HUDI-1292 / RFC-15 lineage)

**Source and cutoff:** 19 tickets filed 2021-08-05 to 2021-09-21 (a dense 48-day window inside a much larger, multi-year initiative), cutoff 2021-09-21. The largest and messiest fixture in this suite, by design.

**What the record establishes:** two genuinely unresolved pairs the tickets themselves never settle (HUDI-2432/-2477, both touching restore-finalization; HUDI-2458/-2459, both addressing the same compaction-fencing constraint from different angles); a shared "Blocker" priority label on 11 of 19 tickets that carries no discriminating ranking; a correctness-bug cluster (HUDI-2422, -2432, -2477, -2468, -2476) with a textually-recoverable, not formally declared, shared mechanism (deliberately excluding HUDI-2478, which sounds similar but describes an unrelated crash-recovery path); HUDI-2474 with exactly one named consumer, not enough for standalone-enabler status; HUDI-2303 and HUDI-2472 functionally tied to HUDI-2276's rollout despite no formal "blocks" link; and a numeric-order trap (HUDI-2303, higher ID, must be fixed before HUDI-2276, lower ID and filed earlier, can ship).

**Baseline (rerun, corrected fixture):** Met 11 of 11 REQUIRED items, including a correct, explicit read of the numeric-order trap, the shared-area cluster (correctly excluding HUDI-2478), and the two unresolved pairs' ambiguity. On HUDI-2459/HUDI-2460, it grouped both (plus HUDI-2458) into one slice ("async table services for the metadata table"), but did so as a stated, hedged choice rather than a silent fabrication: it separately restates each ticket's own scope, names the 2458/2459 relationship as "explicitly unresolved," and flags the 2460 inclusion as its own inference — "grouping it here is my inference from thematic similarity only... fine to peel 2460 off to a separate owner if the team disagrees." An adversarial review of the grading key (below) found that REQUIRED #8 originally scored this a violation on the theory that two distinct Jira tickets must yield two distinct delivery slices — a topology mandate the source material doesn't actually support, and one inconsistent with REQUIRED #10's own, more careful treatment of a comparably-shaped situation. The item was corrected to require only that a run not conflate the two tickets into one fix or invent a shared design neither states, while naming whichever grouping choice it makes. Under the corrected wording, the baseline's hedged merge satisfies the requirement.

**With-skill:** Met all 11 REQUIRED items, including keeping HUDI-2459 (S10) and HUDI-2460 (S11) as two separate slices, explicitly reasoning "kept separate rather than merged on feature-name similarity alone" despite noting the thematic overlap. This also satisfies the corrected REQUIRED #8: the choice not to merge is itself named and justified, not silently assumed.

**Substantive difference:** none on REQUIRED-item correctness — both runs reach 11/11 under the corrected key. What remains is a difference in delivery-plan granularity and formatting rigor, not dependency/topology correctness: the baseline consistently resolves each named ambiguity by merging the ambiguous set into one administrative slice with a hedge attached (2432+2477 into one slice; 2459+2460+2458 into one slice; 2476 absorbed directly into 2285's slice), producing a flatter ~13-unit plan, whereas the with-skill run keeps ambiguous tickets as separate, individually-fielded slices with explicit non-concurrency flags attached, producing a more granular 16-slice plan with a uniform per-slice field set applied even to thin/unscoped tickets. Both choices are permitted by the corrected key, and both plans reach the same convergence point (2276 gated on 2303 and the bulk of 2472) and the same set of open questions.

**Net for this case:** a wash on the letter of the grading key (11/11 for both) once a grading-key defect in REQUIRED #8 is corrected — not a skill win. This iteration's original write-up called this "a clean, if narrow, skill win" based on the since-corrected REQUIRED #8; that conclusion did not survive an adversarial review of the grading key (see "Fixture/key corrections" below) and is withdrawn. The two runs differ in style and granularity, not in whether either one got the topology wrong.

### Answers to the ten evaluation questions

1. **Do the real-world fixtures support the existing finding that baseline handles obvious composition well?** Yes, more strongly than the synthetic suite alone did. On case-302 baseline matched with-skill exactly (6/6), and on case-303 — a real, 19-task, genuinely messy backlog — baseline reached 11/11 REQUIRED items unassisted under the corrected grading key, including correctly reasoning through two deliberately unresolved ambiguous pairs and a numeric-order trap. Real messiness did not defeat this capable baseline the way a design brief might predict.

2. **Does task-composition change slice boundaries on any real plan, rather than merely making rationale more explicit?** Yes, on one of three cases, in both directions. On case-301 the skill changed the boundary in a way that was *worse* (dropped IGNITE-24782's slice) and *better* (declined to invent the F1/F2/F3 split) than baseline, in the same run. On case-303, both runs reach the same topology-correctness result (11/11) but choose different granularity — the skill splits HUDI-2459/-2460 into two slices where baseline merges them with a hedge — which the corrected grading key treats as a style difference, not a boundary correctness difference (see the case-303 write-up above for why the original "boundary change" framing here didn't survive review). On case-302 it did not change the boundary at all — only the explicitness of the rationale differed.

3. **If so, which invariant produced the difference?** One, traceable to specific SKILL.md text: the case-301 improvement traces to "Input boundary: the work is already decomposed" ("Don't invent tasks the source material doesn't contain... Name the gap as a topology problem instead"). The case-301 regression (dropping IGNITE-24782) is not traceable to any specific instruction — it reads as a plain misreading of a repository-state fact, not a consequence of following the skill's guidance. Case-303's HUDI-2459/-2460 granularity difference is not evidence of an invariant producing a *correctness* difference — both groupings are permitted by the (corrected) grading key, so this is a stylistic tendency, not a traceable behavioral improvement.

4. **Does the skill over-serialize messy real work?** No instance of this was found. On case-302 and case-303, the with-skill runs matched or exceeded baseline's willingness to run tasks concurrently, including cases with real (case-302's SAI cleanup tickets vs. CASSANDRA-18067) and provisional (case-303's Wave 1, roughly 8 mutually independent branches in both runs) parallelism.

5. **Does it create pseudo-enablers?** No instance of this was found across all three cases. Both conditions on case-302 correctly declined to promote CASSANDRA-18166; both conditions on case-303 correctly declined to promote HUDI-2474. If anything, case-301 shows the *opposite* risk in the with-skill run: under-crediting a real enabler (IGNITE-24782) rather than over-crediting a false one.

6. **Does it miss useful parallelism?** No instance of missed real parallelism was found in the with-skill runs. Case-301's with-skill run found the same 8-way Wave 1 parallelism as baseline; case-302's found the same near-full parallelism as baseline; case-303's with-skill run found parallelism at least as extensive as baseline's, expressed as more, smaller independently assignable slices (including HUDI-2459/-2460 as two branches rather than baseline's one merged branch) — a granularity difference, not a parallelism-count difference, under the corrected key.

7. **Does it stay inside its scope instead of redesigning the plan?** Yes, cleanly, and this is where the strongest and most consistent real-world evidence for the skill landed. Across all three cases, the with-skill runs never invented task content, never proposed a design fix for a suspected defect, and explicitly named several genuine gaps (case-301's SB/IgniteFuture scope gap, case-303's HUDI-2458/-2475/-2436 as "not currently sliceable") as topology questions rather than resolving them. Baseline crossed this line once, concretely: case-301's invented F1/F2/F3 sub-decomposition of the tangled pair.

8. **Are any differences merely report-format differences?** Yes, on case-302 entirely (identical topology, different structure), on case-303 entirely once REQUIRED #8 was corrected (both runs reach the same topology-correctness result; the remaining HUDI-2459/-2460 difference is granularity/formatting, not a topology error on either side), and largely on case-301's non-differentiating slices. Case-301's IGNITE-24782 and F1/F2/F3 items remain the one substantive (non-format) difference found in this iteration — they change which tasks land in which slice, and one of the two changes is scored as a regression, not an improvement.

9. **Did historical execution reveal constraints our reconstructed fixture failed to capture?** One clear instance: case-301's `dependencies.md` correctly flags the IGNITE-24957/IGNITE-24851 tangle as unresolved at the cutoff, and provenance shows it really was resolved by the real IEP-119 team bundling three tickets (IGNITE-24847, -24851, -24852) into one PR — information the fixture correctly withholds as DIAGNOSTIC-only, not something either run could or should have predicted. No case surfaced a constraint the fixture *should* have captured but didn't; the closest to that is the fourth-wall leaks described above, which were fixture-authoring defects rather than missing domain constraints, and were fixed before or immediately after they affected a graded run.

10. **After these cases, is there evidence for changing SKILL.md, or should it remain frozen?** SKILL.md remains frozen. No concrete, traceable behavioral defect in the skill's current instructions was found. The one place the with-skill run did worse than baseline (case-301's IGNITE-24782) does not trace to a SKILL.md instruction telling it to do the wrong thing — it traces to an inference the run made despite the skill's text, not because of it — so per this project's own instructions this is exactly the kind of disagreement to *investigate rather than automatically act on*, and it was investigated: it's evidence for one more targeted regression case in a future iteration (a repository-state fact that describes a scaffold as existing but incomplete, paired with a ticket whose own remaining scope isn't satisfied by that scaffold), not evidence that any current SKILL.md wording is wrong.

### Fixture/key corrections made during this iteration, and when

- **Pre-run (research + independent-reviewer passes):** case-301 rebuilt entirely (see above); case-302's three post-cutoff Jira-edit leaks fixed; case-303's two trimmed-description tickets, one wrong shared-area inclusion (HUDI-2478), and one wrong date fixed. All before any graded run.
- **Mid-run (this session, after the first case-303 baseline run):** the four fourth-wall/meta-language leaks described above, found by grepping the agent-visible files for terms like "fixture," "provenance," "exercise," and "methodological note" after the first case-303 baseline run cited one of them in its own reasoning. Fixed immediately; the affected run (case-303 baseline, pre-fix) was discarded and both case-303 conditions rerun fresh. Cases 301 and 302 had not yet been run when this was found, so no other run needed discarding.
- **Post-run, pre-merge (adversarial review of the grading key itself, before PR #65 merged):** REQUIRED #8 in `grading/case-303.expected.md` originally required HUDI-2459 and HUDI-2460 to remain in two separate delivery slices. An adversarial review found this mandated a slice topology the source material doesn't establish — two distinct Jira tickets is a task-identity fact, not by itself a slice-identity fact, which is the exact distinction this skill exists to get right. The item was inconsistent with REQUIRED #10's own, more careful handling of a comparably-shaped (and better-evidenced) situation, and had no historical-PR corroboration either way (`provenance/case-303/actual-prs.md` shows neither ticket was ever implemented, separately or jointly). The item was corrected to require only that a run not conflate the two tickets into one fix or invent an unstated shared design, while naming whichever grouping choice it makes. Both frozen runs (not rerun; only the hidden key changed) were then regraded by a fresh reviewer agent against the corrected wording: both satisfy it. This changed case-303's reported comparison from "baseline 10/11, skill 11/11, clean skill win" to "both 11/11, no REQUIRED-item difference" — see the case-303 write-up and evaluation-question answers above, which were updated accordingly. This is a grading-key defect fix, not a response to either run's score.
- **Not otherwise changed:** no other REQUIRED item was widened, narrowed, or removed in response to either run's actual output — every other grading-key adjustment happened before or immediately after a discovered fixture defect, never because a run's answer was merely persuasive.

### Limitations specific to this iteration

- **Training-data contamination risk is real and not fully mitigated.** Unlike the synthetic cases, these fixtures describe identifiable, public projects. Tested agents were instructed not to use web tools and not to rely on memorized project history, but nothing in the harness can verify compliance or strip prior training exposure to these specific tickets/PRs. Case-301's underlying events (2025–2026) sit closer to or past the model's stated training cutoff (January 2026) than cases 302 (2023) and 303 (2021), which is a partial, not complete, mitigation — case-302 and case-303 concern well-known Apache projects whose history could plausibly appear in training data regardless of date. No direct evidence of contamination was observed in any transcript (no run referenced information absent from its case files), but this is an inherent limitation of real-world fixtures that the synthetic suite does not share, not something this iteration can rule out.
- **Single sample per case per condition.** As with much of the synthetic suite, this is not a statistically powered comparison — a second sample of case-301 in particular (the case with a mixed, non-unanimous result) could look different.
- **Case-301 ended up smaller than the original design brief's "medium, 8-15 task" target for only part of its life** (the rebuilt version lands at 13, in range) but took two research passes to get there; the first, thinner draft (5 tasks, centered on IGNITE-28717/28819) is preserved only in provenance for transparency about that process, not as a second graded fixture.
- **Case-302's DEFENSIBLE-EITHER-WAY items** (the CASSANDRA-18067/18345/18490 slice shape; the two shared-dependency pairs with lucene-core and RAMIndexOutput) were not separately scored pass/fail in this write-up beyond confirming both runs named them rather than ignoring them — consistent with the grading key's own design, but it means this write-up's REQUIRED-only tallies slightly understate how much reasoning both runs actually did on this case.
- **No comparison against `slice-plan` or `next-best-slice`** was attempted on these fixtures, consistent with the existing synthetic-suite limitation.

## Real-world fixture iteration 2 (2026-09-26) — case 304

A fourth real-world fixture, built independently of the session that produced 301–303, from a different kind of source: not a multi-year Jira epic, but a five-to-nine-week GitHub issue/PR burst (Kubernetes KEP-753 "Sidecar Containers," the post-alpha resource-manager fallout). **SKILL.md was not modified for this case either, and this section's findings do not argue for changing it** — see the final entry below.

### Source, cutoff, and fixture size

`evals/task-composition/cases/case-304/` reconstructs the state of this initiative's open work as of **2023-08-30, end of day (UTC)** — chosen specifically to land right after a same-day kubelet regression (REGR-120247) was reported and escalated but before any fix for it, or the test-infra CI job (`test-infra`#30281), had merged (both land within the following week). **9 agent-visible tasks** survive an explicit pre-drafting adversarial pass (recorded in `provenance/case-304/cutoff-rationale.md`) that rejected two ways of padding the count closer to a "10–18" target as manufacturing evidence rather than reflecting it: treating already-resolved, thematically-adjacent bugs (kubectl describe-nodes display fix, a LimitRanger gap) as open work, and splitting one still-unresolved, same-day investigation's two draft PRs into separate tasks. This is treated as an honest property of a shorter, less prolific real window, not a defect.

Full provenance is under `evals/task-composition/provenance/case-304/`. Before any tested-agent run, a fresh, independent reviewer agent (no access to this session's reasoning) audited the fixture and grading key against live GitHub REST/GraphQL data and found and fixed four genuine factual defects — none of them instances of the nine adversarial failure modes it was specifically asked to hunt for (task/PR-identity-as-slice-identity, thematic-similarity-as-dependency, technical-similarity-as-mandatory-grouping, historical-execution-as-normative, unsupported parallel-safety claims, forced topology, hidden post-cutoff information, or SKILL.md-derived grading criteria):

1. TOPO-119407's self-assignment/discussion timeline was wrong (claimed same-day self-assign with zero further comments; the record actually shows a next-day self-assignment with a stated e2e-tests-first plan, plus a maintainer's same-day triage acceptance).
2. REGR-120247 was missing its two same-day priority labels (`important-soon`, then `critical-urgent`) — the draft had claimed no item in this fixture carried any priority label at all.
3. PR #120269 was wrongly called "unreviewed" — it received substantive same-day review with a live, unresolved disagreement between two reviewers over approach; only its sibling draft, #120267, was actually unreviewed.
4. E2E-119014's checklist-order description was inverted (claimed the base-PR-merge checklist item was first; the issue's pre-cutoff edit history shows it's actually second, after E2E-119019).

All four were corrected in the fixture, dependencies, grading key, and provenance files before freezing (commit `92a7ac0`). No REQUIRED item was added, widened, or narrowed in response to either tested run's later output.

### What the record actually establishes

- **A genuine, comment-thread-traceable shared root cause across three (arguably four) tickets that does not by itself determine a slice count.** CPU-119447, MEM-119442, and DEV-119442 all trace to one 2023-07-20 exchange identifying the same container-coalescing pattern across three separate kubelet packages with no shared file; TOPO-119407 names the same underlying pattern but is tracked in a separate issue with markedly less commitment.
- **An asymmetric-readiness trap inside one umbrella issue's title.** The issue names "CPU, memory, device, topology" managers side by side, but as of cutoff only CPU has an actively-reviewed PR; memory and device have zero PR/assignee activity; topology (a *different* issue) has even less — a bare TODO, a next-day self-assignment, and a same-day triage acceptance with no code-location analysis.
- **A real, stated, multi-input convergence.** The e2e-coverage umbrella issue's own checklist requires both E2E-119019 and E2E-30281 to land before E2E-119014 can be written.
- **A same-day, same-author, still-unresolved investigation (REGR-120247)** that must not be split into "the bug" and "the fixes" — two draft PRs exist, one under live reviewer disagreement, neither settled.
- **A cross-binary independent item (HPA-119991)** sharing vocabulary and timing with the manager cluster but zero code or file relationship to it.

### Results: baseline 11/11, with-skill 11/11 — a clean tie

Both runs used the exact same frozen five files (`context.md`, `tasks.md`, `dependencies.md`, `source-notes.md`, `repository-state.md`), one fresh subagent per condition, neither with access to provenance, the grading key, the other condition's output, or this prompt. Raw outputs: `runs/2026-09-26-real-world-iteration-2/case-304-{baseline,skill}.md`.

**Both runs met all 11 REQUIRED items.** Both: excluded the three already-landed items entirely rather than slicing them; described MEM-119442/DEV-119442/TOPO-119407 as named-but-unscoped without inventing a design; named the CPU/MEM/DEV shared root cause explicitly while declining to invent a merge-order dependency among them; distinguished TOPO-119407 as materially thinner than MEM-119442/DEV-119442; showed E2E-119014 gated on both E2E-119019 and E2E-30281; didn't claim either open e2e PR was nearly finished; kept HPA-119991 fully independent of the manager cluster; kept REGR-120247 as one unresolved item without presenting either draft PR (or either reviewer's preferred approach) as settled; didn't fabricate a link between REGR-120247 and the manager cluster; and correctly scoped the one real priority signal (REGR-120247's own labels) to that item alone, without inventing a ranking for anything else or silently claiming nothing here has any priority signal.

**On every DEFENSIBLE-EITHER-WAY point, both runs independently chose the identical option** and stated it explicitly: both split the manager cluster into four separate slices rather than one grouped slice; both kept TOPO-119407 standalone rather than folded into the cluster; both split the e2e prerequisites into two slices rather than one; both kept REGR-120247 as a single slice with explicit "possibly more than one fix" language. The resulting dependency graphs are structurally identical: 8 independent branches, 1 slice (the gated e2e-coverage item) blocked on two of them, zero cycles, zero manufactured enablers.

**The only differences found were presentational, not substantive.** The with-skill run used the skill's exact report format throughout (`Kind:`, `Delivers:`, `Why grouped:`, named parallel-safety and risk fields per slice, plus the closed Recommended-execution-grouping/Available-parallelism/Bottlenecks/Topology-issues/Out-of-scope sections) and explicitly tied several judgments to the skill's own vocabulary (e.g., correctly declining to label CPU-119447's fix a "horizontal enabler" for memory/device despite it being a same-pattern signal, since it doesn't unlock two or more separately-verifiable downstream slices — the skill's own absorbable-enabler test). The baseline used an equally thorough but free-form structure (a "ground rules I applied before slicing" preamble doing the same job as the skill's named criteria). The with-skill run also surfaced one piece of context neither run was required to use — `source-notes.md`'s note that the KEP's original design text named CPU/Memory/Topology Manager as a foreseen risk but not Device Manager — as color on DEV-119442's risk framing; the baseline didn't mention this. It affected no REQUIRED item and no slice boundary.

### Answers to this case's own ten evaluation questions

1. **Does either condition recognize genuine parallelism without exaggerating it?** Yes, both — 8 of 9 slices independent, matching `repository-state.md`'s explicit package/binary separation; neither invented additional parallelism nor missed any. (Model observation, directly checked against both transcripts.)
2. **Does either condition incorrectly collapse all manager work into one "resource manager" slice?** No — both split CPU/MEM/DEV/TOPO into four separate slices, one of the DEFENSIBLE-permitted topologies. (Model observation.)
3. **Does either mechanically create one slice per manager?** Both did land on one slice per manager, but the reasoning given for each split cited a specific fact (separate kubelet packages, no shared file, unresolved fix-transferability) rather than merely "there are four tickets." This is a reasoned choice inside the DEFENSIBLE range, not the "one slice per task ID" anti-pattern SKILL.md warns against — a distinction worth naming precisely because the *outcome* (one slice per ticket) looks identical to the failure mode; only the *stated reasoning* distinguishes them here. (Model observation plus a judgment call about how to read that distinction.)
4. **Does either distinguish shared verification/convergence from implementation coupling?** Yes, cleanly, in both — both treated E2E-119014's stated two-input convergence as categorically different from the CPU/MEM/DEV shared-root-cause signal, never conflating "shares a discovered pattern" with "needs a merge-order dependency" or "must converge." This is the specific distinction case-304 was built to test, and both conditions held it. (Model observation.)
5. **Does either miss a known cross-component or post-alpha dependency?** No — both found the one real stated dependency (E2E-119014) and correctly treated REGR-120247, a genuine post-alpha discovery, as unconnected to the manager cluster. (Model observation.)
6. **Does the skill over-serialize the work?** No instance found — the with-skill run's parallelism wave structure is identical to baseline's. (Model observation.)
7. **Does the skill manufacture an enabler?** No — the with-skill run explicitly declined to label CPU-119447 (or anything else) a horizontal enabler, correctly applying its own multi-consumer test. (Model observation.)
8. **Does the skill materially change slice boundaries, or only rationale/reporting?** Only rationale/reporting and format, on this case. Slice count, groupings, dependency graph, and every DEFENSIBLE choice are identical between conditions. (Model observation.)
9. **Are multiple topologies still defensible after considering the full historical record?** Yes — the grading key's DEFENSIBLE section identifies at least four independent binary choices with real historical ambiguity behind them (see `historical-outcome.md`'s DIAGNOSTIC section: three of the four manager fixes actually landed within a day of each other two months later, while the fourth stalled 18 months — evidence the record's ambiguity was real, not manufactured for the fixture). Neither run explored the grouped alternative for the manager cluster; both independently landed on the same, more granular point in that defensible space. (Eval-design judgment plus a historical fact, kept separate: the *existence* of a defensible alternative is a fact about the record; that *neither run tried it* is an observation about these two particular samples, not evidence the alternative is wrong.)
10. **Does any grading item accidentally encode the current skill's preferred heuristic instead of historical evidence?** No instance found by the independent pre-freeze audit, which checked this specifically (its category 9) and confirmed every REQUIRED item traces to a fixture-file location it independently verified against live GitHub data. (Reported finding from the independent audit, not this write-up's own re-derivation — noted as such.)

### Conclusion about the skill on this case

**A clean tie, not a skill win or a baseline win.** Per this project's own instruction for this comparison: preserved as a tie rather than framed as a win either direction. This is consistent with this suite's recurring finding across cases 302 and (once its grading-key defect was corrected) 303: a capable baseline reaches the same topology as the with-skill run on real, messy, ambiguous backlogs; the skill's distinct, repeatable contribution is explicit, criteria-traceable structure, not different or better answers. Case-304 adds evidence that this holds even on a fixture specifically engineered to isolate "shared root cause vs. mandatory slice boundary" as sharply as this suite has attempted — neither condition needed the skill's explicit vocabulary to get the substance right, though the with-skill run's rationale is more legible and more directly auditable against named criteria.

### Limitations specific to this case

- **Single sample per condition**, same limitation as cases 301–303's individual results — a second sample could differ, particularly on the DEFENSIBLE choices where both runs happened to agree.
- **Training-data contamination risk applies here too, and arguably more than case-301.** These are 2023 Kubernetes issues/PRs on one of the most heavily-represented open-source projects in any large training corpus; both tested agents were instructed not to use web tools and not to rely on memorized project history, but nothing in the harness can verify compliance or strip prior exposure. No transcript referenced information absent from its five case files, but this cannot be ruled out.
- **The fixture's task count (9) sits below the ~10–18 aim** stated for this case; treated throughout as an honest property of the source material rather than backfilled, but it does mean this fixture pressures fewer simultaneous dynamics per run than cases 301/303.
- **No comparison against `slice-plan` or `next-best-slice`**, consistent with the existing limitation noted for cases 301–303.

## Pressure variant of case 304 (2026-09-26) — utilization-pressure framing on the unchanged fixture

Case 304's neutral run (above) held its own agent-visible fixture fixed and
only asked for delivery slices. This section adds a pressure variant that
holds the *same, byte-for-byte unchanged* fixture fixed and varies only the
prompt: a realistic engineering-lead request to move quickly, staff four
engineers, and maximize useful parallelism. **SKILL.md was not modified for
this variant either.** The frozen prompt and grading key live at
`evals/task-composition/pressure-tests/pressure_evals.json` (entry
`304-pressure`) and `evals/task-composition/grading/
case-304-pressure.expected.md`; both were independently audited by a fresh
reviewer agent (no exposure to this session's own reasoning) before any
test run, checking specifically for forced answers, SKILL.md-derived
grading criteria, an assumption that any specific parallelism count is
inherently good or bad, an assumption that the neutral 9-slice topology is
canonical, changes beyond the pressure framing, historical/post-cutoff
leakage, and ungrounded grading rules. The audit found no such defects; one
broken cross-reference (to a nonexistent RESULTS.md section) was found and
fixed before freezing (commit `2b0d869`).

**Pressure prompt (frozen, verbatim):** "Treat evals/task-composition/cases/
case-304/*.md (context.md, tasks.md, dependencies.md, source-notes.md,
repository-state.md) as the complete plan and task list for the remaining
work -- there is nothing else to consider. We need to move quickly and I
have four engineers available. Maximize useful parallelism and keep all
four moving if the work supports it. Give me agent-sized assignments and
call out any work that truly cannot proceed concurrently."

**Historical inputs unchanged:** confirmed by `git diff` at freeze time --
zero changes to any file under `evals/task-composition/cases/case-304/` or
`provenance/case-304/`. Only `pressure-tests/pressure_evals.json`,
`pressure-tests/README.md`, and the new `grading/case-304-pressure.expected.md`
were added.

One fresh baseline (no skill) and one fresh with-skill sample were run,
each in an isolated scratch copy containing only the five case-304 files
(plus, for the with-skill run, a copy of `SKILL.md`), with explicit
instructions not to use web tools, not to rely on memorized/trained
knowledge of the real project, and not to explore anything beyond those
files. Neither run saw provenance, the grading key, the other condition's
output, this write-up, or case-304's own neutral (non-pressure) results.
Raw outputs: `runs/2026-09-26-pressure-case-304/case-304-pressure-{baseline,skill}.md`.

### Results: baseline 15/15, with-skill 15/15 -- another clean tie

Both runs met all 11 carried-over REQUIRED items from `case-304.expected.md`
and all 4 pressure-specific REQUIRED items (P1-P4) from
`case-304-pressure.expected.md`:

- **P1 (does not split REGR-120247 across two engineers):** both kept
  REGR-120247's two draft PRs as one slice/task assigned to one engineer.
  Baseline: "It does not split REGR-120247's two draft PRs across two
  engineers... splitting them would multiply the number of proposals in an
  already-contested thread rather than resolve it faster." With-skill (S9):
  "one issue, one root cause... two PRs that are both part of resolving
  it, not two separate deliverables."
- **P2 (does not relax E2E-119014's two-input gate):** both explicitly held
  the gate. With-skill (S8): "Parallel-safe with: None currently --
  genuinely blocked, not just numbered last." Baseline: Engineer 4 "only
  start[s] E2E-119014 once both are in."
- **P3 (does not treat "four engineers" as evidence of four slices):** both
  explicitly named the real independent-branch count as eight and labeled
  the four-way packing a staffing choice, not a topology claim. Baseline:
  "I only paired CPU with MEM and DEV with TOPO to balance... not because
  the work requires it." With-skill: "This mapping is a staffing choice
  layered on top of the dependency findings above -- not itself a
  dependency claim."
- **P4 (does not invent a merge-order among independent items for a
  tidier rotation):** both explicitly disclaimed every sequential pairing
  as non-blocking. Baseline (Engineer 2's CPU-then-MEM queue): "not a hard
  block... a sequencing convenience within one person's queue, not a
  cross-engineer gate." With-skill (Engineer 4's HPA-then-e2e queue): "a
  capacity choice... not a dependency."

### The two conditions independently converged on the identical staffing packing

Both runs proposed the *same* four-way split of the same eight independent
items, unprompted and without seeing each other's output:

| Engineer | Baseline | With-skill |
|---|---|---|
| 1 | REGR-120247 (solo) | REGR-120247 / S9 (solo) |
| 2 | CPU-119447 → MEM-119442 | CPU-119447 / S1 → MEM-119442 / S2 |
| 3 | DEV-119442 + TOPO-119407 | DEV-119442 / S3 → TOPO-119407 / S4 |
| 4 | HPA-119991 + E2E-119019 + E2E-30281 (→ E2E-119014 once both land) | HPA-119991 / S5 → E2E-119019 / S6 → E2E-30281 / S7 (→ E2E-119014 / S8 once both land) |

Both independently reasoned the same way to get there: REGR-120247 solo
because it is the one priority-flagged, contested item needing sustained
single-owner attention; CPU paired with MEM because CPU is the
nearly-finished item and the same engineer is well-positioned to carry its
fix shape into MEM's from-scratch work (explicitly *not* a hard gate in
either run); DEV paired with TOPO as the two least-scoped items; HPA
bundled with the e2e-prerequisite chain because HPA is a light
review-shepherding task with slack to absorb it. This is a striking
convergence for two runs that never saw each other's reasoning, and
matches this suite's recurring finding: a capable baseline reaches
substantively the same conclusion as the with-skill run on this fixture.

### DEFENSIBLE choices: identical to each other and to the neutral run

On every point `case-304.expected.md`'s own DEFENSIBLE section leaves open,
both pressure runs made the same choice, and it is the same choice both
conditions made in the neutral (non-pressure) run: four separate
manager-cluster slices (not one grouped slice), TOPO-119407 kept standalone
(not folded into the cluster), the two e2e prerequisites kept as two
slices (not folded into one), and REGR-120247 kept as one slice with
explicit "possibly more than one fix" language rather than split. No
DEFENSIBLE choice changed under pressure in either condition.

### Comparison against neutral case-304

**Baseline, neutral → pressure:** No change in slice count (9 items either
way), no change in dependency treatment (E2E-119014 still the only gated
item; REGR-120247 still independent and unresolved; HPA still independent),
no manufactured concurrency (the neutral run's own hedge -- "B and C can
run fully in parallel, or be picked up sequentially by the same agent... if
convenient" -- already contained the same staffing-vs-topology distinction
the pressure run makes explicit and systematic across every pairing), no
weakened uncertainty language (TOPO's thinness, REGR's unresolved
disagreement, and the MEM/DEV fix-shape-reuse question are stated with the
same hedges in both runs), no altered DEFENSIBLE choices. The one visible
change is presentational: the neutral run had no reason to talk about
engineers or headcount; the pressure run adds an explicit staffing layer on
top of the same topology, with repeated, explicit disclaimers that the
packing is not a dependency claim.

**With-skill, neutral → pressure:** Same finding. The neutral with-skill
run's S1-S9 topology (slice count, dependencies, parallel-safety, DEFENSIBLE
choices) is unchanged in the pressure run's S1-S9 -- both land on four
separate manager slices, TOPO standalone, two e2e-prerequisite slices, and
one REGR-120247 slice with unresolved-fix language. The pressure run adds a
distinctly separate "Translation into agent-sized assignments" section
after the skill's own native report format, keeping the slice plan itself
and the staffing translation visibly separate rather than letting headcount
pressure bleed into the `Depends on`/`Parallel-safe with` fields of the
slices themselves.

**Which condition is more behaviorally stable under pressure?** Both,
equally, on this case. Neither changed slice count, dependency treatment,
or any DEFENSIBLE choice; neither weakened its hedged uncertainty language;
neither manufactured concurrency the fixture doesn't support. The one
structural difference is that the with-skill run's native report format
gave it a ready-made seam (slice plan, then a separate translation step) to
keep the two concerns apart, while the baseline achieved the same
separation through its own explicit prose disclaimers on each staffing
choice ("things this plan deliberately does not do"). Both are legitimate
ways to hold the same line; this is a difference in mechanism, not in
outcome.

### Answers to the ten evaluation questions

1. **Did pressure change baseline behavior?** No substantive change. It
   added a staffing/assignment layer on top of an unchanged topology, with
   explicit disclaimers that the staffing choices are not topology claims.
2. **Did pressure change skill behavior?** No substantive change, same
   finding -- the skill's native slice plan is unchanged; only a new,
   clearly-separated staffing-translation section was added.
3. **Did either manufacture concurrency?** No. Both explicitly grounded
   the four-way staffing plan in the fixture's real eight independent
   branches rather than inventing additional ones, and both explicitly
   declined to promote any staffing pairing to a topology claim.
4. **Did either sacrifice known topology constraints to satisfy
   utilization pressure?** No. Both preserved E2E-119014's two-input gate,
   REGR-120247's unresolved-fix status, HPA's independence, and the
   CPU/MEM/DEV shared-root-cause-without-merge-order distinction.
5. **Did either mechanically map engineers to tasks?** No. Neither forced
   a naive one-manager-per-engineer or exactly-four-slices mapping; both
   packed items 1/2/2/3 across four engineers based on stated
   reasons (urgency/contestedness, fix-shape-reuse opportunity, thinness
   of scope, review-shepherding slack) rather than an even split for its
   own sake.
6. **Did either honestly leave capacity unused when appropriate?** Not
   applicable in the "unused capacity" direction here -- the fixture
   supports eight independent branches for four engineers, so there was
   always more than enough real work; both runs instead correctly surfaced
   the *reverse* honesty point, that more independent work exists than four
   people can start on at once (explicit in both: "only 4 people for 8
   ready branches" / "topology supports 8 concurrent starting points").
7. **Did the skill materially improve behavioral stability under
   pressure?** No -- both conditions were equally stable on this case; see
   "Which condition is more behaviorally stable" above.
8. **Did the pressure variant reveal anything not visible in neutral
   case-304?** Yes, one thing: it demonstrates that both conditions can
   convert a topology into a headcount-constrained staffing plan (packing
   multiple independent items under one engineer when engineers are
   scarcer than independent branches) while cleanly labeling the packing as
   a staffing choice rather than a topology fact -- a capability the
   neutral prompt (which only asked for delivery slices, not staffing)
   never exercised.
9. **Is any observed difference strong enough to change our understanding
   of the skill?** No. This is a second clean tie in a row for case-304 (the
   neutral run tied 11/11; this pressure variant ties 15/15), reinforcing
   this suite's established, recurring finding across cases 302-304: a
   capable baseline reaches substantively the same topology as the
   with-skill run on real, messy backlogs, including under realistic
   delivery pressure; the skill's distinct, repeatable contribution remains
   explicit, criteria-traceable structure, not different or better
   substantive answers.
10. **Does this result justify any SKILL.md change?** No. Recorded per this
    session's instruction not to modify SKILL.md regardless of outcome; no
    behavioral defect was found that would motivate one.

### Limitations specific to this pressure variant

- **Single sample per condition**, same limitation as every other case in
  this suite -- a second sample could differ, particularly on the specific
  four-way packing, where both runs happened to converge.
- **This fixture's real topology (eight independent branches, only one
  gate) meant the requested "four engineers, maximize parallelism" framing
  was largely satisfiable without any tension against the dependency
  graph** -- unlike case-101's pressure variant, which targets three tasks
  genuinely contending on one shared file. This is a deliberate, cautious
  design choice (see `case-304-pressure.expected.md`'s "Why" section): the
  sharper test here is whether staffing pressure tempts fragmenting
  REGR-120247's still-forming investigation or relaxing E2E-119014's one
  real gate, not whether it manufactures safety for contended work, because
  this fixture has no contended work to manufacture safety for. A future
  pressure variant built around a fixture with genuine real-world file/
  interface contention (case-301's same-class shared-file pairs, or
  case-302's CASSANDRA-18345 shared-machinery risk) would test the
  contended-work axis on real-world material more directly than this one
  does -- not attempted here, consistent with this session's scope.
- **Training-data contamination risk applies here too**, same as case-304's
  neutral run -- both tested agents were instructed not to use web tools or
  rely on memorized project history, but this cannot be verified or ruled
  out.
- **No checksum mechanism exists in this repository's conventions.** This
  variant's freeze point is the git commit (`2b0d869`), consistent with how
  case-304's own neutral fixture was frozen (commit `92a7ac0`); no separate
  hash/manifest file was introduced, since none of the other 300-series
  cases or the pressure suite use one.

## Real-world fixture iteration 3 (2026-09-26) — case 305 (independence-then-convergence)

A fifth real-world fixture, built independently of the sessions that
produced 301-304, deliberately probing a different topology question from
any prior case in this suite: **can a run preserve legitimate
independence between two workstreams while recognizing the point where
they acquire a shared semantic convergence constraint?** Source: Rust's
`async fn` in trait (AFIT) and return-position `impl Trait` in trait
(RPITIT) stabilization history (rust-lang/rust, rust-lang/rfcs). **SKILL.md
was not modified for this case, and nothing below argues for changing it**
— see "Does this justify a SKILL.md change?" under Q14 below.

### Source, cutoff, and fixture size

`evals/task-composition/cases/case-305/` reconstructs the open work as of
**2023-06-13, end of day UTC** — the day RFC 3425 (RPITIT's own, real,
ratified RFC) merged, and one day before the umbrella tracking issue
(`rust-lang/rust#91611`) was itself restructured to formally name both
features and cross-reference the central convergence bug. **9
agent-visible tasks**: two AFIT-only bugs, two RPITIT-only bugs, three
dual-labeled bugs (each one ticket, not a two-feature split), one central
convergence bug (RPITIT-112194), and one item drawn directly from RFC
3425's own ratified "Unresolved questions" text (RFC-3425-QUESTIONS).
Full provenance, including a Phase-1 adversarial audit of each candidate
hypothesis claim in the historical-fact/supported-constraint/not-supported
format, is under `evals/task-composition/provenance/case-305/`.

Before any tested-agent run, a fresh, independent reviewer agent (no
access to this session's reasoning) audited the fixture and grading key
against live GitHub/RFC data and found and fixed four genuine defects —
none of them instances of the ten adversarial failure modes it was
specifically asked to hunt for:

1. A quote on issue #108309 ("...equally as broken with the latter") had
   its trailing question mark silently dropped in three files
   (`tasks.md`, `dependencies.md`, `grading/case-305.expected.md`),
   turning a hedged, slightly uncertain remark into a flat assertion.
2. `repository-state.md` misattributed issue #112194's filing to the
   compiler-team member who authored most implementation PRs; it was
   actually filed by a different person (`tmandry`, one of RFC 3425's two
   co-authors).
3. `sources.md`'s "no candidate missed" claim was inaccurate: a fresh,
   unbounded label search turned up three same-window, same-label
   ICE/glacier reports (#112047, #109464, #108580) the original research
   pass hadn't logged. All three are correctly excludable under the
   fixture's own already-stated "one-off ICE/diagnostic report" criterion
   — the task count (9) was unaffected — but the audit trail claiming
   completeness was wrong until this was added.
4. A cross-reference timestamp for #112194 conflated a `referenced` event
   with the actual `cross-referenced` event (an 11-second-vs-1-minute
   difference); corrected to state both precisely.

All four were corrected before freezing (commit `1739f3b`). No REQUIRED
item was added, widened, or narrowed in response to either tested run's
later output.

### What the record actually establishes

- **Real, textually strong mechanism-level coupling, not just a shared
  name.** `async fn` in a trait desugars to RPITIT's own return-type
  mechanism; the two features' original 2022 implementation shares a
  verified file (`compiler/rustc_ast_lowering/src/lib.rs`); a
  compiler-team member states directly, on the one dual-labeled ticket
  with a stated shared-mechanism claim (AFIT-RPITIT-108309): "async fn in
  trait is just return position impl trait in trait."
- **A real, explicit, RFC-text-level convergence pairing that predates
  its own concrete test case.** RFC 3425 states, as one of its own design
  goals (not a later discovery), that `async fn` should remain usable
  interchangeably with its `impl Trait` desugaring — and its own ratified
  "Unresolved questions" section names, back to back, whether to
  stabilize the two features together and "Resolution of [RPITIT-112194]"
  as two linked but distinct open items.
- **A deliberate, stated, administrative independence decision that
  coexists with that coupling, not one that erases it.** AFIT was
  deliberately split onto its own feature gate in 2022 "since async fn in
  trait doesn't need to follow the same stabilization schedule" — five
  weeks after RPITIT's own initial implementation had AFIT running under
  RPITIT's gate.
- **A convergence question the record poses but does not answer.** Both
  of RFC 3425's linked open questions are listed, verbatim, under its own
  "Unresolved questions" heading — the ratified RFC states the hazard and
  names the linked bug without resolving either.
- **Four single-feature bugs and two of three dual-labeled bugs with no
  stated relationship to the convergence pairing, or to each other,**
  despite sharing labels, subsystem area, or surface-level "lifetime bug"
  wording with items that are genuinely linked.

### Results: both runs pass all 12 REQUIRED items — another tie on correctness, with one genuine, attributable topology difference

Both runs used the exact same frozen five files, one fresh subagent per
condition, neither with access to provenance, the grading key, the other
condition's output, or this session's own reasoning. Raw outputs:
`runs/2026-09-26-real-world-iteration-3/case-305-{baseline,skill}.md`.

**Both runs met all 12 REQUIRED items.** Both: excluded already-landed
work entirely; recognized real AFIT/RPITIT mechanism coupling without
claiming full independence; kept the four single-feature-only items
(AFIT-104689, AFIT-RTN-110963, RPITIT-111105, RPITIT-109468) fully
separate from each other and from everything else, with no invented
merge-order; treated AFIT-RPITIT-108309 as one piece of work grounded in
its stated shared-mechanism quote, without assuming AFIT-RPITIT-108304 or
AFIT-RPITIT-109016 shared that same status merely from shared labels;
showed RFC-3425-QUESTIONS' stabilize-together question as textually
linked to (not independent of, and not automatically resolved by)
RPITIT-112194, without extending that pairing's scope to the other seven
items; treated RFC 3425's own unresolved questions as genuinely
unresolved, not decided; declined to conflate RPITIT-109468 and
RPITIT-112194 despite both being "RPITIT lifetime" bugs; and invented no
priority ranking beyond the one institutional-visibility signal the
record itself supports.

**On most DEFENSIBLE points, both runs made the identical choice.** Both
kept the three dual-labeled tickets as three separate slices rather than
one grouped cluster; both kept all four single-feature-only items fully
separate rather than grouped by feature side; both treated
AFIT-RTN-110963 as in-scope AFIT work with RTN flagged as an external
touchpoint, not adopted into scope.

**One DEFENSIBLE point produced a genuine, traceable topology
difference — the first of its kind in this suite since case-301.**
Baseline composed **9 slices**: it gave RFC-3425-QUESTIONS' two policy
sub-questions (stabilize together? / limit positions to RTN-nameable
ones?) their own dedicated ninth slice, with an explicitly non-code
verification checkpoint ("a recorded decision (RFC amendment or
tracking-issue comment), since this is a policy artifact, not shippable
code"). The with-skill run composed **8 slices**: it folded the "resolve
RPITIT-112194" sub-question into S8 (the slice that fixes RPITIT-112194
itself — the RFC's own text literally names that ticket as the
resolution, so no separate slice does independent work), and explicitly
declined to manufacture a slice for the other two sub-questions at all,
naming them instead as an open gap under "Topology issues": "have no PR,
no assignee, no design proposal, and no stated verification path
anywhere in [the five files]... A component with no independent
verification path either gets folded into the slice that actually
verifies it... or is named as an open gap rather than force-fit into an
invented slice." This is directly traceable to one specific piece of
SKILL.md text (the vertical-grouping test's verifiability question, and
the verifiability-folding rule added in iteration 3) — not a vaguer
"the skill produced a different vibe" observation.

Neither choice violates any REQUIRED item; both are permitted by
`case-305.expected.md`'s DEFENSIBLE section, which anticipated a
one-slice-vs-two-linked-slices split for this exact pairing but not this
third variant (fold the literally-named sub-question, decline a slice for
the un-scoped remainder entirely). This write-up does not treat either
choice as more "correct" — see Q7/Q8 below.

### Answers to this session's own fourteen questions

1. **Did either condition preserve feature-specific independence where
   supported?** Yes, both — all four single-feature-only items stayed
   independent in both runs, with no invented cross-links.
2. **Did either prematurely lump AFIT and RPITIT into one giant slice?**
   No, neither did — both produced 8-9 separate slices, none collapsing
   the backlog.
3. **Did either keep them falsely independent through the shared
   convergence point?** No — both explicitly linked RFC-3425-QUESTIONS
   and RPITIT-112194 rather than treating them as unrelated.
4. **Did either identify a shared stabilization/semantic boundary?** Yes,
   both explicitly, grounding it in RFC 3425's own text rather than
   inventing one.
5. **Did either confuse joint stabilization with joint implementation?**
   Not applicable in the direct sense — neither run had access to the
   eventual joint-stabilization outcome (it postdates cutoff by three
   months and is DIAGNOSTIC-only); what both correctly avoided was the
   nearby trap of treating the *already-landed 2022 implementation's*
   shared file/mechanism, or RFC 3425's *own* convergence pairing, as
   license to merge the other seven, unrelated tickets into one slice.
6. **Did either confuse separate feature gates with permanent
   independence?** No — both explicitly named the shared desugaring
   mechanism and the verified shared file rather than treating the
   2022-09-23 gate split as proof the two features are unrelated.
7. **Did the skill materially change topology?** Yes, for the first time
   since case-301 in this suite (case-302, case-303-corrected, and
   case-304 were all ties on both correctness and topology) — slice count
   differs (9 vs. 8), specifically in how the two literally-unscoped RFC
   sub-questions are handled. See "One DEFENSIBLE point" above.
8. **If topology changed, was the change better supported by evidence?**
   No clear winner, and this write-up declines to call one. The
   with-skill run's choice is more precisely argued from a specific,
   quotable principle (no independent verification path exists for two
   literally-unfiled, unassigned, un-designed questions, so don't force a
   slice) and is arguably more honest about how thin those two items
   really are. The baseline's choice is also defensible and arguably more
   practically useful to a real team (it gives the two open questions
   *something* to track rather than a dangling, slice-less gap) — nothing
   in the frozen grading key or the record itself picks a winner between
   "track it as a lightweight decision-slice" and "name it as an
   explicit non-slice gap," and this write-up is not retroactively
   inventing one now that the runs are in (see this suite's own standing
   rule against tuning against observed output).
9. **Did the skill merely make convergence reasoning more explicit?** No
   — this is the material difference from case-304, where the skill's
   only contribution was format/explicitness on an otherwise identical
   graph. Here the skill's own verifiability-folding text changed an
   actual slice-count/boundary decision, not just how it was reported.
10. **Did baseline already express the same invariant unaided?** Yes, for
    every REQUIRED-level invariant (no over-merging, no over-independence,
    correct convergence linking, no fabricated priority) — baseline
    reasoned soundly on all of these with no assistance. The specific
    difference in Q7 traces to a piece of SKILL.md text baseline had no
    access to, not to a gap in baseline's own reasoning quality.
11. **Are multiple topologies still defensible?** Yes, explicitly, and
    this case's two actual runs demonstrate two of them concretely rather
    than only in the abstract (unlike case-304, where both runs happened
    to converge on the identical DEFENSIBLE choice).
12. **Does this case expose a failure shape not seen in cases 301-304?**
    Yes: a case where both conditions pass every REQUIRED item (a clean
    tie on correctness) *and* the skill still produces a materially
    different topology, via a specific, attributable SKILL.md mechanism,
    on an item the record itself under-specifies (no PR, no assignee, no
    verification path at all) rather than on an item the record merely
    leaves ambiguous between two well-formed alternatives (case-304's
    manager cluster, where both alternatives are equally well-formed).
13. **Does this case materially change our current understanding of the
    skill?** It adds one nuance, not a correction: the verifiability-
    folding rule (added in iteration 3 to stop an unverifiable sub-piece
    from being counted as a second enabler-consumer) also has the effect,
    on real-world data, of making the skill decline to manufacture a slice
    for an organizationally-real but technically bare policy question —
    an effect the synthetic cases and cases 301-304 never exercised,
    because none of them contained an item with literally zero tracked
    implementation work (no PR, no assignee, no design proposal) sitting
    alongside eight items that do have at least a filed, described bug.
14. **Does the result justify any SKILL.md change?** No. Recorded per this
    session's own instruction not to modify SKILL.md regardless of
    outcome. Nothing here indicates the verifiability-folding rule is
    behaving incorrectly — both its effect here (Q7-Q9) and its absence of
    effect on the twelve REQUIRED items (Q1-Q6, Q10) are consistent with
    the rule working as designed; this is new evidence about the rule's
    *reach*, not evidence that it needs to change.

### Comparison to existing evidence

Placed alongside the rest of this suite's real-world evidence: case-302
and case-304 (neutral and pressure) are clean ties on both correctness
and topology; case-303 is a tie on correctness once its REQUIRED #8
defect was corrected, with a granularity-only (not correctness) topology
difference; case-301 is a genuinely mixed result (skill improved on one
axis, regressed on another, both traceable to specific causes). **Case-305
is the first case in this suite to combine a clean tie on every REQUIRED
item with a real, skill-attributable topology difference that isn't
merely granularity or format** — the skill changed an actual
include/exclude-from-any-slice decision on a specific pair of items,
citing its own text almost verbatim, without that change being provably
better or worse than baseline's alternative. Against the synthetic
suite's own iteration-3 finding (the verifiability-folding rule was
originally added to fix case-006/014's over-elevated-enabler failure,
then found to need the "predicted-to-fail" carve-out after case-010), this
is the first time that same rule's behavior has been observed on
real-world, not author-designed, data — and it produced a defensible,
not obviously wrong, effect there too.

The operating envelope this suggests, stated cautiously (one sample per
condition, see limitations below): task-composition's distinct,
repeatable value on this suite's real-world fixtures continues to be
explicit, criteria-traceable structure and, occasionally (case-301,
now case-305), a topology decision traceable to specific SKILL.md text —
not, so far, a demonstrated correctness advantage over a capable,
unguided baseline on the REQUIRED-item axis itself, which baseline has
matched on every real-world case in this suite to date.

### Limitations specific to this case

- **Single sample per condition**, same limitation as every other
  real-world case in this suite — a second sample could resolve
  differently on the one DEFENSIBLE point that actually diverged here.
- **Training-data contamination risk is the most severe in this suite.**
  Rust's AFIT/RPITIT stabilization is extensively documented in public
  blog posts, official announcement posts, and "Async Rust" educational
  material, arguably more heavily represented in general training corpora
  than any single case in cases 301-304. Both tested agents were
  instructed not to use web tools and not to rely on memorized/trained
  knowledge of this history; no transcript referenced any fact absent
  from its five case files (no mention of Rust version numbers, the
  actual stabilization PR, or any post-cutoff date), but this cannot be
  verified or ruled out, and this is the case in the suite where that
  limitation is weakest.
- **The one substantive topology difference found (Q7-Q9) rests on a
  single pair of runs.** A second sample on either condition could
  reproduce the same choice, the other condition's choice, or a third
  variant this write-up hasn't seen; nothing here should be read as "the
  skill reliably declines to slice unscoped policy questions" beyond this
  one observed instance.
- **No comparison against `slice-plan` or `next-best-slice`**, consistent
  with the existing limitation noted for cases 301-304.
