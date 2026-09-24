# identity-authority-audit — eval results

**Run date:** 2026-09-24
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per
run, default settings.
**Harness:** one subagent per run, given `skills/identity-authority-audit
/SKILL.md` in full and instructed to follow it exactly (including its
exact Review report template), then given exactly the named case files
and nothing else in the repository, and told this is the complete
evidence available. Each run's full report was graded by the orchestrating
session against that case's `grading/case-1XX.expected.md`, cross-checked
against the actual fixture source where a run's claim needed independent
verification (done for cases 101, 102, 106, 107, 112). Raw transcripts are
local, untracked artifacts; this file and the `grading/*.expected.md`
files are the committed, auditable record every claim below cites.

This is iteration 1: the skill's first eval suite, authored and run in the
same session as the skill's own design. See "What this proves / what this
does not prove" before treating any of this as strong validation.

## Numeric summary

- Pressure suite (`pressure-tests/pressure_evals.json`), with-skill:
  **13/13 cases passed** (all REQUIRED expectations met), one run per
  case, first run.
- No baseline (no-skill) runs were collected for this suite, matching
  this skill family's convention for a pressure-style suite (see "Why one
  suite" in `pressure-tests/README.md`): it exists to probe where the
  skill's own stated contract holds or breaks, not to benchmark uplift
  over an unstructured baseline. This is a real limitation, named plainly
  in "What this does not prove" below.
- **Three grading-key updates were made after runs**, all in the
  direction of crediting behavior that exceeded or reasonably diverged
  from the original key, following this skill family's established
  precedent (see `evals/state-ownership-audit/RESULTS.md`'s "Fixture and
  grading-key findings" section) for a first-iteration key turning out
  stricter or narrower than the skill's own correct behavior. See "Fixture
  and grading-key findings" below. No case was re-run against a revised
  key.
- **One in-contract weakness was found and fixed in `SKILL.md` itself**
  (case-108): a Confirmed-tier finding that blended a directly-observed
  structural fact with an unresolved consequence. See "SKILL.md
  correction" below.

## Per-case results

| Case | Scenario | Result |
|---|---|---|
| 101 | Clean BFF with real token exchange | Pass. Correctly credited all three clean properties and directly rejected the "just forward the cookie" framing. Additionally found a real, verified-against-the-fixture scope-over-grant (a GET-only call site requesting `orders:write` too) -- grading key revised to credit this (see below). |
| 102 | Raw forwarding chain, hop discrimination | Pass. Named the BFF→API A hop clean, the API A→API B forward as a confirmed structural fact, and correctly capped the audience-check gap at API B/MCP as *Likely* rather than *Confirmed*, explicitly citing the absent gateway evidence -- exactly the evidence-discipline calibration this case was built to test. |
| 103 | Teams notification, legitimate continuation | Pass. Named the deep link as navigation-only, verified (not assumed) the post-login per-resource authorization check by citing it directly, and named the continue-param open-redirect guard. Also found a real, minor 404-vs-403 tenant-existence disclosure as a bonus finding. |
| 104 | Signed Slack callback: one route misuses it, one doesn't | Pass. Discriminated precisely between the two handlers rather than issuing one verdict for both; named the platform-authenticity-vs-resource-authorization conflation directly; found a bonus identity-representation inconsistency (`approved_by` vs. `comments`). Correctly labeled its own remediation ideas "Design-mode territory." |
| 105 | UI-only authorization | Pass. Named the client-side-only check and the exact missing server-side enforcement; rated Confirmed/HIGH without hedging (correctly, given no gateway evidence at all). Bonus: independently found the adjacent `update_user_role()` privilege-escalation gap. |
| 106 | Legitimate SPA + PKCE, no BFF | Pass. Did not demand a BFF; verified audience/scope narrowing by citing the actual code; correctly kept the 8-hour-token-lifetime detail at Deliberate-tradeoff level. Bonus, verified against the fixture: a real, well-grounded finding about iframe-dependent silent renewal and third-party-cookie blocking. |
| 107 | Genuine workload identity, no user in the loop | Pass. Did not demand user delegation for a genuinely workload-owned job; correctly characterized the credential and destination-side workload authorization. Labeled the hardcoded-allow-list wrinkle "Deliberate tradeoff" rather than "LOW paved-road note" -- verified against the fixture's own rationale comment and credited as an equally correct, arguably more precise call. |
| 108 | User-to-workload transition (async report job) | Pass on substance (named the transition, the enqueue-time freeze, answered the customer's scenario, proposed no fix). Exposed a real, in-contract calibration gap: rated a second finding Confirmed/HIGH while its own Unknowns section named an unresolved destination-side question that could change that consequence. Motivated a `SKILL.md` clarification (see below). |
| 109 | Read/write agent, unused capability metadata | Pass. Named both the shared full-CRUD credential and the unread `"destructive"` field precisely, connected both to directly answer the team's either/or question. Bonus: found a real actor-attribution gap (`session_id`/approver identity never reaches Salesforce). |
| 110 | Proper MCP delegation | Pass, exemplary. Zero manufactured Confirmed/Likely findings; positively named all four required strengths (audience/issuer/expiry validation, scope separation, destination-side authorization, dual actor attribution); raised three sharp, well-grounded "Ambiguity requiring verification" findings pointing precisely at what the supplied evidence can't settle (claim-scoping, refund-grant assurance, token TTL vs. session liveness) -- none of the forbidden speculative noise (no token-replay or generic step-up demands). |
| 111 | Step-up freshness vs. MFA already upstream | Pass, exemplary. Correctly separated the freshness question (wire transfers) from the factor-strength question (billing history, satisfied tenant-wide upstream), and cleanly distinguished a separate, correctly-unconflated session-lifetime observation from the MFA question the ticket asked about. |
| 112 | Secret manager vs. resulting service authority | Pass. Explicitly separated credential management (Vault) from authorization scope, then found and cited the over-broad `GRANT ALL PRIVILEGES` role. Rated it Confirmed/HIGH rather than this key's original MEDIUM-by-default suggestion -- credited as an equally defensible call, consistent with how HIGH was applied to comparably-reachable findings elsewhere in this suite (see grading-key update below). |
| 113 | Recovery flow inherits primary assurance label | Pass, exemplary. Named the `amr` mislabeling and the weaker-factor authority grant as two distinct, properly-connected Confirmed findings; stayed scoped to the fixture's own evidence rather than expanding into general SMS-carrier or IdP-recovery-policy commentary. |

## Fixture and grading-key findings

Three with-skill runs (cases 101, 107, 112) surfaced real, code-grounded
subtlety or a defensible severity/tier judgment call the original grading
keys did not anticipate, in every case verified independently against the
actual fixture source before crediting it -- not taken on the run's own
word.

- **Case 101** was designed as a clean, no-findings BFF/token-exchange
  case. The run additionally reported that `token_exchange.py`'s
  `exchange_for_orders_api()` unconditionally requests
  `scope="orders:read orders:write"`, while the only call site in
  evidence (`bff_orders_route.py`'s `get_order`) is GET-only and never
  performs a write -- verified directly against both files: true as
  written. The finding was reported as Confirmed/MEDIUM with explicit,
  correct hedging about whether other unshown call sites justify the
  shared scope. This is not the fabricated "needless complexity" finding
  the case was built to guard against; it doesn't question the exchange
  mechanism, the BFF pattern, or the session mechanism at all. The
  grading key was revised to require no fabricated finding about those
  three things specifically, rather than "zero findings of any kind,"
  which this fixture does not actually guarantee.
- **Case 107** labeled the hardcoded reconciliation allow-list a
  "Deliberate tradeoff" rather than the "LOW paved-road note" the key
  suggested. Verified against `ledger_service_reconcile_handler.py`: the
  code carries an explicit comment stating the rationale for choosing a
  hardcoded list over the org's policy engine -- exactly what
  `SKILL.md`'s Deliberate-tradeoff tier is defined to require (a comment
  explaining a knowing choice). The grading key was revised to accept
  either label.
- **Case 112** rated the over-scoped Vault-issued database role
  Confirmed/HIGH rather than the MEDIUM the key suggested as a default.
  The finding fits `SKILL.md`'s own HIGH definition ("a sensitive write
  reachable without appropriate authorization") without requiring
  separate proof of exploitation, consistent with how HIGH was applied to
  comparably-reachable findings elsewhere in this suite (case-105's
  UI-only authorization, also rated HIGH on reachability alone). The
  grading key was revised to accept either MEDIUM or HIGH.

None of these three required a fixture code change and none required a
rerun -- in each case the original transcript already satisfies the
revised expectations, and each revision was checked against the fixture's
actual source (not the run's own restatement of it) before being made.

## SKILL.md correction

**Case 108** exposed a real, in-contract calibration gap, not a fixture
or grading-key issue. The run's second finding ("No destination-side
re-authorization; the worker's broad service credential is the only
authority present at data-fetch time") was rated Confirmed/HIGH, while
the same finding's own "Unresolved uncertainty" and the report's
"Unknowns" section both named that the data warehouse might independently
enforce a project-level ACL the supplied code doesn't show. This is
exactly the pattern `SKILL.md`'s evidence-discipline section already
warns against in the abstract (prefer "not visible in the inspected
path; verify" over "is missing") but the tier-selection guidance didn't
yet make the connection explicit for a finding that mixes an observed
structural fact with an unresolved consequence in one sentence. `SKILL.md`
was revised (the "Sort every finding into exactly one tier" section) to
state this directly: a finding whose own Unresolved-uncertainty line
names something that could change its stated consequence should not
carry Confirmed-level certainty for that consequence -- split the
structural fact (Confirmed) from the consequence (Likely), or into two
findings. The case was not re-run against the revised wording; this
remains a single N=1 observation of the failure mode, not a repeated
pattern, and the fix is recorded here as a small, targeted clarification
rather than a rewrite, per this skill family's practice of matching
evidence effort to the size of an observed defect.

## What the suite as a whole shows

Across all 13 cases, the with-skill runs consistently:

- **Discriminated within a single fixture rather than issuing one verdict
  for the whole system.** Cases 102 and 104 each contain a clean hop/route
  and a broken one; every run correctly separated them instead of
  clearing or condemning the fixture as a whole.
- **Held the Confirmed/Likely/Ambiguity distinction under real pressure.**
  Case 102's core test -- capping an audience-check gap at *Likely*
  because no gateway evidence exists, rather than declaring it flatly
  missing -- was met precisely, and case 110's three "Ambiguity requiring
  verification" findings (with zero manufactured Confirmed/Likely
  findings on an intentionally coherent design) is the clearest positive
  evidence in this suite that the skill can tell the difference between a
  real, evidence-backed structural fact and a genuine unresolved question.
  Case 108 is the one clear counter-example (see above).
- **Avoided every reference-architecture bias the suite specifically
  tested for.** No run demanded a BFF for the PKCE SPA (106), demanded
  user delegation for the workload-owned job (107), or invented a finding
  against the coherent MCP design (110) -- the three cases built
  specifically to catch this failure mode all passed cleanly.
- **Refused scope creep consistently.** No run drifted into a specific
  remediation design being asserted as the point of a Review-mode
  finding (case 104 explicitly labeled its own fix ideas "Design-mode
  territory"; case 108 and 109 both stopped at naming the gap); no run
  expanded case 113's recovery-assurance finding into a general SMS-
  carrier or IdP-administration audit, matching `SKILL.md`'s explicit
  scope refusal.
- **Found several real, fixture-verified bonus findings** (101's scope
  over-grant, 103's 404/403 disclosure, 104's attribution inconsistency,
  105's adjacent privilege-escalation endpoint, 106's iframe/third-party-
  cookie issue, 109's missing actor attribution to Salesforce) -- none of
  which were fabricated; every one checked against the fixture source
  before being credited in this write-up.

## What this proves / what this does not prove

**What it's suggestive of:** across 13 designed scenarios spanning clean
BFF/token-exchange, SPA/PKCE, workload identity, and proper-MCP-delegation
false-positive-resistance tests; platform-authenticity-vs-authorization,
UI-only-authorization, user-to-workload, read/write-capability-boundary,
step-up-vs-upstream-MFA, secret-manager-vs-authorization, and recovery-
assurance issue-detection tests; and one hop-discrimination/evidence-
discipline restraint test -- the skill, run once per case with a fresh
subagent and no prior context, consistently reconstructed an accurate
hop-by-hop identity flow, applied the Confirmed/Likely/Ambiguity/
Tradeoff/Convention vocabulary correctly in the large majority of
instances, avoided every specific reference-architecture bias the suite
was built to catch, and held its Review-mode scope boundary (no
remediation designs asserted as findings) throughout.

**What it does not prove:** every case was run exactly once, with one
model family (claude-sonnet-5) and default settings -- this is not a
statistically powered benchmark, and any single case could look different
on a repeat sample. No baseline (no-skill) comparison was collected for
this suite at all, so there is no direct evidence of how much of this
behavior a capable, unguided model would reach on its own -- unlike
`state-ownership-audit`'s and `lifecycle-audit`'s regression suites, which
found baseline often reaches the same substantive conclusion and
differs mainly in scope discipline and vocabulary. All 13 fixtures are
synthetic, single-author-constructed systems in the 2-4-file range,
written by the same session that wrote `SKILL.md` and every grading key
-- a known source of unintentional alignment between what a fixture
rewards and what the skill happens to emphasize; the fixture-authoring
work was split across parallel subagents from precise specifications
this session wrote, and grading-key revisions were made by the same
session that authored the original keys, checked against fixture source
directly rather than taken on faith, but not by an independently
recruited second reviewer (unlike `state-ownership-audit`'s iteration 1,
which used a fresh adversarial subagent specifically to check its own
grading-key revisions -- that additional check was not done here and is
named as a gap below). No fixture combines more than two or three of the
skill's named failure categories at once, and none exceeds four files;
whether the skill's discrimination and evidence-discipline behavior holds
on a larger, messier, real-world codebase (rather than a small synthetic
one built to isolate a single question) is untested. Explain and Design
modes were not exercised by this suite at all -- only Review mode was
run, since all 13 scenarios in the design brief were framed as review
questions; Explain mode's report shape and Design mode's "smallest
coherent change" discipline have zero eval coverage in this iteration.
The engagement-profile YAML block was never requested or produced in any
of the 13 runs (none of the prompts asked for it, and SKILL.md marks it
optional), so it has no evidence behind it either.

## Remaining weaknesses and open questions

- **Confirmed/Likely calibration when a finding's own Unknowns section
  contradicts its stated certainty** (case 108) is a real, observed,
  in-contract failure mode, now addressed by a small `SKILL.md`
  clarification but not re-tested. A second fixture specifically
  targeting this exact pattern (a Confirmed-looking finding whose
  consequence secretly depends on an unshown component) would be the
  most valuable next addition to this suite.
- **No baseline comparison at all.** Unlike sibling suites in this
  family, this iteration has zero evidence of what an unguided model
  would do on any of these 13 scenarios. Given how much of this skill's
  apparent value (per the family's own established pattern) tends to be
  scope discipline and vocabulary rather than reaching different
  conclusions, this is a real gap, not a formality.
- **No independent adversarial review of the grading-key revisions.**
  `state-ownership-audit`'s iteration 1 used a fresh subagent to
  specifically pressure-test whether its own author's grading-key
  revisions were legitimate recalibrations or quiet weakening. This
  iteration's three revisions (101, 107, 112) were checked against
  fixture source directly by the same session that wrote the original
  keys, which is a real check but not an independent one.
- **Explain and Design modes have no eval coverage.** This suite tests
  Review mode exclusively. Explain mode's ten-category report shape and
  Design mode's "smallest coherent change, name the property restored"
  discipline (including the "Exchange the incoming user credential..."
  vs. "API B currently accepts authority intended for API A..." contrast
  `SKILL.md` itself specifies) are both entirely unexercised.
- **No fixture larger than four files or combining more than two or
  three failure categories at once.** Whether the "what earns a full
  entry"-style admission bar this skill implicitly relies on (deciding
  which hops matter enough to report on) degrades gracefully on a real,
  messy, many-hop production codebase is untested.
- **No test of the organization-specific profile mechanism.** No case in
  this suite supplies `references/organization-profile-template.md`-style
  input; whether an "organization-specific convention" tier finding is
  correctly resolved when a real profile is present has zero coverage.
