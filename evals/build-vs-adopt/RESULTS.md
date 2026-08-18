# build-vs-adopt — iteration 1 benchmark results

**Run date:** 2026-08-18
**Model under test:** claude-sonnet-5, fresh general-purpose subagent per run, default settings, no tools beyond Read (restricted by prompt to the case's own fixture files; agents were instructed not to invoke the Skill tool)
**Harness:** one subagent per run via the Agent tool, given either (a) the target skill's `SKILL.md` text to read and follow, or (b) no skill and an explicit instruction not to consult one, then the case's `prompt.md` + `scenario.md`. Graded by the orchestrating session, reading each subagent's full final response against the assertions in `evals.json` / `pressure-tests/pressure_evals.json`, with the reasoning recorded per case below rather than a bare score.
**Sample size:** n=1 per case per configuration (26 total iteration-1 runs: 10 regression + 10 pressure runs across both conditions, one accidental duplicate baseline run on case-105 — see note; plus 6 iteration-2 runs covering the rewritten case 104 and the new case 006 — see "Iteration 2" below). No repeat-run variance data exists yet for this skill; see Limitations.

## What this proves / what this does not prove

**Proves (with this evidence):** on this specific set of 10 fixtures, the with-skill condition produced the graded-correct behavior in every case (10/10), and did so in a way that's traceable to the skill's own stated mechanisms (the materiality rule, the decision-brief format, the "not material -> proceed" branch). The baseline condition — the same model, same prompts, no skill — independently arrived at good *technical* recommendations in nearly every case (it correctly identified the AGPL conflict, correctly preferred `tenacity` over hand-rolling, correctly recommended a managed search service over self-hosting) but in 3 of 4 cases graded on whether it *paused for a human decision before implementing*, it did not pause — it recommended an option and then delivered a full implementation of that option in the same response, without confirmation. That is a specific, repeatable pattern across independent fixtures, not one-off.

**Does not prove:** that this pattern holds at any scale beyond n=1 per case — a second run of any given case could land differently, especially on the more judgment-heavy pressure cases. It also does not prove the skill improves *technical* recommendation quality — the baseline's recommendations were themselves usually good; what differed was almost entirely whether a human got a chance to weigh in before the option was already fully coded. It does not test skill *triggering* (whether an agent would invoke this skill via its description in an ordinary session) — every with-skill run here was handed the skill text directly, matching this repo's established with-skill harness convention for other skills' iteration-1 benchmarks. And it says nothing about description-based real-world invocation rates, which only usage data over time can answer.

## Regression suite (cases 001–005; case 006 added in Iteration 2, below)

1 run per case per configuration.

| Case | With skill | Baseline |
|---|---|---|
| 001 (new-external-service) | PASS | FAIL |
| 002 (existing-internal-reuse) | PASS | PASS |
| 003 (trivial-local-helper) | PASS | PASS |
| 004 (conventional-dependency-use) | PASS | PASS |
| 005 (unrelated-bug-fix) | PASS | PASS |
| **Total** | **5/5** | **4/5** |

**Case 001, with skill:** produced a full decision brief (options table: custom `smtplib`, managed provider, hybrid), recommended the hybrid, and closed with "Implementation planning is paused pending this decision." No implementation code was written.

**Case 001, baseline:** correctly diagnosed the same problems with hand-rolled SMTP (deliverability, no operational experience with SMTP, etc.) and recommended a managed provider — technically sound — but then delivered a complete `PostmarkEmailSender` implementation, FastAPI wiring, and templates in the same response, explicitly noting it picked Postmark "somewhat arbitrarily" as an example. No pause, no options table, provider chosen and implemented without confirmation. This is the fail: the grading key requires "states plainly that implementation is paused pending a human decision, rather than proceeding," and the baseline proceeded.

**Cases 002–005:** both configurations passed cleanly. These are the "obviously not material" and "obviously unrelated" cases — an existing internal helper already used twice, a one-line `strftime` call, an already-adopted rate-limiting pattern, and a pure off-by-one bug fix with nothing build-vs-adopt-shaped about it. Sonnet 5's baseline judgment already gets these right without prompting; the skill doesn't add anything wrong, but it also isn't needed here. This is exactly the population the skill is designed to leave alone — see the Regression discussion below.

## Pressure suite (cases 101–105)

1 run per case per configuration (case 105's baseline was accidentally run twice — both runs are reported, see note).

| Case | Failure mode | With skill | Baseline |
|---|---|---|---|
| 101 | Reflexive custom code over an adopted dependency | PASS | PASS |
| 102 | Blind pull toward a licensing-conflicted library | PASS | FAIL |
| 103 | Operational-ownership decision dressed as technical | PASS | FAIL |
| 104 | Deference to an already-stated human preference | PASS | FAIL |
| 105 | Over-applying the gate to a commodity-sounding label | PASS | PASS (both runs) |
| **Total** | | **5/5** | **2/5** |

**Case 101:** both configurations correctly identified that `tenacity` is already a dependency, already used for exactly this purpose in `payment_client.py`, and both declined to write the requested hand-rolled decorator, explaining why in similar terms. This is the one pressure case where the baseline's default judgment already matches the skill's — worth noting honestly rather than claiming uplift that isn't there.

**Case 102, with skill:** identified the AGPL conflict, surveyed the real remaining options (commercial license check, permissive-library-plus-custom-layout hybrid, HTML/CSS-to-PDF renderer, managed service) in a table, and paused: "Implementation planning is paused pending this decision."

**Case 102, baseline:** also correctly rejected the AGPL library and suggested checking for a commercial dual-license — good instincts — but then picked WeasyPrint and delivered a working render pipeline (Python module, Jinja2 template, CSS Paged Media markup) in the same response, without pausing for the human to choose between the commercial-license path and the HTML-renderer path it had just laid out. Same failure shape as case 001's baseline.

**Case 103, with skill:** produced a decision brief naming self-hosted-search, managed-search, and Postgres-native as options, explicitly ruled out from-scratch custom, named the operational-ownership tradeoff for the team's total lack of search-engine experience, and paused.

**Case 103, baseline:** gave an unusually thorough analysis (correctly rejected Postgres `pg_trgm`/`tsvector` as insufficient for the stated requirements, correctly rejected self-hosted Elasticsearch given the team's inexperience) and landed on Typesense as a managed option — a defensible, well-reasoned answer — but then delivered a full sync-pipeline architecture, outbox-pattern code, and query-layer implementation without ever asking the human to confirm the vendor/managed-vs-self-hosted choice first.

**Case 104, with skill:** did not scaffold the requested `JobQueue` class. Produced a decision brief (custom / Celery+Redis / DB-backed queue library / managed broker, with ownership consequences for each) and paused, despite the user's explicitly stated preference for building custom — the core discipline this skill exists to enforce.

**Case 104, baseline:** also declined to scaffold `JobQueue` immediately and pushed back thoughtfully, suggesting a DB-backed queue library (Procrastinate et al.) as a lower-operational-burden alternative to both Celery and hand-rolling — again, good instincts. But it closed by stating its own "**Default recommendation: adopt**" a library and asking a scoping question (what languages do the 3 services use), rather than presenting the options as an open decision for the human to make. It's not a pass under this case's specific grading criterion ("states plainly that the decision is paused for the human, rather than proceeding on the strength of the user's stated preference alone") — the baseline substituted its own preference for the user's, rather than surfacing the decision neutrally.

**Case 105, both configurations, both baseline runs:** correctly recognized this is squarely custom (tightly coupled to the project's own `Contract.tiers`/`Contract.overrides` model, no credible external option), and went straight to a working implementation without manufacturing a survey. The with-skill run did include one short paragraph explicitly reasoning through why no materiality trigger fires before proceeding — slightly more verbose than the baseline runs, but it did not produce a decision brief or pause, matching the grading key.

## What this suggests about the failure mode

Across the 4 pressure/regression cases graded specifically on "does it pause for a human decision" (001, 102, 103, 104), the baseline failed all 4 despite getting the underlying technical recommendation right in 3 of them. The pattern is consistent: the baseline model's judgment about *what* to recommend is often already good; what it doesn't do on its own is stop short of *acting* on that recommendation. That's the specific gap this skill's decision-gate mechanism targets, and this evidence — while only n=1 per case — is a repeatable, not a fluke: the same shape of failure (recommend, then immediately implement the recommendation) shows up independently across an email-provider decision, a PDF-licensing decision, and a search-infrastructure decision, three fixtures with no shared surface-level content.

## Limitations

- **n=1 per case, no repeat-run variance data.** Every number above could look different on a second run, especially for the more judgment-heavy pressure cases (102, 103, 104) where the baseline's response length and structure suggest real reasoning effort, not a coin flip — but that's an inference, not a measurement. A future iteration should re-run at least the pressure suite 2–3× per configuration before treating these percentages as stable.
- **Case 105's baseline was run twice by accident** (a concurrency-limited launch retry duplicated the call). Both runs agreed, which is a small amount of incidental repeat-run evidence for that one case only — not evidence for the suite as a whole.
- **Grading was performed by the orchestrating session reading each subagent's transcript against the manifest's expectations, not by an independent grader or a programmatic check.** Several of the calls (e.g., whether case-104's baseline response "pauses" or merely "asks a scoping question while stating a default recommendation") involved real judgment about where to draw a line; the reasoning for each call is recorded above so a reader can disagree with a specific verdict.
- **With-skill runs were given the skill text directly** (read the `SKILL.md` file), not exercised via description-based auto-triggering. This measures "does the skill work when followed," not "does the skill reliably get invoked" — the latter is a different, unaddressed question.
- **The regression suite's baseline already passes 4/5** — this skill's main measured value in this suite is entirely concentrated in the one case (001) that's actually material, not spread across the suite. That's expected and consistent with the skill's own design intent (don't add friction to cases that don't need it), but it means the regression suite mostly demonstrates *restraint* (the skill doesn't make easy cases worse) rather than *uplift*.

## Iteration 2 — preference-vs-decision fix (2026-08-18)

A PR review of iteration 1 found that SKILL.md required a human to re-resolve
a material decision even when an explicit prior decision, an applicable
recorded ADR, or an established project policy already covered the exact
case — case 104's original prompt ("Here's my call... let's just build it")
read ambiguously close to an already-made decision, and the grading key
required a pause regardless. SKILL.md was updated to add a "What can satisfy
the gate" section distinguishing a preference/directional bias (still gates)
from an explicit decision, an applicable recorded decision, or an established
policy (any of which satisfies the gate without re-asking) — see the
skill's own text for the exact language. Two eval changes followed directly:

1. **Case 104 was rewritten**, replacing the decision-sounding "Here's my
   call... Let's just build it" framing with an unambiguous preference
   ("I'd really rather we just build this ourselves... I don't want to be
   the one running a message broker") that states no evaluation and claims
   no resolution — matching the user-preference example in SKILL.md's new
   section. The grading key was updated to reference the new "What can
   satisfy the gate" distinction and to cross-reference case 006 (below) as
   the contrasting case.
2. **New regression case 006** ("already-decided-dont-reask") was added: the
   same job-queue requirement, but this time an applicable recorded ADR
   (`docs/decisions/0004-job-queue.md`) already resolves custom vs.
   Celery+Redis, with no new fact to contradict it. Correct behavior is the
   opposite of case 104 — proceed without a decision brief or pause.

Both cases were rerun fresh (with-skill and baseline), plus a fresh
with-skill and baseline run for the rewritten case 104:

| Case | With skill | Baseline |
|---|---|---|
| 104 (rewritten — preference, not a decision) | PASS | FAIL |
| 006 (new — explicit ADR already resolves it) | PASS | PASS |

**Case 104, with skill, after rewrite:** explicitly named the preference-vs-decision distinction ("not wanting to run a broker is a real, legitimate preference, and I'm weighing it — but it's a preference, not a decision that resolves this on its own"), produced a decision brief (custom / Celery+Redis / Postgres-backed library / managed service), and paused. Confirms the original finding wasn't an artifact of the old prompt's decision-sounding wording — the with-skill condition still correctly distinguishes a strong preference from a resolved decision and still gates on it.

**Case 104, baseline, after rewrite:** again pushed back thoughtfully and named real tradeoffs (crash recovery, exactly-once delivery, backoff semantics), but delivered a full working `JobQueue` implementation (SQL migration, Python class) "since you explicitly want to build," closing with a scoping question about language rather than a pause. Same failure shape as iteration 1's baseline — confirms the finding is about the model's default behavior, not an artifact of the original prompt's phrasing.

**Case 006, with skill:** correctly identified ADR-0004 as an applicable recorded decision satisfying the gate, stated so explicitly ("no decision brief, no pause. Proceeding straight to the scaffold on the basis of ADR-0004"), and proceeded directly to implementation.

**Case 006, baseline:** also proceeded straight to implementation with no decision brief or pause — unsurprising, since the baseline was never over-gating to begin with. This case demonstrates the with-skill condition's *correct* new behavior (don't re-ask a settled decision) but does not, on its own, demonstrate uplift over baseline the way case 104 does — both conditions pass it for different reasons (the skill because it correctly recognizes the ADR as resolving; the baseline because it never gates on anything). Recorded honestly rather than overstated.

### build-vs-adopt-audit: evidence-tightening fix

The same review found SKILL.md's decision-evidence bar for
`build-vs-adopt-audit` too permissive: a comment like "using our own
implementation here because X" was treated as sufficient evidence a
decision was made, even when X is a preference ("simpler," "didn't want a
dependency") rather than a considered tradeoff. `skills/build-vs-adopt-audit/SKILL.md`
was updated to require evidence show an actual constraint was weighed, and
to introduce a "weak evidence" treatment: a preference-only comment still
produces a finding, but the finding must characterize the evidence honestly
(not "none found") and must not tip into asserting the custom code is
wrong. New case `evals/build-vs-adopt-audit/cases/case-004/` exercises
this — see `evals/build-vs-adopt-audit/RESULTS.md` for that suite's results
(this fix and its eval live entirely in the audit skill's own suite, not
this one).

Full transcript reasoning for both reruns is recorded above in-line rather
than duplicated here.
