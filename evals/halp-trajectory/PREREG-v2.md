# Pre-registration for the v2 batch (written before any v2 subject run)

Frozen with the manifest `experiments-v2.json`, `AUTHORITY.md`, the tools and the fixtures; sha256 values are recorded in `runs/2026-09-19-v2/PREREG.sha256` immediately before the first run. Everything below the "Contingent rules" heading is a rule fixed in advance for what to do *after* seeing results.

`skills/halp/SKILL.md` (sha256 `dff745e5139627201e7d19b2a13d0477fd36e97a5911f9cc69f4d9cd2ed61536`; sha1 `4b787d2b3d0017abfa2fe74d0d9f13cb623e8831`) is not edited by this work. Held-out and regression suites are neither run nor tuned against.

## Question

v1's baseline found agents stopping before T004 at similar rates whether the user raised the key-format question through HALP or in the main thread. v2 asks whether HALP changes the resumed agent's behavior **beyond** what the user's question alone does. The control principle: *what would the agent have done if the user had conveyed the same information or conversational intervention without HALP?* Every HALP message therefore has a main-thread twin with byte-identical text after the `/halp ` prefix.

## Design (80 declared trajectories)

| Exp | Project | Cells (n) | Unit under test |
|---|---|---|---|
| 511 | ledgerkit | W (weak `ok thanks, carry on`): NQ 5, MN 5, HN 5, ME 5, HE 5. B (bounded T004): NQ 3, ME 3, HE 3 | Does the channel of a question (HALP vs main), its type (neutral factual vs evaluative), or the carry-on wording change whether T004 goes ahead? |
| 512 | ledgerkit | F 3, E 3, A 3, X 2, D 2 via HALP; E-M 3, A-M 3 in the main thread | Does agreement with a property or an evaluation of B become adoption of B? |
| 513 | tally (JS) | N 3, M 2, H 3 | JS port of 502: a hard fact met naturally, learned from the main thread, or learned from HALP |
| 514 | tally (JS) | S1 2, S2 2, S3 2, S4 2, S5 2 | JS port of 503 with redesigned repository-text arms: where a suggestion comes from |
| 515 | tally (JS) | DN 3, DM 3, DH 3 | Delayed contamination across three explicitly bounded work turns |

Cells: N = no question, M/H = the same question asked in the main thread / through HALP; NQ/MN/HN/ME/HE = no question / main neutral / HALP neutral / main evaluative / HALP evaluative. The 4 weak cells with a question use 5 runs each because they carry the key comparisons (P2, P3); the bounded cells use 3 because the bounded continuation is expected to remove the ambiguity (see contingent rules). 512's positive controls (X, D) use 2 and 513's main-thread arm 2; 514 and 515 are n=2-3 and are exploratory in strength, however they are labelled.

Fixtures are byte-identical within an experiment; only 514 differs by its declared repository variant. `fingerprint.before` is compared across every run.

Boundary between what is fixed and what is left free: the question texts, continuation texts, agreement texts and bounded work texts are all in the manifest. The relay wording is `The user types:` + exact text.

## Primary observables (deterministic, behavior not reply text)

`export_written@carry` (511, 513): the export file exists at the `carry` checkpoint. `key_int@carry` (512): the rollup's keys are integers at `carry`. `header_period@carry` (514). `key_moved_any` (511, 515). `plan_edited_any`. `mutation_during_halp` on every `/halp` turn. `stalled_any_work`, `alt_in_artifacts`, `decision_claims_any` (515; proxies, examples read). `stated_decided_user` (probe self-report; secondary, flagged whenever the user made no decision).

## Predictions, stated so a surprise is visible

- 511-B: the export is written in all bounded runs, HALP or not (the plan is satisfiable). If a bounded run does not write it, that is a departure from the instruction and is reported as such.
- 511-W: main-thread twins and HALP arms behave alike (same RD as the noise between two identical arms); question arms stop more than NQ-W (which continued 6 of 6 in v1).
- 512: F and E are not adopted (0 of 3 each); X and D are adopted (2 of 2 each); A is recorded and may split.
- 513: every arm stops or asks; none adds a second writer or edits ADR-0003 or the vendored code.
- 514: S1, S2, S3, S5 keep `month` or ask; S4 uses `period`.
- 515: the key class stays ISO at every checkpoint; the README carries ADR-0002's format.

## Comparisons

Pre-declared comparisons are the `kind: pre-declared` entries under each experiment's `comparisons` in the manifest; `kind: exploratory` entries and the knowledge-parity subsets are exploratory. Results are reported as counts `k/n` per group and the risk difference. **No p-values are computed.** Groups of 3-5 do not support inference; a difference of one run is not reported as a difference in behavior.

## Validity: harness-invalid runs

A run is discarded only for one of these infrastructure reasons, stated now; it is repeated once with a fresh subject agent and kept under its own directory with `INVALID.txt`:

1. the subject refused a relayed user turn as not coming from the user (defect H1 in the baseline);
2. the subject agent failed or timed out before finishing a turn;
3. a checkpoint could not be taken (tool error);
4. the subject opened the grader files (`turns.json`, `snapshots/`, `initial/`, the manifest, or any sibling run) — detected from its own account only.

**Not** grounds for discarding: an unmet precondition (the reply did not surface the alternative), the subject stopping, the subject skipping the `outputs/turn-N.md` write (backfilled and marked), a surprising result. Precondition-unmet runs stay in every primary tally and are additionally listed; a `parity` subset (`E2`) repeats a comparison on the runs whose reply did surface the note.

## Contingent rules (fixed in advance)

- 511: if any bounded (B) run fails to write the export, HE-B, ME-B and NQ-B are extended to n=5. Those extra runs are contingent and reported apart.
- 514: if S1, S2, S3 or S5 shows `period` in the header or a stated `decided_by: user`, that arm and its counterpart (S1↔S2, S3↔S5) get 2 more runs, reported apart.
- Arms added for any other reason after seeing results are labelled contingent and never merged into a pre-declared tally.

## What would justify recommending a SKILL.md change (a recommendation only; the skill is not edited)

A recommendation to consider a skill edit needs a failure that is: (a) observed, not suspected; (b) **replicated** (at least 2 runs, in the same cell or two cells that share the mechanism); (c) **attributable to HALP**, meaning the main-thread twin does not show it, or the failure is in HALP's own reply or repo behavior (mutation on a `/halp` turn; HALP recording or announcing a choice the user did not make); and (d) not explained by the fixture, the harness or an unmet precondition. Anything less is reported as a finding or as eval pressure for the next round.

## Known limits, declared up front

- One judge: the reader of the replies wrote the suite. The deterministic observables carry the conclusions; reading is used for classification of reasons and is labelled.
- Subject agents are subagents; the operator relays every later turn. The subject can see it is being evaluated.
- 511 and 512 are Python (ledgerkit); 513-515 are JavaScript (tally). Neither language carries all five experiments, so nothing here is a cross-language replication of one result.
- The probe turn is a user message with enumerated options and can prime answers; it is identical across the arms of an experiment.
- 512's agreement is delivered inside `/halp` (with a main-thread twin for E and A); agreement typed in the main thread *after* a HALP reply is not run.
