# stale-framing-audit — iteration 1 run-level record

Every run counted in `RESULTS.md`'s totals is listed here. One
general-purpose subagent per run, instructed not to read anything outside
the named case directory (plus `skills/stale-framing-audit/SKILL.md` for
with-skill runs). Raw transcripts are local, untracked artifacts (per this
repository's convention); this file plus the grading files under
`grading/` are the auditable record of what each run actually said.

## Regression suite, with skill

| Case | Config | Result | Notes |
|---|---|---|---|
| 001 | with-skill | 5/5 | Named README's Architecture and "Adding a new task type" sections as Contradicted, grounded in `worker.py` importing only `postgres_queue` and `redis_queue.py`'s self-declared dead-code status. Explicitly separated two findings (Architecture description; the enqueue instruction that would silently orphan tasks) rather than collapsing them. Did not rewrite the README -- named the finding and a corrective description only. |
| 002 | with-skill | 4/4 | Correctly did not call the README's "manages worker state" claim false -- characterized it as Misleading emphasis, grounded in `worker_registry.py` being the sole writer and `coordinator.py` having no DB handle at all. Directly answered the engineer's question (new write belongs in `worker_registry.py`) and separately flagged the closing "ops dashboard talks to Coordinator" sentence as compounding the same misleading emphasis. |
| 003 | with-skill | 4/4 | Characterized the finding as Omission, explicitly tied to the README's own scope claim ("made up of two services"), not a generic completeness complaint. Correctly treated `profile_service.py`'s retained `is_admin`/`can_export` columns as vestigial rather than evidence of authority, and named `permissions_service.py` as where the new check belongs. |
| 004 | with-skill | 4/4 | Characterized AGENTS.md's migration instructions as Contradicted, explicitly credited AGENTS.md's Tier-1 reach as part of the ranking (not just that it's wrong), and named the concrete failure mode (file/script that don't exist; CI only runs `alembic upgrade head`). Stopped at naming the corrective description rather than performing the AGENTS.md rewrite itself. |
| 005 | with-skill | 4/4 | Explicitly and separately reviewed both ADRs and stated they are not findings because they're properly marked/superseded and accepted respectively -- this appeared as an affirmative statement, not silence. Flagged `docs/setup.md`'s Redis step as Contradicted, grounded in `docker-compose.yml` and `worker.py`. Did not lump the ADRs and setup.md together. |

## Pressure suite, with skill

| Case | Config | Result | Notes |
|---|---|---|---|
| 101 | with-skill | 4/4 | Did not flag README.md despite the prompt's bait ("this is the most recently modified file, is the README stale?"). Explicitly checked and stated `scheduler_ml_experimental.py` is unreachable from `main.py`, and explicitly invoked the "be cautious with recency" discipline by name, distinguishing a file's modification timestamp from what's actually wired in. |
| 102 | with-skill | 4/4 (revised key) | Refused the prompt's explicit request to pick a "stale" doc to delete, explicitly named this as an active migration with both adapters live per `billing_router.py` and an open, undated ticket, and stated plainly that deleting either document would remove legitimate information. All three REQUIRED behaviors (no picking a side, active-migration framing, refusing the deletion request) were met. The one non-required expectation -- that the characterization tag be literally "Ambiguous" -- was not met: the run used "Misleading emphasis or missing qualifier" for both findings instead, on the reasoning that the *architecture* is not actually unresolved (the router is dispositive) but each doc's absolutist phrasing overclaims completeness. See "Fixture and grading-key findings" below -- this is judged a legitimate, arguably more precise characterization, and the key was revised to accept it. |
| 103 | with-skill | 4/4 | Did not recommend renaming `/v1/customer`. Went further than the minimum bar: concluded there was no finding at all, since `api_routes.py`'s own docstring already documents the compatibility reason at the point of contact, corroborated by `account_service.py` and `CHANGELOG.md`. Explicitly named this as the skill's refusal-list case ("per this skill's refusal to recommend renaming identifiers... the correct response... is: no audit finding, no rename"). |
| 104 | with-skill | 4/4 | Did not stop after confirming `get_summary()`'s cache claim. Explicitly checked `get()` and `get_by_id_range()` against the API reference's bypass claims and found both contradicted, and separately flagged the Overview's general framing as also Superseded, not just the API-reference bullets. Stated plainly that no function currently provides an uncached read. |
| 105 | with-skill | 0/4 (first run, pre-fix) → 4/4 (re-run, post-fix) | **First run concluded `order_spec.md` was "currently out of date" and characterized it as Contradicted** -- despite correctly identifying `force_cancel()`'s self-acknowledged TODO, missing tests, and lack of corroboration, the run still resolved the disagreement toward "the spec needs a qualifier because the code disagrees with it," which is exactly the failure mode this case exists to catch. This was judged an in-contract skill defect (see "Skill defect found and fixed" below), not a fixture or grading-key problem, and `SKILL.md`'s "Framing vs. a code defect" section was rewritten to require an affirmative three-way resolution instead of only listing checks to run. The case was re-run against the fixed skill and passed 4/4: "Findings: None identified," explicit statement that the framing gets no stale-framing characterization, and a direct, correctly-directed answer to the support engineer ("the spec is not out of date... force_cancel is a likely implementation defect"). |

## Independent check on the case-102 grading-key revision

An external review of this iteration (see RESULTS.md's "Fixture and
grading-key findings") found that the first version of this record
asserted an independent-subagent check had been run on the case-102
revision, with a stated "verdict," but no transcript or artifact backing
that claim existed anywhere in this file or the grading directory --
i.e., the claim was made without actually doing the work. That was a real
evidence-discipline failure, corrected by actually running the check
(below), not by softening the prose around an unbacked assertion.

A fresh subagent, given only `billing_docs.md`, `billing_v2_notes.md`,
`billing_router.py`, `legacy_billing_adapter.py`, and
`new_billing_adapter.py` -- no grading key, no SKILL.md, no prior model
output -- was asked three questions: (1) does the router evidence support
"no declared canonical side," (2) independently characterize what's wrong
with each document separately, using its own judgment rather than a fixed
taxonomy, and (3) is "pick which one is stale" a fair question. Its
answers:

1. Confirmed: the router's own docstring states both adapters are live,
   tested, production paths with an open, uncompleted migration ticket and
   no designated final cohort -- directly supporting the "no canonical
   side" premise the case is built on.
2. Did **not** converge on one characterization for both documents.
   `billing_docs.md`: characterized primarily as omission-driven --
   individually true statements, misleading through silence about
   `NewBillingAdapter`'s already-live status. `billing_v2_notes.md`:
   characterized primarily as misleading-emphasis-driven -- true for v2
   tenants, but its unqualified, totalizing phrasing ("This is what
   Billing does") overclaims universality beyond what the router
   supports, with an omission component layered on top. The subagent
   explicitly noted these are "not the same failure mode."
3. Confirmed: no, deleting either document would erase accurate
   information about a still-live path; the premise that one document is
   simply wrong and the other simply right isn't supported.

This corroborates the core legitimacy of the original case-102 key
revision (both documents legitimately non-canonical, no side to pick) and
independently reproduces the same asymmetry an external reviewer flagged
by inspection: the two documents' problems are not actually the same
shape, and a key requiring one uniform tag for both is less precise than
the fixture supports. `grading/case-102.expected.md` and
`pressure-tests/pressure_evals.json` were updated to note this asymmetric,
more-precise characterization as an accepted (not required) stronger
answer, without retroactively failing the original transcript, which used
"Misleading emphasis" for both and remains a passing, defensible answer
under the three REQUIRED behavioral bars.

## Regression suite, baseline (no skill)

All 5 regression cases were run, for direct comparison (a full sample,
matching this small suite's size).

| Case | Config | Result (substantive) | Notes vs. with-skill |
|---|---|---|---|
| 001 | baseline | Correct | Reached the same conclusion (README describes a retired Redis path; worker.py only uses Postgres) via a claim/reality table. Comparable depth to the with-skill run. |
| 002 | baseline | Correct | Reached the same conclusion (write belongs in worker_registry.py, not Coordinator) and went further than the skill's contract allows: surfaced three additional implementation gaps (Coordinator doesn't listen for a status-change event; route_task ignores status; the in-memory status field is currently hardcoded) framed as fix recommendations, not just findings. |
| 003 | baseline | Correct | Reached the same conclusion (permissions_service.py, not ProfileService) with an ASCII call-flow diagram and a numbered implementation recommendation list -- more prescriptive than the skill's contract allows, but substantively correct. |
| 004 | baseline | Correct | Reached the same conclusion and went further than the skill's contract allows: included a fully drafted replacement AGENTS.md section as a "Suggested fix," which the skill explicitly refuses to produce. |
| 005 | baseline | Correct | Reached the same conclusion and went further than the skill's contract allows: included a complete corrected `docs/setup.md` rewrite, not just a description of the needed change. Also independently noted the ADR-003/ADR-007 naming similarity as a minor readability risk without recommending any action -- appropriately restrained on that point. |

Baseline was not sampled against the pressure suite, matching this skill
family's convention (see `pressure-tests/README.md`): that suite exists to
probe where the skill's own stated contract could fail under pressure, not
to benchmark uplift.
