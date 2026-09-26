# field-debug — eval results

**Run date:** 2026-09-25
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per
run, default settings.
**Harness:** one subagent per run, instructed to read only the target
case's own directory (`evals/field-debug/cases/case-NNN/`) and nothing
else, with no live tools beyond ordinary file reading; with-skill runs
additionally received `skills/field-debug/SKILL.md` and were told to read
and follow it exactly, including its report structure; baseline runs
received the same case files and the same one-line task framing, with no
skill file and no imposed report structure. For the two interactive cases
(`case-004`, both variants), the orchestrating session played the two
human roles named in the case (the partner engineer and Priya, on-call)
directly in the subagent's conversation, replying to whatever the tested
agent asked using the sealed grading key's scripted answer. Raw
transcripts are local, untracked artifacts; the `grading/*.expected.md`
files are the committed, auditable record every claim below cites.

This is iteration 1: the skill's first eval suite, authored and run in the
same session as the skill's own design, on a corpus sized to pressure the
skill's central behaviors, not the full ~32-case target the design dossier
proposed. See "What this proves / what this does not prove" before
treating any of this as strong validation. See "Iteration 2" near the end
of this file for a follow-up round that tightened the skill's identity
around portable field investigation, generalized Handoff into a
mid-investigation Delegate behavior, added a lightweight checkpoint/resume
mechanism, sharpened two epistemic-discipline details, and added one new
case (`case-008`) to pressure the delegation/checkpoint behavior.

## Numeric summary

- 7 cases, one scenario_id pair (`case-002`/`case-003`, same underlying
  incident at two observability tiers), covering 7 of the 12
  differentiator scenarios named in the implementation brief: unfamiliar-
  terrain tool discovery (case-001), distributed RCA with an
  observability-tier axis (case-002/003), an inaccessible intermediate
  service reachable only through one human-operator probe (case-004,
  which covers both of those separately-listed differentiators at once),
  sequential independent failures tempting a unified cause (case-005), a
  misleading status-code transition (case-006), and a POC-to-production
  readiness call (case-007). Not covered this iteration: enterprise
  auth/integration-boundary routing, behavior living outside the repo as
  its own dedicated case, stale architecture documentation, legacy/
  brownfield integration as its own dedicated case, and migration/
  change-safety -- see "Remaining weaknesses and recommended next eval
  expansion."
- With-skill: **34/36 REQUIRED expectations met** across the 7 cases'
  `pressure_evals.json` entries (5 REQUIRED items each for cases 1-6, 6
  for case 7), first run, no case re-run. The 2 unmet items were both in
  case-007 and both resolved by widening that case's grading key to credit
  the higher-quality alternative finding the run actually gave -- see
  "Fixture and grading-key findings." After that revision: 36/36.
- Baseline (no skill) runs were collected for all 7 cases, for contrast,
  not for pass/fail grading against the skill's own report structure and
  vocabulary -- matching this skill family's established convention
  (`evals/state-ownership-audit/RESULTS.md`). Baseline reached the same
  substantive root cause as the with-skill run in all 7 cases.
- Both interactive `case-004` runs (baseline and with-skill) needed a
  mid-conversation resume: the tested agent's own harness returned control
  after asking Priya its question, before her answer arrived, rather than
  blocking on it in one turn. This is a harness/orchestration property of
  how these runs were executed, not a skill defect -- both runs correctly
  waited to be resumed before concluding, and neither guessed a root cause
  in the gap.

## Per-case results

| Case | Scenario | With-skill | Baseline (no skill) |
|---|---|---|---|
| 001 | Silent SKU-sync drop; the diagnosis lives in a dead-letter file, not the job's own summary log | 5/5, plus an unanticipated fixture finding (see below) | Reached the same root cause and same narrow-fix recommendation independently |
| 002 | Checkout latency spike; two live hypotheses, full telemetry | 5/5 | Reached the same conclusion, including correctly separating "the deploy enabled the exposure" from "the vendor's own slowdown triggered it" |
| 003 | Same incident as 002, request logs unavailable for the window | 5/5 -- explicitly named the log gap, did not fabricate log content | Reached the same conclusion; also explicitly named the log gap unprompted |
| 004 | Partner webhook signatures failing; one on-call engineer, one allowed probe | 5/5 -- asked exactly one well-targeted question, converged correctly on Priya's answer, flagged the residual 2-day timing gap as UNKNOWN rather than asserting it | Reached the same conclusion via the same single question and the same honest UNKNOWN flag on the timing gap |
| 005 | Two unrelated failures near a shared, irrelevant deploy | 5/5, plus a stronger discriminator (the deploy postdates both incidents' actual onsets, not just "doesn't touch the code") | Reached the same conclusion via the diff-content argument alone |
| 006 | "500" reported by a customer; actually a 504 from the proxy, relabeled by the client SDK | 5/5 | Reached the same conclusion and the same proxy-vs-app attribution |
| 007 | POC readiness call: one manufactured non-finding (auth), a real blocker, a scale/infra trap | 5/6 against the original key (see below); 6/6 after the key was widened | 6/6 against the original key, including the specific finding (upload size) the with-skill run substituted for |

## Fixture and grading-key findings

Two with-skill runs surfaced real subtlety this suite's grading keys
either hadn't fully accounted for or had over-specified, in both cases
matching this skill family's established precedent (see
`evals/state-ownership-audit/RESULTS.md`'s "Fixture and grading-key
findings" section) of revising toward the higher-quality answer rather
than treating a legitimate improvement as a miss.

- **Case 001** was designed around one dominant discriminating signal
  (11 of 12 failing SKUs share one feed and one error shape). The
  with-skill run additionally noticed that `sync_job.py`'s 3x retry loop
  writes a dead-letter record on *every* attempt, so `var/dead_letters/`
  contains 36 lines for only 12 unique failing records, and
  `tools/inspect_dead_letters.py`'s own printed counts are consequently
  3x the real unique-failure count -- a genuine property of the fixture
  as written, and a legitimate catch (retries don't just fail to help
  here, they inflate the evidence trail 3x). This didn't require a
  grading-key change -- the key never claimed anything about absolute
  counts -- but it's recorded here because it's exactly the kind of
  detail this skill's "debug by observation" discipline is supposed to
  surface, and it should inform anyone reusing this fixture for a
  degradation-curve or count-sensitive follow-up case.
- **Case 007** was designed with one anticipated "second concrete
  finding" (a missing upload-size limit) alongside the intended
  centerpiece finding (unrecoverable data loss on OCR-parse failure).
  The with-skill run instead named two different, equally real, arguably
  more consequential findings: whether `results.db` -- the only durable
  record of a real submission -- survives a container restart or
  redeploy (genuinely unaddressed by the fixture's `README.md`, correctly
  flagged as unresolved rather than guessed either way), and that the
  service runs via Flask's development server with no production WSGI
  server in `requirements.txt`. Both are real, evidenced properties of
  `main.py`/`README.md`, not fabrications, and at least as relevant to a
  pilot handling real financial data as the anticipated upload-size gap.
  The grading key's REQUIRED item was widened from "names the missing
  upload size limit" to "names at least one further concrete, evidenced
  concern beyond the parse-failure gap," listing all three acceptable
  findings by name. **This revision was made by the same person who
  authored the fixture, the skill, and the key, and -- unlike the
  precedent it follows -- was not independently re-checked by a second,
  context-free reviewer before this write-up; that check is a named gap,
  not a step skipped silently.** The baseline run for this same case
  happened to name the originally-anticipated upload-size gap and would
  satisfy the key either way, which is at least mild corroborating
  evidence that the widening credits a real alternative rather than
  rationalizing a miss, but it is not a substitute for independent
  review.

## SKILL.md corrections

None. No run in this suite surfaced a defect, contradiction, or missing
instruction in `skills/field-debug/SKILL.md` itself -- every with-skill
run correctly selected a mode, applied the evidence vocabulary, held to
the root-cause standard, and (in case-004) asked exactly one discriminating
question without further prompting. This is one iteration on a small,
synthetic, single-author corpus with no case yet designed to pressure
Handoff mode, sibling routing, or genuine non-convergence (see "Remaining
weaknesses" below); a correction may well surface once those gaps are
covered.

## What the baseline comparison shows

Every baseline run reached the same substantive root cause as its
with-skill counterpart across all 7 cases, including the interactive
one-probe case (case-004) and the observability-degraded case (case-003) --
consistent with the pattern already documented across this skill family
(`state-ownership-audit`, `lifecycle-audit`, `domain-orientation`): a
capable model with no skill and no imposed structure often reaches sound
engineering judgment on cases like these. This suite's evidence does not
show the skill producing conclusions a strong baseline reliably misses.

Where the with-skill runs differed, consistently:

- **Explicit report structure and evidence tiering.** Every with-skill run
  used the skill's exact section headings (System model, Failure, Evidence
  chain, Reasoning changes, etc.) and tagged claims OBSERVED/INFERRED/
  ASSUMED/UNKNOWN; baseline reports were well-organized prose without a
  reusable, checkable vocabulary or a mandatory "remaining uncertainty"
  field. Both case-002/003 with-skill runs and the case-004 with-skill run
  explicitly tagged the genuinely unresolved fact (why the vendor slowed
  down; the 2-day gap before the partner noticed) as UNKNOWN rather than
  omitting it or asserting a guess -- baseline runs surfaced the same gaps
  in prose but without a structural requirement forcing the field to exist.
- **The interactive discipline (case-004) held under both conditions.**
  Both runs asked exactly one well-targeted question rather than several,
  and both correctly treated it as a discriminating probe rather than a
  vague request for more context. This suggests the "ask one discriminating
  question, not several" behavior this case exists to pressure is not
  purely an artifact of the skill's explicit instruction to do so -- the
  case's own framing (Priya has time for exactly one check) may be doing
  real work on its own. A version of this case without that framing spelled
  out as clearly, run baseline-only, would be needed to separate the two
  effects; this suite does not do that.
- **Productionization triage (case-007).** Both runs correctly avoided
  manufacturing the auth non-finding and correctly avoided cargo-culting
  a queue/autoscaling recommendation neither the fixture nor the pilot's
  scale calls for -- this suite's evidence does not show the skill's
  explicit "don't cargo-cult infrastructure" instruction producing
  different restraint than baseline showed on its own.

Read plainly: this iteration's evidence suggests the skill's value on
these specific fixtures is less about reaching different root causes and
more about (a) forcing a checkable evidence-tiered structure and a
mandatory uncertainty field, and (b) making the interactive
one-discriminating-question discipline and the anti-cargo-cult restraint
explicit and named, rather than incidentally present. That is a real but
more modest claim than "the skill finds things baseline misses," and this
suite's case count does not establish how consistently that structural
difference would replicate, or whether it matters when the underlying
model is less capable than the one used here.

## What this proves / what this does not prove

**What it's suggestive of:** across 6 scenario families -- terrain/tool
discovery, distributed RCA with a genuine observability-tier contrast,
an interactive single-probe investigation through a human proxy, two
sequential unrelated failures resisting a unified explanation, a
misleading client-visible status code, and a POC production-readiness
call -- the with-skill runs consistently (a) discovered evidence sitting
outside the one file a less careful investigation would fixate on (the
dead-letter file, not the summary log line; the nginx layer, not just the
app logs); (b) discriminated between live hypotheses using the actual
evidence rather than defaulting to the more dramatic or more recently-
changed candidate (ruling out the inventory-svc pool change and the
platform-svc deploy by checking their own metrics/diffs, not by priors);
(c) in the one case designed to require it, asked a single, correctly-
targeted discriminating question of a constrained human proxy and
correctly waited for and used the answer; (d) avoided the two
evidence-discipline traps this suite specifically built in (crediting the
SSO-ingress paved road instead of manufacturing an auth finding in
case-007; not treating "500 Internal Server Error" as a confirmed
application fact in case-006); and (e) avoided cargo-culting
infrastructure the fixture's own scale didn't call for.

**What it does not prove:** every case was run once per condition with one
model family and default settings -- this is not a statistically powered
benchmark, and any single case could look different on a repeat sample.
All 7 fixtures (8 case directories) are synthetic, single-author-
constructed, in the 3-6-file range, written by the same person who wrote
the grading keys and the skill -- the same known source of unintentional
alignment between what a fixture rewards and what `SKILL.md` happens to
emphasize that this repo's other skills' RESULTS.md files already
disclose, and the same person revising one grading key after seeing the
with-skill output is the same bias to disclose plainly here, with the
added caveat (unlike this family's usual precedent) that the revision
was not independently re-checked by a second reviewer this iteration.
Because baseline reached the same substantive conclusion in every case,
this suite provides no evidence that the skill improves *accuracy* on
fixtures this size and this synthetic; it only provides evidence about
*structure, discipline, and the interactive/anti-cargo-cult behaviors*
named above. The suite does not test: a genuinely large or messy real
codebase (every fixture here is small and clean by construction); a case
where the environment cannot answer and no human proxy exists either
(true Handoff-mode territory -- not exercised at all this iteration); a
case requiring actual live tool execution rather than reading a static
evidence set (no case here required running a script, querying a live
system, or using an MCP server); enterprise middleware/vendor-console
archaeology as its own dedicated case, despite the skill's text treating
it as first-class; a model materially weaker than the one used here; or
more than one competing hypothesis surviving to the very end (every case
in this suite has exactly one fixture-supported root cause once evidence
is actually checked -- none tests a case that remains genuinely
ambiguous even after full investigation, which is what field-debug's
"explicitly fail to converge" contract is for).

## Remaining weaknesses and recommended next eval expansion

- **Handoff mode is entirely untested.** Every case in this suite is
  solvable from the evidence given (with or without a human proxy). No
  case tests the skill actually stopping at an access/ownership wall it
  genuinely cannot cross, producing the Handoff report instead of a
  root cause. This is arguably the highest-priority gap to close next.
- **No case tests genuine non-convergence.** Related to the above: the
  root-cause standard's "explicitly fail to converge rather than
  manufacture a plausible-sounding guess" clause has no case designed to
  pressure it -- every fixture here has a discoverable, discriminated
  answer.
- **Enterprise/legacy terrain is present only as flavor (case-004's
  webhook/secrets-rotation scenario), not as its own dedicated case.**
  The brief's differentiator list separately named "enterprise
  auth/integration boundary," "behavior living outside the repo," "stale
  architecture documentation," and "legacy/brownfield integration" as
  distinct pressure points; this iteration covers none of them as a
  dedicated case, only touches adjacent territory incidentally.
  Migration/change-safety is also entirely absent.
- **No case tests routing to a sibling skill under actual pressure.**
  The skill's "How this composes with neighboring skills" section and
  its refusal to re-derive identity/authority or state-ownership verdicts
  is asserted in `SKILL.md` but never exercised by a case in this suite
  that specifically dangles an identity/authority or state-ownership
  question mid-investigation to see whether the run correctly routes to
  `identity-authority-audit`/`state-ownership-audit` instead of
  re-deriving that judgment inline.
- **No case requires live tool use.** All 7 cases are static evidence
  sets an agent reads; none requires actually running a script, querying
  a live system, or using an MCP server to obtain evidence not already
  sitting in a file -- a real gap given the skill's own emphasis on
  "debug by observation where possible."
- **The observability-tier pairing (case-002/003) has only two tiers.**
  The skill's design brief suggested several (full telemetry / no logs /
  no traces / topology-only / an undisclosed useful tool / one human
  probe / stale docs); this suite tests exactly one degradation step
  (dropping logs only) on exactly one scenario. The data shape (a shared
  `scenario_id`, paired grading files cross-referencing each other) is
  preserved so more tiers can be added to the same scenario later without
  restructuring, per the implementation brief's instruction not to build
  degradation-curve infrastructure yet -- but no infrastructure exists
  yet to actually compute or report a degradation curve across more than
  two tiers, and none was built this iteration.
- **`eval-commons` was inspected, not adopted.** Per the implementation
  brief's instruction to check that sibling repo before building bespoke
  eval machinery: its case/pressure-test corpus is built around review and
  evidence-discipline behaviors (spec review skepticism, git-state
  honesty, output discipline, repository safety) rather than live
  debugging/RCA/terrain-discovery scenarios, and its harness (`commons.py`,
  playlists, matched pairs, materialize/release pipeline) is materially
  heavier than this repo's `cases/`+`grading/`+`pressure_evals.json`
  convention. No fixture or pressure-test from it was a direct donor for
  this suite; its `stale-agent-instructions-misdirect-next-action` and
  `readme-claim-contradicted-by-code` entries are a reasonable inspiration
  for a future stale-documentation case, but nothing was imported
  verbatim.
- **CASE SEED harvesting is designed, not exercised.** `SKILL.md`
  describes the lightweight running-note mechanism and the CASE SEED
  schema, but no case in this suite, and no run against these cases,
  actually produced a CASE SEED artifact to check the mechanism against
  real investigation behavior -- it remains unproven in practice.
- **Grading was performed by the fixture/skill author, largely without
  the independent adversarial re-check this skill family's precedent
  calls for.** Case-007's key revision is the one place this is disclosed
  explicitly above; the same caveat applies more broadly to every case's
  first-pass grading in this iteration.

Recommended next expansion, in priority order: (1) a Handoff-mode case
with a genuine, uncrossable wall and no human proxy; (2) a case built to
remain genuinely unresolved even after full investigation, to pressure
the "explicitly fail to converge" contract; (3) a dedicated
sibling-routing case (an identity/authority or state-ownership question
surfacing mid-investigation); (4) a case requiring actual live tool
execution rather than a static evidence set; (5) the remaining named
differentiators not yet covered (stale documentation, migration/change-
safety, a dedicated enterprise-integration-boundary case) once the above
four are in place.

## Iteration 2 (2026-09-25)

**What changed in `SKILL.md`, and why.** This round tightened the skill's
identity around its primary intended use: a portable investigation
protocol for debugging inside customer-owned environments (enterprise/
brownfield integration, legacy/hidden-behavior systems, and POC-to-
production judgment calls), not a general autonomous-agent framework.
Concretely:

- Rewrote the frontmatter description and added an intro paragraph
  naming the customer-owned-environment framing and the "use the
  customer's native machinery; preserve enough state to survive leaving
  it" principle.
- Generalized the previously terminal Handoff mode into a new **Delegate**
  behavior nested inside Diagnose (`investigate -> identify a bounded
  uncertainty -> delegate -> receive evidence -> assimilate -> continue`),
  with a QUESTION/WHY/KNOWN/REQUEST/CONSTRAINTS/RETURN template and an
  explicit instruction to separate a delegate's observation from their
  interpretation (an `OBSERVED` / `INFERRED BY TOOL` / `UNKNOWN` worked
  example). Handoff itself now explicitly means "no delegate can cross
  this either," not just "I personally can't."
- Added a lightweight **Checkpoint and resume** section (Objective,
  current system model, observations, active/ruled-out hypotheses,
  assumptions, unknowns, constraints, last-known-good/first-known-bad,
  next discriminating move, and a named "time-sensitive evidence to
  revalidate" field) with a `load -> re-ground -> identify deltas ->
  continue` resume discipline, distinguishing stable facts from
  runtime-perishable ones.
- Reworded the confirmatory-evidence claim in the root-cause standard:
  previously "an experiment that would only confirm the current favorite
  is not evidence, it's decoration"; now confirmatory evidence can still
  be real evidence, and the actual failure mode named is treating a
  non-discriminating result as if it had settled the question.
- Added a documentation-vs-runtime-truth distinction to the enterprise/
  legacy terrain section, with an `OBSERVED`/`INFERRED`/`UNKNOWN` worked
  example (a README's SSO-ingress claim).
- Folded in a short, explicitly non-formal action-selection consideration
  (access, observability, blast radius, time, human help, query cost) and
  a one-line note that mitigation may proceed before root cause is fully
  known.
- Updated the composition, refusals, and anti-patterns lists to name the
  three new failure modes (laundering a delegate's conclusion into an
  observation, laundering documentation into confirmed runtime fact,
  reusing a stale checkpointed fact without revalidating it).

No case-harvesting infrastructure, cost optimizer, or continuity
benchmark suite was added, per this iteration's explicit scope -- these
were deliberate omissions, not oversights.

**Grading-key language sharpened, not loosened.** `grading/case-007.
expected.md`'s auth-related REQUIRED item was reworded to fail an answer
in *either* direction: flagging the missing app-level auth as a defect
(as before), or writing as if the README's SSO-ingress claim were an
independently confirmed runtime fact rather than the documented system
model. This is a wording tightening prompted directly by this iteration's
documentation-vs-runtime-truth distinction, not a response to any run
result -- no case-007 run was repeated against the reworded key this
iteration, so it has not been re-verified against fresh output. That is a
named gap, not a step skipped silently.

**New case: `case-008` (checkpoint / delegation / assimilation).** A
static fixture (no interactive harness needed, unlike `case-004`):
`checkpoint.md` is a structured checkpoint a fictional colleague ("Marco")
wrote before going off-shift mid-investigation, including a Delegate
request he sent to NetOps; `delegation_response.md` is NetOps' reply
(a real observation -- a packet capture showing SYNs sent but never
ACKed -- plus NetOps' own admittedly-unverified guess, "probably a
firewall rule," alongside two attachments they call "probably
unrelated": `deploy_log.md` and `security_group_config.md`). Those two
attachments actually pin the mechanism down precisely: a routine
cert-rotation redeploy moved the calling service's gateway pods to a new
CIDR block the destination's security group was never updated to allow,
so the redeploy's own traffic falls through to a `deny all` rule -- a
firewall/CIDR staleness bug, not a generic "networking issue." The task
is to resume the investigation from these four files with no further
access to Marco or NetOps and reach a conclusion.

Run once per condition, fresh `general-purpose` subagents, same harness
convention as iteration 1 (with-skill additionally received and was told
to follow `skills/field-debug/SKILL.md`; baseline received the same case
files and one-line task framing, no imposed structure).

| Case | Scenario | With-skill | Baseline (no skill) |
|---|---|---|---|
| 008 | A colleague's checkpoint plus a delegated NetOps reply that offers an unverified guess and two attachments that actually pin the mechanism down | 6/6 | 5/6 -- missed the "flag a checkpointed time-sensitive fact as needing revalidation" item |

**Both runs correctly did the substantive work.** Both independently:
built on Marco's checkpoint rather than restarting the investigation from
scratch; correctly separated NetOps' actual observation (SYNs sent, never
ACKed, no response from the destination) from NetOps' own conclusion
("probably a firewall rule," which NetOps itself flagged as an unchecked
guess) instead of accepting the guess as the root cause; used
`deploy_log.md` and `security_group_config.md` to reach the specific
CIDR-staleness mechanism, explicitly correcting NetOps' own "unrelated"
characterization of the redeploy; correctly retired the pool-exhaustion
and destination-side-slowness hypotheses using the packet-capture
evidence; and did not fabricate access beyond what NetOps actually
provided. The with-skill run additionally used the skill's own Delegate
vocabulary verbatim ("NetOps' own conclusion ... was their unverified
guess (INFERRED BY TOOL), not something they had confirmed"). Both runs
also surfaced the same real, evidence-based residual doubt on their own
initiative -- an unexplained ~4-minute gap between the redeploy's
completion and the first observed failure, and tension between that gap
and the failure's sharp (non-ramping) onset -- rather than papering over
it, which both this suite's convention and the skill's "remaining
uncertainty is mandatory" requirement call for.

**Where the two runs actually diverged.** Marco's checkpoint explicitly
named the ~8% failure rate and ~30% pool-utilization reading as
"time-sensitive evidence that should be revalidated on resume." The
with-skill run picked this up directly, flagging in its own "remaining
uncertainty" section that the 8% figure is "a single ~14:10 UTC snapshot
that hasn't been re-measured since -- trend data doesn't exist here." The
baseline run reused the same 8% figure throughout its otherwise
equally-rigorous report without ever flagging it as a stale,
un-reconfirmed snapshot -- it named other genuine unknowns (unverified
payments-svc telemetry, an unconfirmed assumption about the new pod
range being exhaustive) but not this one. This is the first case in this
suite where a specific, checkable REQUIRED item's outcome differs between
conditions, and it lines up with a piece of the skill's text added this
iteration for exactly this purpose (the checkpoint's named
"time-sensitive evidence" field) rather than with anything already
present in iteration 1.

**What this one case does and does not show.** It is one run per
condition on one synthetic, single-author fixture -- not evidence that
baseline "always" misses a stale-data flag, and not evidence that the
skill's checkpoint field reliably produces this behavior across
different scenarios. It is evidence that, on this fixture, the skill's
explicit "revalidate before relying on it further" instruction produced
a concrete, checkable behavior (naming a specific figure as unconfirmed)
that a comparably careful baseline run, working from the same evidence
and reaching the same root cause, did not spontaneously produce. That is
consistent with iteration 1's overall finding (the skill's value showing
up in structure and discipline rather than in reaching a different
conclusion), but sharper than iteration 1's evidence because it is tied
to one concrete field-level omission rather than a general "baseline
reports checked the same ground in prose." This case was not designed to,
and does not, exercise: a scenario where the tested agent must *author* a
Delegate request itself (this case only requires assimilating one already
written into the checkpoint); Handoff proper (an uncrossable wall with no
delegate available at all -- still completely untested in this suite);
or routing to a sibling skill under real pressure (also still untested).

**No `SKILL.md` corrections this iteration.** Neither run exposed a
defect, gap, or ambiguity in the new Delegate or Checkpoint-and-resume
text; both applied it (or, for baseline, arrived at equivalent judgment
without it) cleanly on the first attempt.

## Cumulative numeric summary (recomputed at write-up time, both iterations)

- 8 cases total (7 from iteration 1, plus `case-008`). With-skill:
  **42/42 REQUIRED expectations met** across all 8 cases' `pressure_
  evals.json` entries (5 each for cases 1-6, 6 for case 7 post-revision,
  6 for case 8) -- the case-007 count reflects the widened key from
  iteration 1, not a re-run against the further-reworded auth wording
  from this iteration (see above; not yet re-verified).
- Baseline was graded pass/fail against `pressure_evals.json`'s REQUIRED
  items only for `case-008`, matching the point this iteration introduced
  a case where the two conditions' answers could differ on a specific,
  named item; it scored 5/6, missing only the stale-data-revalidation
  item. Baseline for cases 1-7 remains ungraded against those items by
  design (contrast only, per this skill family's convention) and is not
  retroactively scored here.

## Remaining weaknesses and recommended next eval expansion (updated)

Iteration 1's list mostly still holds. Updates from this iteration:

- **Continuity/checkpoint/delegation-assimilation is now covered by one
  case** (`case-008`), where it previously had zero. This item is
  downgraded from "entirely untested" to "one case, one run per
  condition, single fixture design" -- still the highest-value next
  addition if a second, differently-shaped continuity case is wanted,
  but no longer a complete gap.
- **Still fully untested:** Handoff proper (an uncrossable wall with no
  delegate reachable at all -- `case-008` tests Delegate succeeding, not
  Handoff triggering); a case where the tested agent must originate a
  Delegate request itself rather than assimilate one already written;
  genuine non-convergence; sibling-skill routing under real pressure;
  live tool execution; enterprise/legacy terrain as a dedicated case
  (still only present as flavor); stale architecture documentation as
  its own case (the closest existing material is `case-007`'s auth
  trap, which is a *correct*-documentation case, not a stale one); and
  migration/change-safety.
- Per this iteration's explicit scope, no further case expansion, no
  external benchmark import, and no continuity benchmark suite were
  attempted -- these remain deliberately deferred, not forgotten.

## What this proves / what this does not prove (iteration 2 addendum)

Iteration 1's statement of what this suite proves and does not prove
still applies in full; this iteration adds one narrower, more concrete
data point on top of it: on one fixture, the skill's newly-added
checkpoint "time-sensitive evidence" field produced a specific, checkable
behavioral difference from baseline (flagging a stale metric baseline
reused uncritically) that iteration 1's evidence did not contain. This
does not establish a rate, does not generalize past this one fixture, and
was authored, run, and graded by the same person who wrote the skill
text it's evaluating, with no independent second-reviewer check this
iteration (the same disclosed limitation as iteration 1's case-007
revision). It should be read as "the mechanism can work, once, on a
fixture built to exercise it" -- not as confirmation that it reliably
will.

## Iteration 3 (2026-09-25): adversarial review, SKILL.md corrections, 5 new cases

This iteration followed an adversarial review of the skill and the first
two iterations' evals, conducted by a fresh reviewer session with no
access to this file's prior conclusions. That review is not reproduced
here; only the concrete, repository-verified defects it identified, and
what was actually done about them, are recorded below. Two categories of
review claim were explicitly distinguished throughout: a defect the
reviewer directly verified against files in this repository (acted on
immediately) versus a suspected weakness inferred from reading rule text
without running anything (turned into eval pressure -- a new case -- not
acted on directly, per this repo's `AGENTS.md`).

### SKILL.md corrections made before any new case was run

These three were independently verified in-repo (not inferred) before
being fixed:

1. **Sibling-skill routing named an unavailable skill.** `SKILL.md`'s
   frontmatter, composition section, and refusal list all named
   `identity-authority-audit` as a skill to route identity/authority
   questions to. Verified: no `skills/identity-authority-audit/` exists
   on `main` or on this branch -- only an open, unmerged PR branch and an
   untracked eval directory. An installation that has this skill but not
   that one would follow a refusal instruction pointing at nothing.
   Fixed: removed `identity-authority-audit` from the frontmatter
   description; reworded the composition section to state explicitly that
   routing assumes the named sibling is actually installed, and that
   field-debug reasons about the sub-question directly (flagging the gap)
   when it isn't; reworded the matching refusal-list entry the same way.
2. **Testimony/vantage-point semantics.** The evidence vocabulary listed
   "a person's direct answer" under OBSERVED without qualification, while
   the Delegate section separately (and correctly) warned that a
   delegate's answer usually arrives as interpretation, not raw
   observation -- an unresolved tension between two parts of the same
   document. Fixed: the OBSERVED bullet now states that a person's answer
   is OBSERVED as *what they reported*, not automatically as what it
   establishes, and that a check run from the wrong vantage point,
   environment, or time window is a real observation of that check, not
   evidence the underlying question is settled.
3. **Two grading keys asserted certainty their own fixtures didn't
   support.** `grading/case-004.expected.md` required a "conclusive" root
   cause but never accounted for a ~2-day gap between the secret rotation/
   partner handoff (Sept 21) and the reported failure onset (Sept 23).
   `grading/case-008.expected.md`'s BONUS item credited a timing
   correlation as "plausibly explained by connection-pool cycling" with no
   fixture evidence for that specific mechanism. Both keys were reworded
   to require the mechanism as conclusive while requiring the unexplained
   timing gap to be named as an open gap, not resolved away -- not
   loosened, tightened toward what the evidence actually supports. Neither
   change was re-verified against a fresh run of cases 004/008 this
   iteration (case-004 and case-008 were not re-run); that is a named gap,
   not a step skipped silently.

A fourth reviewer claim -- that case-004's "asks exactly one question"
requirement mostly tests prompt-following rather than judgment, and that
case-007's grading rewards restraint more than case-001/008's do -- was
not acted on. Neither is a verified defect in the sense the three above
are; they're framing observations about existing, already-shipped cases
that no run this iteration contradicted. Left as-is.

### Five new cases: P1/P3/P4/P5/P6 (enterprise, legacy-archaeology, and
POC-to-production coverage)

Per the reviewer's own priority ranking, five new cases were built,
targeting three previously-named coverage gaps from iteration 2's
"Remaining weaknesses" list: enterprise/brownfield terrain, legacy-system
archaeology, and POC-to-production identity risk. Design constraints
applied to all five, per instruction: no prompt claims the evidence given
is complete; the load-bearing evidence is discoverable by exploring the
given working directory, not announced by the prompt; each case's initial
directory is a foothold into a larger system (an ops config layer, a
warehouse-owned DB trigger, a partner's own acknowledgment channel, a
queue-manager topology) rather than the whole system living in one
obvious file.

| Case | Scenario |
|---|---|
| 009 | Ticket blames the export code; the actual cause is a stale ops-owned config override shadowing a fix that already shipped to `main` three months earlier |
| 010 | An MQ admin's earlier answer in the incident thread never states which of two identically-named queue managers it covered, or whether it covers the incident window at all |
| 011 | A real, evidenced application bug explains 14 of a reported 1,186-order gap; the other ~1,172 live in a warehouse-owned DB trigger outside the service's own code |
| 012 | A "cosmetic" encoding change silently breaks a fixed-width byte-length contract for accented names; the partner's own rejection reason sits unread on disk |
| 013 | A ServiceNow ticket-creation POC authenticates as the individual builder's personal account against a dev-only tenant |

Each case was run once per condition (baseline: same case files, one-line
task framing, no skill file, no imposed structure; with-skill: same case
files plus `skills/field-debug/SKILL.md`, told to follow it exactly),
using fresh `general-purpose` subagents with file/shell access restricted
to an isolated copy of that case's own directory (plus the skill file for
with-skill runs), instructed not to explore anything else. Every run's
full final report was read and graded by hand against that case's
`pressure_evals.json`/`grading/*.expected.md` REQUIRED items -- including
each key's new cross-cutting "hiding-behind-uncertainty" item (fails
either overclaiming settled certainty the evidence doesn't support, or
refusing to commit to a conclusion the evidence has actually settled).

**A fixture defect surfaced by an actual run, fixed before grading
continued.** Case-010's original grading key asserted, as hidden ground
truth, that the incident-thread reply came from checking `QM_QA01`
specifically -- but no agent-visible file in the fixture actually states
which queue manager was checked; that fact existed only in the grading
key, not in anything discoverable. Both the baseline and with-skill runs
independently surfaced this by reasoning about the ambiguity correctly
(neither guessed a queue manager the fixture didn't support) or, in
baseline's case, by *demonstrating the failure the key was supposed to
detect* in a form the key hadn't anticipated (see below). The key was
rewritten to require identifying the ambiguity itself (queue manager
genuinely unstated, not "stated as QA and missed") rather than a specific
hidden answer the fixture never actually encoded -- fixed, not loosened:
the corrected key is strictly harder to fake, since it no longer accepts
naming either queue manager as the "confirmed" one.

**A second grading-key defect surfaced by an actual run.** Case-013's
original key blanket-forbade recommending "retry/idempotency
infrastructure," modeled too closely on case-007's unrelated
auth-scale-infra pattern without checking whether it actually applied
here. The baseline run correctly, with direct code evidence (no dedup key
anywhere on the webhook-to-ticket path), flagged that a redelivered
alert-manager webhook would create a duplicate ServiceNow ticket -- a
real, evidence-backed finding, not cargo-culting. The key was narrowed to
forbid only heavyweight infrastructure investment (a message queue, an
autoscaler) nothing in the fixture calls for, while explicitly crediting
an evidenced dedup-key gap on the ticket-creation path itself as a
legitimate finding. Both runs were re-graded against the corrected key
(below); this key change was made after seeing the baseline run's
specific finding, without a second re-check this iteration -- disclosed
per this repo's own precedent for the same situation in iteration 1.

### Per-case results (both conditions graded against the corrected keys)

| Case | With-skill | Baseline | Notable difference |
|---|---|---|---|
| 009 | 6/6 REQUIRED + BONUS | 6/6 REQUIRED + BONUS | None -- both found the override via the startup log and overrides file, neither touched the code, both flagged the ~3-months-vs-~3-weeks timing gap as UNKNOWN rather than resolving it |
| 010 | 6/6 REQUIRED + BONUS | **5/6 REQUIRED, BONUS missed** | Baseline's own re-scoped delegation request asserted, unsupported by the fixture, that Sam's prior check "already confirmed [QM_PROD01] clean" -- the same overclaim-a-vantage-point-as-settled failure this case exists to catch, just aimed at the opposite queue manager from what a shallow reading would guess. The with-skill run explicitly tagged the historical-`GL_MQ_ENV` claim ASSUMED rather than confirmed and never asserted which queue manager the prior check covered, satisfying every REQUIRED item and the BONUS |
| 011 | 6/6 REQUIRED + BONUS | 6/6 REQUIRED + BONUS | None -- both explained the 14-record parse bug, explicitly compared it against the 1,186 reported gap, found the warehouse-owned dedupe trigger unprompted, and named it a 2015-era scale regression |
| 012 | 6/6 REQUIRED (incl. hiding-behind-uncertainty) + BONUS | 6/6 REQUIRED + BONUS | None -- both independently executed `build_record` against the sample data to verify byte-length overflow, found the unread acknowledgment files, and rejected the passing ASCII-only test as proof of correctness |
| 013 | 6/6 REQUIRED (corrected key) + partial BONUS | 6/6 REQUIRED (corrected key) + partial BONUS | Both named the personal-credential blocker, its consequences, and the dev-tenant-only evidence scope. The with-skill run additionally named, explicitly and by name, that `identity-authority-audit` was the sibling skill this question would ordinarily route to, that it was **not installed in this session**, and that it was therefore reasoned through directly rather than deferred or silently worked around -- a live, first-time demonstration of the sibling-routing-unavailable fallback this iteration's SKILL.md fix (see above) was written to produce, not merely asserted |

**Numeric summary, this iteration's 5 cases:** with-skill 30/30 REQUIRED
items met (6+6+6+6+6, using each case's post-correction key) plus 4 of 5
BONUS items fully met (case-013's partially); baseline 29/30 REQUIRED
(missing one item in case-010) plus 3 of 5 BONUS items fully met
(case-010's BONUS missed entirely; case-013's partially, same as
with-skill).

*Correction (made during iteration 5, below):* the two rows above and this
numeric summary originally read "7/7" for case-012 and totaled 31
REQUIRED items. `evals/field-debug/grading/case-012.expected.md` has held
exactly 6 REQUIRED items since it was committed (verified via `grep -c
"^- REQUIRED"` against the file's one and only commit, `5ed834c` --
never edited since) -- this was a miscount in the original write-up, not
a grading-key change or a re-graded case. Fixed here, not silently: the
correct totals are 6/6 for case-012 in both conditions, 30/30 REQUIRED
with-skill and 29/30 baseline for this iteration's 5 cases.

### What this iteration's evidence shows, and does not show

Four of five cases replicate this skill family's now-consistent pattern:
a baseline run with no skill and no imposed structure reaches the same
substantive conclusions a with-skill run does, on fixtures this size and
this synthetic. Case-010 is the one case in three iterations of this
suite where the with-skill and baseline runs' *substantive conclusions*
differ in a way traceable to a specific instruction in `SKILL.md` (the
documentation-vs-runtime-fact distinction, added in iteration 2 for an
unrelated reason and never previously shown to matter) rather than to
report structure or vocabulary alone. That is one data point, on one
fixture, produced by one run per condition -- it demonstrates the
mechanism can produce a real behavioral difference, not that it reliably
will across other fixtures shaped like this one. Case-013's sibling-
routing-unavailable behavior is similarly one data point: it shows the
iteration's SKILL.md wording fix behaves as intended under actual
pressure (this was explicitly listed as untested in iteration 2), not
that it will hold up against a harder case built specifically to probe
edges of that fallback (e.g., a question genuinely too specialized to
reason through directly without the sibling's depth).

**What this does not prove:** each of these 5 cases was run once per
condition, by the same person who wrote the fixtures, the grading keys,
and the skill text being evaluated, with no independent second-reviewer
check of any grading judgment this iteration -- the same disclosed
limitation as iterations 1 and 2. Two of the five grading keys were
revised after seeing actual run output before being treated as final,
which narrows the space of the "same author checking their own claims"
concern but does not eliminate it. No case in this suite (this iteration
or prior ones) yet tests: a genuinely uncrossable Handoff with no
delegate reachable at all; a sibling-routing case hard enough that
reasoning through it directly (rather than deferring) is actually the
wrong call; live tool/script execution as opposed to static file reading
(though two with-skill and two baseline runs this iteration chose, on
their own initiative, to execute the fixture's own code locally to verify
a byte-length claim -- a genuine, unprompted use of "debug by
observation," not required by any prompt); or a real, messy production
codebase rather than a small synthetic fixture.

### Recommended next step

Per this iteration's own scope instruction: since these five cases did
not surface a further `SKILL.md` behavioral defect (only two grading-key
corrections, both fixture-side), synthetic-case iteration on this skill
should stop here rather than continue manufacturing cases against
predicted weaknesses with no verified failure behind them. The two
highest-value next steps, in order: (1) sanitized real field-debug
incidents (per the skill's own CASE SEED mechanism, never yet exercised
in this suite) would test claims this suite cannot -- whether the
skill's structure holds up on a codebase too large and messy for one
person to author both sides of; (2) selectively adapted external
benchmark cases (SRE/incident-response corpora, not general coding
benchmarks) would provide grading distance from the skill's own author,
addressing the single-author-bias caveat repeated across all three
iterations of this file.

## Iteration 5 (2026-09-25): re-validation of cases 009-013 after an editorial SKILL.md compression pass

Between iteration 3 and this iteration, `SKILL.md` went through a
prose-only compression pass (PR #60's own description has the full
diff/size accounting): merging the "Anti-patterns" list into "What this
skill refuses to do," folding Investigation behavior into The loop,
tightening the Delegate/Handoff distinction and sibling-composition
prose, and shortening the frontmatter description. No mode, schema field,
evidence-vocabulary term, or named invariant was intended to change. This
iteration re-runs the five hardest cases from iteration 3 (009-013, the
ones targeting enterprise/legacy/POC-to-production terrain, including the
two cases -- 010 and 013 -- where iteration 3 found a real with-skill vs.
baseline behavioral difference) against the *compressed* `SKILL.md`, to
check that compression didn't quietly drop the behaviors those two cases
depend on.

**Harness, this iteration:** fresh `general-purpose` subagents (one per
run, 10 runs total), each given its own isolated copy of the case
directory under a scratch path outside the repo -- with-skill copies also
received the current `skills/field-debug/SKILL.md`; baseline copies did
not. Each agent was instructed not to read or explore anything outside
its assigned directory and not to use web access. With-skill agents were
told to read `SKILL.md` and follow it exactly, including its output
formats; baseline agents got the case's own `context.md` and no imposed
report structure, matching iteration 3's convention. All 10 runs were
executed once per condition, no case re-run. Every run's full final
report was read and graded by hand directly against
`evals/field-debug/grading/case-0NN.expected.md`'s REQUIRED and BONUS
items (re-read in full for this grading pass, not from memory of
iteration 3's summary).

### Per-case results

| Case | With-skill | Baseline | Notable difference |
|---|---|---|---|
| 009 | 6/6 REQUIRED, BONUS not cleanly met | 6/6 REQUIRED, BONUS closer but still not a clean match to the exact wording | Both found the override via `ops/prod_startup.log` and `ops/overrides.properties`, both proposed the config fix (not a code rewrite), both correctly separated "what `main` does" from "what's running." Neither run's follow-up explicitly names the *override-file mechanism itself* (as opposed to this one flag) as a durability gap independent of this instance -- baseline's "force-retire `flat_percentage`... prevent this class of drift from recurring" comes closer to the BONUS's exact ask than with-skill's follow-up, which only proposed investigating the override's change history |
| 010 | 6/6 REQUIRED + full BONUS | **5/6 REQUIRED, BONUS not met** | Same failure axis as iteration 3, reproduced in softer form: baseline's report states Sam's check ran "almost certainly against the default/assumed environment (prod), not both" -- an unstated-in-fixture directional assumption about which queue manager was checked, hedged as an assumption rather than flatly asserted (unlike iteration 3's baseline run, which stated it as if confirmed), but still a real, if smaller, instance of the same overclaim-a-vantage-point item this case exists to catch. The with-skill run explicitly declined to name which queue manager Sam's check covered ("Unknowns: which queue manager Sam's 03:19 check covered") and explicitly tagged the historical `GL_MQ_ENV=prod` documentation claim ASSUMED rather than confirmed, satisfying every REQUIRED item and the BONUS |
| 011 | 6/6 REQUIRED + BONUS | 6/6 REQUIRED + BONUS | None -- both explained the 14-record parse bug, explicitly compared it against the 1,186 reported gap, found the warehouse-owned dedupe trigger unprompted, and both framed it explicitly as a 2015-era scale regression, not a new bug |
| 012 | 6/6 REQUIRED + BONUS not stated | 6/6 REQUIRED + BONUS met | Both independently executed `build_record` against the sample data to verify the byte-length overflow, found the unread `inbound/ack/` files, and rejected the passing ASCII-only test as proof of correctness -- tied on every REQUIRED item. The baseline run additionally named, unprompted, that "nothing in this pipeline appears to parse or alert on" the ack files (the exact BONUS ask); the with-skill run's follow-up only named the missing non-ASCII test fixture, not the alerting gap -- a case where baseline's finding was more complete than with-skill's |
| 013 | 6/6 REQUIRED (corrected key) + BONUS not met | 6/6 REQUIRED (corrected key) + BONUS not met | Both named the personal-credential blocker via `integration.py`'s own attribution comment, named >=2 concrete consequences, marked the pilot as dev-tenant-only evidence, and gave an actual "not production-ready" verdict without conflating the conclusive identity issue with the genuinely-unknown production-tenant specifics. Both BONUS misses are clean, anticipated ones: both stopped at "get a dedicated service account" rather than naming the ownership question itself (who owns it, who's on-call, how it's rotated) -- exactly the failure mode the BONUS text names. The with-skill run additionally, and explicitly by name, stated that `identity-authority-audit` was not installed in this session and reasoned through the authority question directly rather than deferring -- reproducing iteration 3's sibling-routing-fallback demonstration under the compressed `SKILL.md` |

**Numeric summary, this iteration's 5 cases:** with-skill 30/30 REQUIRED
items met (perfect, across all five cases); baseline 29/30 REQUIRED
(missing the same item, case-010's queue-manager-ambiguity item, that
iteration 3 flagged, though in a softer/hedged form this time). BONUS:
with-skill fully met on 2 of 5 (010, 011); baseline fully met on 3 of 5
(009 partially/arguably, 011, 012); both cleanly missed case-013's BONUS.

**A correction found while re-grading, disclosed above at its source:**
iteration 3's per-case table and numeric summary recorded case-012 as
"7/7 REQUIRED" in both conditions and totaled 31 REQUIRED items for its
five cases. `grading/case-012.expected.md` has always had exactly 6
REQUIRED items (confirmed via `grep -c` against the file's sole commit,
which iteration 3 itself made) -- this was a miscount in iteration 3's
write-up, not a re-graded case or a grading-key edit. Fixed at its source
in the "Per-case results" table and numeric summary above, not silently:
the corrected iteration-3 totals are 30/30 with-skill and 29/30 baseline.

### What this iteration's evidence shows, and does not show

The central question this iteration was run to answer -- did the
editorial compression pass on `SKILL.md` quietly drop any of the
behaviors that iteration 3 showed actually matter -- has a clear answer
for the two cases that matter most: no. Case-010's with-skill run
reproduced the exact discipline (explicit ASSUMED-tagging of a
documentation claim, explicit refusal to name an unstated vantage point)
that produced iteration 3's only clean with-skill/baseline REQUIRED-item
divergence in this suite, and case-013's with-skill run reproduced the
sibling-routing-unavailable fallback iteration 3 called "a live,
first-time demonstration" -- this iteration is the second such
demonstration, under materially shorter instruction text, which is
meaningfully stronger evidence that the mechanism survives paraphrase
than either demonstration alone would be.

Baseline reproduced its own iteration-3 pattern too, including the same
specific miss on case-010 -- weaker this time (a hedged "almost
certainly," not a flat assertion), which is consistent with ordinary run-
to-run variance in a single-sample baseline rather than evidence of
anything about `SKILL.md`. Case-012 is a new data point this iteration
did not have before: baseline's follow-up named the BONUS-level alerting
gap and with-skill's did not, the reverse of the usual pattern in this
suite where with-skill either ties or exceeds baseline. This is one run
each, on one fixture; it shows with-skill's structured-report discipline
doesn't guarantee a more complete follow-up list than an unstructured
baseline's, not that the skill degrades follow-up quality generally.

**What this does not prove:** this is still a single run per condition
per case, by the same person who wrote the fixtures, the grading keys,
the skill text, and the compression edit being validated -- the same
single-author-bias caveat as every iteration before this one. Grading
this iteration's 10 runs did surface one arithmetic error in iteration
3's own record (case-012's REQUIRED count), which is itself a small,
concrete argument for re-deriving totals from the committed grading keys
at write-up time rather than trusting a prior iteration's summary,
exactly as this repo's `AGENTS.md` already asks.

### SKILL.md corrections from this iteration

None. No run this iteration surfaced a `SKILL.md` behavioral defect --
every with-skill REQUIRED item was met across all five cases, and the two
mechanism-dependent behaviors from iteration 3 (case-010's
documentation-vs-runtime discipline, case-013's sibling-routing fallback)
both reproduced correctly under the compressed text. The compression pass
is not re-litigated here; this iteration's purpose was narrowly to check
it didn't regress with-skill behavior, and it didn't.

### Recommended next step

Unchanged from iteration 3: sanitized real field-debug incidents (via the
skill's own CASE SEED mechanism, still never exercised in this suite) or
selectively adapted external benchmark cases remain the highest-value next
steps, for the same reason iteration 3 gave -- this suite still cannot
address the single-author-bias caveat repeated across all five iterations
of this file now.

## Iteration 6 (2026-09-25): six new cases authored, frozen, not yet run

This iteration is eval-authoring only -- **no baseline or with-skill agent
was run against any of the six cases below, and no grading key was
adjusted based on model output.** `skills/field-debug/SKILL.md` was not
modified. The cases and their grading keys are frozen as committed; a
future session, with no involvement in their design, is expected to run
and grade them.

Prior iterations' cases pressure enterprise/legacy terrain, delegation,
checkpoint/resume, and productionization restraint, but none test
temporal/concurrent/distributed-state reasoning specifically, and none
test whether the skill over-investigates when the evidence is already
straightforward. Six new cases (`case-014` through `case-019`) target
that gap:

| Case | Scenario |
|---|---|
| 014 | A 50-unit limited drop ends up with 52 confirmed orders; the inventory table reads a clean `available = 0` with no errors anywhere. Root cause: a check-then-act read-modify-write with no lock/version guard lets two concurrent requests both read the last unit as available and both confirm. Includes a deterministic two-thread reproduction against the real reservation function (not a re-implementation), run and verified during authoring. |
| 015 | ~62% of payment attempts fail after a routine API-key rotation, looking random from the customer's side. Root cause: a rolling restart across 8 pods paused on an unrelated readiness-probe failure and never resumed, leaving 5 of 8 pods still running the old, now-revoked key -- fully deterministic per pod once grouped, not intermittent. |
| 016 | DB connection-pool utilization spikes to 100% for 10-15s on an exact ~300-second cadence after a cache-TTL config change. Root cause: the shared cache key's expiry is unguarded by any lock/single-flight, so the whole fleet misses and re-runs the same expensive query within the same second. |
| 017 | A customer is charged twice for one order despite payments-svc's own logs and order status showing nothing wrong. Root cause: the first capture attempt actually committed on the payment gateway's side before the caller's client-side timeout fired; the caller's retry, sent with no idempotency key, created a second, independent, equally real charge. Includes a small script that mechanically verifies the gateway's completion timestamp precedes the client timeout. |
| 018 | Straightforward control, no trap: a deploy accidentally changed a configured port from 443 to 8443; the target service is directly confirmed listening on 443. Tests whether the skill commits to the direct fix instead of inventing hidden causes. |
| 019 | Straightforward control, no trap: a producer renamed a required event field; the consumer's own schema and rejection log directly confirm the mismatch, and the producer's "no consumer changes needed" claim is directly contradicted by that evidence. Tests the same stop-when-settled discipline from the opposite direction. |

Each case was authored with an explicit design constraint: the prompt
never names the mechanism (no "race condition," "stale cache," "timed
out but may have succeeded," or "the obvious answer is correct" in any
agent-visible file), and the two control cases carry an explicit
anti-overfitting grading item requiring that unnecessary continued
hypothesis generation, delegation, or terrain exploration be treated as
a failure of investigation discipline once the evidence already
discriminates conclusively. Every REQUIRED grading item was checked
against actually-discoverable fixture content (not fixture prose that
merely asserts a conclusion), and every case with a runtime-checkable
mechanism (`case-014`, `case-017`, and the schema validation in
`case-019`) has a script or test that was actually executed during
authoring to confirm the hidden ground truth reproduces deterministically
-- see each `grading/case-0NN.expected.md` for the specific run output
that verification is based on.

**What this adds, and does not add:** this is fixture and grading-key
authoring evidence -- it demonstrates the scenarios are internally
consistent, reproducible, and isolated from their own grading material
(`bash scripts/check.sh` passes). It says nothing yet about whether
`SKILL.md`, with or without the compression from iterations 4-5, actually
performs better than an unassisted baseline on any of these six cases --
that comparison has not been run and no claim about it is made here.

## Iteration 7 (2026-09-25): blind runs and grading of cases 014-019

This iteration runs and grades the six cases iteration 6 authored but
deliberately left unrun, per PR #61's own instruction: "a completely fresh
session, with no involvement in their design," should run and grade them.
This session had already read PR #61's description and this file's
iteration-6 section (both name each case's intended mechanism) before
running anything, so it could not itself be that fresh, uninvolved
reader -- the isolation this iteration actually relies on is that every
*tested* agent was a brand-new `general-purpose` subagent with no
conversation history, given only an isolated copy of one case's fixture
directory (plus `skills/field-debug/SKILL.md` for with-skill runs) and
never the orchestrating session's context, this file, or the PR
description. No `fork` subagent (which would have inherited that
context) was used anywhere in this iteration. Grading keys
(`grading/case-0[14-19].expected.md`) were not read until all 12 tested-
agent outputs already existed as committed files, and no case fixture,
grading key, `pressure_evals.json`, or `SKILL.md` was modified before or
during grading.

**Run protocol.** Each case's fixture directory was copied twice (once
for baseline, once for with-skill) into an isolated scratch path outside
the repo; with-skill copies additionally received a copy of
`skills/field-debug/SKILL.md` under `.skill/`. Twelve fresh
`general-purpose` subagents (one per case per condition, default model
settings) were launched across three waves of size 5/5/2 to respect this
session's subagent concurrency limit, with cases mixed within a wave
(e.g. wave 1 ran case-014's both conditions alongside case-015's and one
of case-016's) so that no case's result could influence another case's
tested agent -- each subagent has no visibility into any other
subagent's run. Every subagent was instructed to work only inside its
assigned directory, read `context.md` as the task framing (the same
framing this suite's iterations 1-5 used), investigate using whatever
else was in the directory (executing scripts/tests where present), and
write a complete final report to `RUN_OUTPUT.md` inside that directory;
with-skill subagents were additionally told to read `.skill/SKILL.md`
first and follow its report structure exactly. No subagent was told this
was an evaluation, shown any grading material, or given any prior run's
output. All 12 `RUN_OUTPUT.md` files were confirmed to exist before any
grading key was opened.

### Per-case results

| Case | Baseline REQUIRED | With-skill REQUIRED | BONUS | Substantive difference | Attributable to a specific skill instruction? |
|---|---|---|---|---|---|
| 014 (lost-update race) | 6/6 | 6/6 | Both met | None of substance -- both independently ran `reproduce_concurrent_reservation.py` and `tests/test_checkout_service.py`, both used the `t0514`/`t0515` audit rows to pin the exact interleaving, both explained why `available` reads `0` not `-2`, both proposed an atomic-guarded-decrement-class fix. With-skill's report used the skill's OBSERVED/INFERRED/ASSUMED vocabulary and section headings; baseline's was organized prose covering the same ground. | No -- a tie, structure/vocabulary only |
| 015 (stalled rollout, stale API key) | 7/7 | 7/7 | With-skill met both immediate mitigation and a durability follow-up (alerting on a stuck rollout); baseline's remediation section named only the immediate resume-the-rollout fix, with no durability/prevention recommendation anywhere in the report | With-skill win, but narrow: identical root-cause chain, identical per-pod evidence use; the only difference is one extra recommended line item | Plausibly the skill's "Follow-up" field, which iteration 2's `case-008` finding also traced a similar completeness difference to |
| 016 (cache-stampede, TTL change) | 6/6 | 6/6 | **Baseline met, with-skill did not (see below)** | Baseline explicitly stated the BONUS's exact claim ("at the old 3600s TTL, the stampede -- if it occurred at all -- would have been an hourly, easy-to-miss blip"). With-skill's closest treatment of the same question is a hedge in its own "Remaining uncertainty" field: "Whether this exact stampede was already occurring at the prior 3600s TTL cadence is ASSUMED/INFERRED... versus some other condition making the pre-change behavior actually benign" -- i.e. it treated whether the old TTL had the same defect as genuinely unresolved rather than committing to "yes, just less often," which is what the BONUS asks for. Both reports otherwise reach an identical root cause and identical anti-scaling argument. This is a real, if narrow, baseline win. | This is a close call -- flagged as such rather than adjudicated silently; see full quotes above. It does not look attributable to any specific skill instruction (nothing in `SKILL.md` tells a run to hedge this particular claim); it reads as ordinary run-to-run variance in how confidently two independent runs treat the same under-evidenced counterfactual |
| 017 (ambiguous timeout + non-idempotent retry) | 6/6 | 6/6 | With-skill met (named a concrete `Idempotency-Key` remedy); baseline explicitly declined to recommend one, writing "it does not evaluate or recommend a specific fix... as that was outside the scope of the question asked" | With-skill win: baseline reached the identical root-cause chain (same `verify_timing.py` execution, same 33ms finding, same idempotency-gap identification) but its own reading of the task's scope ("look into it," not "fix it") led it to withhold a fix recommendation; the skill's report structure has no such opt-out (a Follow-up/Intervention field is always populated) | Plausibly attributable to the skill's mandatory Follow-up/Intervention fields forcing a recommendation baseline chose to withhold as out of scope |
| 018 (control: port config) | **5/6** (missed the "states what would verify the fix" item) | 6/6 | With-skill met (explicit "no experiment... would have been ceremony, not rigor" line); baseline did not include an equivalent statement anywhere | **This is the one REQUIRED-item difference in this iteration.** Baseline's report has no "Recommended fix"-adjacent sentence describing what confirms the fix worked (e.g. fulfillment requests reaching `inventory-svc`, or the connection-refused errors stopping); with-skill's mandatory "Verification" field states exactly that. Both reports otherwise reached the identical root cause via the identical diff/log comparison, and both correctly avoided speculative causes (firewall/DNS/auth/cache) and avoided calling for further investigation, delegation, or a handoff | Yes -- directly traceable to `SKILL.md`'s mandatory Verification field, which has no baseline equivalent when no report structure is imposed |
| 019 (control: producer field rename) | 6/6 | 6/6 | Neither met | Both reached an identical, complete diagnosis (schema vs. payload comparison, executed `tests/test_consumer_validation.py`, explicitly rejected the producer's "no consumer changes needed" claim, proposed the same minimal schema fix). With-skill's report explicitly declined to add the CI-contract-testing durability note "per the skill's own standard rather than speculated," citing no evidenced owner -- baseline simply didn't raise it. Both land on the same BONUS-miss, for different reasons | No -- a tie on substance, and the with-skill run's explicit self-restraint here argues against the skill inducing padding, not for it |

A note on a borderline grading judgment made identically to both
conditions, not a with-skill-vs-baseline difference: case-018's
anti-overfitting REQUIRED item asks that no hypothesis be entertained
"beyond the one the config/log comparison already settles." Both the
baseline and with-skill reports include, in a clearly separate
"remaining uncertainty" field, an honest note that they cannot fully
rule out `inventory-svc` itself having an unfinished, intended migration
to port 8443 -- the identical residual doubt, in both conditions, never
promoted into the main conclusion or the recommended fix, and never used
to justify further investigation, a Delegate, or a Handoff. This was
graded as satisfying the anti-overfitting item in both cases (disclosed
epistemic honesty in a clearly-scoped uncertainty field, not a live,
unresolved hypothesis blocking commitment) -- but it is a judgment call,
recorded as such rather than silently resolved, and since both conditions
did the identical thing it does not change this iteration's baseline-
vs-with-skill comparison either way.

### Numeric summary (re-derived from the table above, not from memory)

- REQUIRED items across the six cases' grading keys: 6+7+6+6+6+6 = 37
  per condition. **Baseline: 36/37** (the one miss is case-018's
  verification-statement item). **With-skill: 37/37.**
- BONUS items (one per case, six total): **baseline 2/6** (014, 016);
  **with-skill 4/6** (014, 015, 017, 018), with case-016's baseline-vs-
  with-skill BONUS outcome flagged above as a close call rather than a
  clean win.
- No case was re-run. No grading key was edited as a result of any run's
  output this iteration (contrast iterations 1, 3, and 5, which each
  revised a key after seeing a run) -- every key was used exactly as
  committed in PR #61.

### Answering the six questions this iteration was run to address

1. **Does field-debug help on actual concurrency/interleaving reasoning
   (case-014)?** No measurable difference. Both conditions independently
   executed the real reservation function under forced interleaving,
   independently found the same two colliding audit rows, and reached
   the identical mechanism. This iteration adds no evidence that the
   skill improves concurrency reasoning specifically -- both a skilled
   baseline and the skill handled it equally well.
2. **Does it correctly reason about partial failures caused by
   instance-local stale state (case-015)?** Yes, but so did baseline.
   Both correctly grouped failures by pod, cross-referenced the rollout
   log, and named the process-start key-read mechanism. The only
   difference was a completeness gap in baseline's remediation
   (mitigation only, no durability follow-up) -- a real but narrow
   difference, not a difference in the core reasoning.
3. **Does it recognize cache-coordination failures rather than merely
   blaming the overloaded dependency (case-016)?** Yes, cleanly, but
   again baseline recognized it identically well, and on this case's one
   BONUS nuance (would the same defect exist under the old TTL, just
   less often) baseline was arguably the more decisive, more clearly
   evidence-grounded of the two -- see the flagged close call above. This
   is the one place in this iteration where a baseline run's stated
   position was arguably better-supported than the with-skill run's.
4. **Does it distinguish a timeout from evidence that an operation
   failed (case-017)?** Yes, and so did baseline -- both explicitly used
   `verify_timing.py`'s executed output to establish that the first
   capture committed before the client timeout fired, and both correctly
   refused to treat "the caller timed out" as "the operation failed."
   The only difference was baseline's explicit, scope-based refusal to
   recommend a fix versus with-skill's mandatory Follow-up field
   producing one.
5. **On straightforward cases, does the skill stop when the evidence is
   sufficient, or does it over-investigate (cases 018/019)?** It stopped.
   Neither with-skill run generated extra hypotheses, delegated, requested
   a handoff, or explored beyond the four-to-eight files given, and both
   explicitly narrated the stopping decision ("no experiment was run
   beyond reading the four provided files... this evidence already
   discriminates conclusively... per the skill's standard against
   manufacturing ceremony"). Baseline stopped equally appropriately in
   both cases, just without narrating why. This iteration finds no
   over-investigation in either condition on either control case.
6. **Are any differences merely formatting/evidence-label differences
   rather than substantive investigation improvements?** Mostly, yes.
   Four of six cases (014, 016, 017 core reasoning, 019) tied on
   substance, with with-skill's OBSERVED/INFERRED/ASSUMED vocabulary and
   named section headings the only visible difference -- consistent with
   every prior iteration of this suite. Two cases (015's durability
   follow-up, 018's verification statement) show a real, if narrow,
   behavioral completeness difference traceable to specific mandatory
   fields in the skill's report structure (Follow-up, Verification), not
   to different reasoning.
7. **Did baseline outperform with-skill anywhere?** Yes, once, on
   case-016's BONUS item -- recorded above with equal prominence to the
   with-skill wins, not downplayed. It is a narrow difference (a BONUS
   item, not a REQUIRED one, and a genuinely close call on the exact
   wording), but it is real: baseline's report committed to the specific
   claim the BONUS asks for, and with-skill's did not.

### What this iteration's evidence supports, and does not

**Supports:** on these six cases, field-debug's with-skill condition
matched or exceeded a capable, unstructured baseline on every REQUIRED
item (37/37 vs. 36/37), with the one baseline miss and two of the four
with-skill BONUS wins traceable to specific mandatory fields in the
skill's report structure (Verification, Follow-up) rather than to
different underlying investigative reasoning -- the same pattern this
suite's every prior iteration has found. Both conditions correctly
handled a genuine concurrency race, a distributed partial-failure
pattern, a cache-coordination failure, and a timeout-vs-failure
ambiguity, and neither over-investigated either control case.

**Does not support:** a claim that field-debug improves the underlying
reasoning quality on concurrency, distributed-state, or timeout-
ambiguity problems specifically -- on every one of those axes, this
iteration's baseline reached the identical substantive conclusion by the
identical evidence path. It also does not support a claim that with-skill
is uniformly better even on completeness: case-016's BONUS is a
documented counterexample, deliberately not smoothed over. Each case was
run once per condition, by a session that (unlike the fixture author) had
not designed these cases but had read both PR #61's description and this
file's iteration-6 section before running anything -- the tested agents
themselves never saw that material, but the grading judgment calls above
(particularly case-016's and case-018's close calls) were made by the
same session that ran the evaluation, with no independent second
reviewer, the same disclosed limitation as every prior iteration of this
file.

### Fixture and grading-key findings

None that required a repair. One interpretive note is recorded above
(case-018's anti-overfitting item, read as compatible with a clearly-
scoped, non-blocking uncertainty disclosure) because both conditions
triggered it identically and it was a real judgment call worth
disclosing, not because either fixture or grading key needs to change.

### SKILL.md corrections

None. No with-skill run this iteration missed a REQUIRED item, entertained
a speculative cause on either control case, over-investigated, or produced
a report contradicting its own evidence. The one place a with-skill run
looked weaker than baseline (case-016's BONUS) is a narrow, arguably
defensible epistemic-caution choice on a single under-evidenced
counterfactual, not a reproducible defect traceable to specific
`SKILL.md` text -- per this repo's own instruction to distinguish an
observed defect from a suspected one, and to only correct `SKILL.md` on
the former, no change is made.

### Recommendation

**Leave `skills/field-debug/SKILL.md` frozen.** With-skill matched
baseline on every case this iteration graded and struck REQUIRED-item
parity or better everywhere (37/37 vs. 36/37), with the sole with-skill-
favoring REQUIRED difference traceable to the skill's own mandatory
report structure rather than to superior reasoning, and the one baseline-
favoring result confined to a single BONUS item on a genuinely
close-call claim. Neither outcome rises to "a concrete behavioral failure
traceable to the current instructions," which is this repo's own bar for
changing the skill text. This is one run per condition per case,
graded by the same session that ran it with no independent second
reviewer -- consistent with, and no stronger than, every prior
iteration's disclosed limitation.

## Iteration 8 (2026-09-25): four staged, multi-phase cases authored and frozen, not yet run

This iteration is eval-authoring only -- **no baseline or with-skill agent
was run against any of the four cases below, no model-assisted grading
was performed, and no grading key was adjusted based on model output.**
`skills/field-debug/SKILL.md` was not modified. The cases and their
grading keys are frozen as committed; a future session, with no
involvement in their design, is expected to run and grade them, exactly
as PR #61/#62's iteration-6-to-7 handoff did for `case-014` through
`case-019`.

Iterations 1-7 pressure-test terrain-mapping, delegation, checkpoint/
resume against a single continuous incident, scoped single-witness
testimony, and temporal/concurrent/distributed-state reasoning within one
investigation session -- but none test what happens *across* a session
boundary when the world keeps moving without the investigator, what a
*good* checkpoint handoff looks like when nothing needs to change, what
happens when the people who hold the evidence are split across vantage
points and one of them leaves mid-investigation, or a genuinely
multi-stage incident where fixing one real problem reveals a second, and
then a third, real problem. Four new cases (`case-020` through `case-023`)
target that gap.

### External design sources (mechanics donors, not scenario material)

Per the task that requested this expansion, four external systems were
used as sources of *mechanics* to borrow, not scenarios or datasets to
copy or add as dependencies. No URL was fetched this session; each is
cited by the title/description given in the task, and the specific idea
borrowed into a case is named so the citation is checkable against that
case rather than taken on faith:

- **SentinelBench** (Microsoft Research, described as a benchmark for
  long-running monitoring agents): the mechanic borrowed is "the
  environment changes independently of agent actions, and a resumed
  agent must revalidate perishable facts rather than replay everything or
  trust everything" -- this is `case-020`'s and `case-021`'s central
  mechanic (a canary rollout that auto-promotes on its own timer,
  independent of any agent's request to pause it).
- **AWS DevOps Agent** (autonomous incident response): the mechanic
  borrowed is "prior context persists but must be reconciled with new
  information delivered between reasoning steps, and investigation
  resumes rather than restarts" -- shaped `case-020`/`case-021`'s
  checkpoint-then-resume structure (the checkpoint is handed forward, the
  original investigator's raw process is not).
- **Gemini Cloud Assist investigations** (Google Cloud): the mechanic
  borrowed is "explicit Observations/Hypotheses/Findings that stay
  inspectable across a revision, rather than being silently overwritten
  when new evidence arrives" -- this is why both `case-020`'s and
  `case-023`'s grading keys explicitly require *not* discarding or
  retroactively rewriting an earlier, still-valid finding just because a
  later one arrived.
- **Google SRE incident management / handoff**: the mechanic borrowed is
  "a living incident-state document lets an incoming responder continue
  from current state instead of reconstructing the incident from
  scratch" -- this is the core design constraint behind `case-020` and
  `case-021`'s checkpoint files, and behind `case-022`'s replacement-
  responder (Chris covering for Dana) receiving pointers to existing
  evidence rather than starting cold.
- **Cloud-OpsBench**: the mechanic borrowed is "process-level evaluation:
  a correct final answer without the supporting evidence chain is not
  equivalent to a good investigation" -- this is why every new case's
  grading key includes REQUIRED items about *how* the conclusion was
  reached (actually running the reproduction at each stage, citing which
  vantage point said what and how it was checked), not just what the
  final conclusion says.

None of these four systems' code, datasets, or benchmark harnesses were
added as a dependency; nothing here imports or reuses their material
beyond the mechanics named above.

### The four cases

| Case | Mechanic under test | Scenario |
|---|---|---|
| `case-020` | Changed-world resume | A colleague's checkpoint on an `orders-svc` -> `partner-erp-gateway` incident correctly implicates a v3.15 retry-logic change while a canary hold request is still pending. Between the checkpoint and resume, the canary auto-promotes to 100% on its own default policy -- independently of the investigation -- and the fleet-wide failure rate rises from a diluted ~9% to 34%. The resumed investigation must revalidate the now-stale canary/failure-rate snapshot, recognize the world changed rather than concluding the prior model was wrong, and still do real further work (connecting the retry code to the partner's documented rate-limit/burst behavior) to reach the actual root cause. |
| `case-021` | Unchanged-world resume (control) | A structurally identical checkpoint/resume handoff on an unrelated nightly customer-export job, but nothing material changes between the checkpoint and resume -- same code, same library version, same affected accounts, essentially the same drop rate one more night running. The one open question the checkpoint already scoped (a `recordsdb-client` keyset-cursor caveat) is answered by new documentation. This case exists to catch the opposite failure from `case-020`: needless replay, re-litigating already-ruled-out hypotheses, or general distrust of a checkpoint that was actually sound. |
| `case-022` | Changing people / scoped witnesses | Three vantage points on a customer-CRM sync complaint -- Northwind's Ops admin (webhook-receipt dashboard), our own platform SRE (send-side job log), and Northwind's CRM admin (the only one who can see CRM-side ingestion) -- each report a true observation from their own layer, two of which superficially conflict ("Delivered" vs. "nothing new has shown up") without either being wrong. The Ops admin goes unavailable (a scheduled system migration) partway through, handing off to a less-experienced replacement responder, forcing the investigation to delegate one bounded, concretely-targeted request rather than either stalling or asking everyone everything. |
| `case-023` | Sequential genuine failures | The hardest case in the suite. A vendor integration fails three real, sequential, unrelated-cause boundaries in order: an auth-scheme cutover (401), then, once fixed, a payload-contract mismatch the vendor's own migration notice said wouldn't happen (422), then, once that's fixed too, an unbounded-concurrency burst tripping the vendor's documented rate limit (429 on 5/25 orders). All three are real; none is a red herring; a benign, unrelated `DeprecationWarning` fires identically at every stage as an anti-overcorrection trap. Fully mechanized: `run_sync.py`/`pytest` against real, runnable code reproduces each stage deterministically as the agent applies each real fix. |

### Staging approach: no invented orchestration where the existing conventions already cover it

Deliberately, none of these four cases add new orchestration
infrastructure. Each reuses whichever existing convention in this suite
already fits its mechanic, rather than building something new:

- **`case-020`/`case-021`** follow `case-008`'s existing checkpoint-handoff
  convention exactly: Phase 1 is an authored, frozen checkpoint (nothing
  a live agent produced this session, consistent with this iteration
  running no agents at all), and the tested agent only ever sees Phase 2
  -- the checkpoint plus "current state" files gathered fresh for the
  handoff. There is no phase-1 raw transcript file in either case
  directory (mechanically checked -- see below).
- **`case-022`** follows `case-004`'s existing scripted-live-interaction
  convention exactly: the grading key holds Chris's, Dana's, and Priya's
  scripted responses, to be played by whichever future session actually
  runs this case, keyed on whether the tested agent's question is
  well-targeted -- the same mechanism iteration 1 already established and
  iterations 3-7 never needed to change.
- **`case-023`** needed no live orchestration at all: the three sequential
  failures are produced by actually running real, deterministic Python
  against a local sandbox harness that mirrors the vendor's documented
  contract (auth check, then schema validation, then a concurrency cap),
  in that order, so a stage's failure is only ever observable by fixing
  the stage before it and re-running. This was verified to reproduce
  deterministically five times in a row during authoring before being
  frozen (see below) -- not asserted from the code alone.

The task's suggested "sealed harness returning phase-appropriate tool
output" was considered and deliberately not built as new infrastructure:
`case-023`'s real code already provides that property for free (a stage's
error text does not exist anywhere until the code that produces it is
actually executed), and `case-020`/`case-021`/`case-022` are each
adequately served by an existing, already-battle-tested convention in
this suite. Match the size of the mechanism to the size of the case.

### Fixture/harness validation actually run this session

Two standalone verification scripts were written under
`evals/field-debug/scripts/` (deliberately outside `cases/`, so they are
never copied into a tested agent's sandbox under this suite's own run
protocol, and so they can safely reference grading-relevant specifics
without being an isolation violation):

- **`verify_case_023_progression.py`** -- copies `case-023`'s real code to
  a scratch directory and mechanically applies exactly the three fixes a
  correct investigation would apply, one at a time, re-running the real
  `run_sync.py` after each. Confirmed, this session: unmodified code
  produces 25/25 `401` and no `422`/`429` anywhere in the output; the auth
  fix alone produces 25/25 `422` and no `401`/`429`; the auth+schema fix
  produces exactly 20/25 accepted and 5/25 `429` (also independently
  re-run five additional times outside this script during authoring, with
  an identical 20/5 split every time -- the concurrency window is
  deterministic, not flaky); all three fixes together produce 25/25
  accepted. The same script also greps `case-023`'s static agent-visible
  files (`context.md`, `partner_migration_notice.md`,
  `sync_log_so_far.md`) and confirms none mentions the stage-2 or stage-3
  failure signatures ahead of time.
- **`verify_checkpoint_resume_isolation.py`** -- confirms, for both
  `case-020` and `case-021`, that (a) the case directory contains no file
  shaped like a raw prior-investigator transcript (only the distilled
  checkpoint plus current-state files), and (b) `checkpoint.md` -- the
  only Phase-1-authored artifact in either case -- contains none of that
  case's Phase-2-only facts (the specific rollout percentages/failure
  rates only gathered fresh for `case-020`'s handoff, and the specific
  drop percentage only gathered fresh for `case-021`'s).

Both scripts were run this session and both passed
(`verify_case_023_progression: PASS`,
`verify_checkpoint_resume_isolation: PASS`). `bash scripts/check.sh` also
passes against the full tree, including the four new cases, their
`grading/*.expected.md` files, and their `pressure_evals.json` entries
(206 case directories total, no leakage flagged).

**What is mechanically verified vs. represented as a frozen scripted
interaction, stated plainly:** `case-023`'s three-stage sequence is fully
mechanically verified -- it is real, executable code, not a narrated
outcome. `case-020`/`case-021`'s checkpoint/current-state split and
`case-022`'s three-vantage-point testimony are internally consistent,
isolation-checked, static fixtures -- not executable, and not run against
a live agent this session. `case-022`'s Chris/Dana/Priya interaction is,
like `case-004`'s Priya before it, a **scripted role to be played live by
whichever future session actually runs this case** -- its correctness as
written is a matter of narrative/grading-key consistency (checked by
hand, adversarially re-read for leakage and chronology this session), not
something a script can execute and assert on.

### What this adds, and does not add

This is fixture and grading-key authoring evidence: it demonstrates the
four scenarios are internally consistent, isolated from their own grading
material, and (for `case-023`) reproducible. It says nothing about
whether `SKILL.md` performs better than an unassisted baseline on any of
these four cases -- that comparison has not been run and no claim about
it is made here. It also does not itself demonstrate that `case-022`'s
scripted human responses will be played correctly or consistently by
whatever session eventually runs it live -- that session should re-read
`grading/case-022.expected.md`'s scripted-response section before playing
any of the three roles.

### Limitations the future blind-run session should know

- `case-022` requires a human-role-playing orchestrator exactly as
  `case-004` did -- budget for that when planning the run wave, and route
  its Chris/Dana/Priya turns through the grading key's scripted responses
  rather than improvising.
- `case-023`'s red-herring `DeprecationWarning` fires on every call and
  will appear in `pytest`'s captured-warnings output by default; this is
  intentional (see the grading key's anti-overcorrection item) and is not
  a fixture defect to "clean up" before running.
- `case-020` and `case-021` intentionally share a mechanic (checkpoint/
  resume) but not a scenario, domain, or checkpoint author -- they are a
  matched pair for the changed-world/unchanged-world contrast, not the
  same incident at two points in time.
- As with iteration 6, every REQUIRED grading item was checked against
  actually-discoverable fixture content, not fixture prose that merely
  asserts a conclusion -- but this session authored the cases and cannot
  itself be the "fresh, uninvolved reader" iteration 7 called for; that
  property still depends on the next session being a genuinely fresh one,
  as instructed.

