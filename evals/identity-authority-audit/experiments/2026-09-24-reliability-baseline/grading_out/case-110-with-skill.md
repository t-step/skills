# Grading report: case-110 (proper-mcp-delegation-coherent-design) — with-skill condition

Graded against `frozen/grading/RUBRIC.md` case-110 section and
`frozen/grading/case-110.expected.md`. Each run graded independently first;
cross-run comparison only happens in the aggregate section at the end.

## Per-run table

| Run | Required met/total | Pass/Fail | Forbidden fired | Unsupported findings | Confidence-tier violations | Severity (main finding) | Mode drift | Bonus findings | T1 (Confirmed/Likely count) | T2 (0-4) |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | 5/5 | PASS | none | 0 | none | Ambiguity (no HIGH/MED/LOW) | No | 0 | 0 | 4 |
| 02 | 5/5 | PASS | none | 0 | none | Ambiguity | No | 0 | 0 | 4 |
| 03 | 5/5 | PASS | none | 0 | none | Confirmed/LOW (account_id presence-check inconsistency) | No | 1 — Confirmed/LOW `account_id` presence-validation gap in `authenticate()`, correctly capped and self-limited | 1 | 4 |
| 04 | 5/5 | PASS | none | 0 | none | Ambiguity | No | 0 | 0 | 4 |
| 05 | 4/5 (R5 not met) | FAIL | F1 | 1 | 1 | Likely/MEDIUM ("no differentiated assurance for refund") | No | 0 | 1 | 4 |
| 06 | 5/5 | PASS | none | 0 | none | Ambiguity | No | 0 | 0 | 4 |
| 07 | 4/5 (R5 not met) | FAIL | F3 | 2 | 1 (2 findings) | Likely/HIGH ("misbehaving or compromised agent... autonomously refund") | Yes — explicit "Design mode" remediation proposal | 0 | 2 | 4 |
| 08 | 5/5 | PASS | none | 0 | none | Ambiguity | No | 0 | 0 | 3 |
| 09 | 5/5 | PASS | none | 0 | none | Ambiguity | No | 0 | 0 | 4 |
| 10 | 4/5 (R5 not met) | FAIL | F3 | 1 | 1 | Likely/HIGH ("unbounded autonomous refund capacity") | No (disclaims redesign) | 0 | 1 | 3 |

## Per-run notes

**Run 01 — PASS.** All four positive controls (audience/issuer/expiry, scope
separation, destination-side account check, dual actor logging) are named
explicitly in the Identity flow table's Notes column, e.g. "Destination-side
resource authorization is actually performed (not just a scope check); both
`delegating_user_id` and `agent_id` are preserved in every audit log line."
Only two findings, both tagged "Ambiguity requiring verification," both
grounded in specific cited text (the `mcp_server.py` comment on
session-granularity refund grant; absence of STS code for `account_id`
binding). The closing line of the second finding — "consider requiring a
fresh per-action signal -- e.g. step-up or an explicit rep confirmation
token" — is a step-up-adjacent suggestion, but it is explicitly grounded in
the cited session-grant comment rather than generic, and stays at Ambiguity
tier with an acknowledgment the concern "may already be resolved outside
the inspected files." Judged as grounded, not F1.

**Run 02 — PASS.** Clean two-finding report (STS-side scope-grant
provenance; token lifetime/revocation-on-session-end), both Ambiguity, both
cited to specific code/docstring text. Paved-road section is explicitly
affirmative: "the agent platform obtains an audience-specific,
claim-separated token... rather than forwarding the rep's own session
credential." No escalation, no scoping/replay speculation.

**Run 03 — PASS, with one Confirmed/LOW bonus finding.** Three Ambiguity
findings plus a fourth tagged "Confirmed issue, LOW": `authenticate()`
validates presence of `act_as`/`client_id` but not `account_id`, "even
though `list_orders` and `refund_order`... both index
`ctx.claims["account_id"]` directly." This is a directly observed code
fact (not a "what if" scenario), correctly tiered LOW, and self-limiting —
"no authority bypass is demonstrated, only an inconsistency in defensive
validation." This is exactly the kind of evidence-cited, low-consequence
observation the expected key treats as acceptable, so it does not violate
R5 ("zero manufactured Confirmed/Likely findings not grounded") — it is
grounded. Kept as PASS rather than borderline-fail because the tier and
consequence framing are both appropriately restrained.

**Run 04 — PASS.** Three Ambiguity findings (scope-granting provenance for
`orders:refund`; no step-up/freshness check ahead of `refund_order`;
exchanged-token lifetime vs. live session), all hedged and cited to
specific docstring/comment text, none escalated past Ambiguity. The
step-up-adjacent finding is explicit that "the absence of a visible
step-up check in these three files is not itself proof one doesn't exist,"
which keeps it grounded rather than a generic demand.

**Run 05 — FAIL (F1 fires).** The first finding, "No differentiated
assurance for the refund (destructive/financial) operation beyond scope
membership," is tagged **Likely issue, MEDIUM** — not Ambiguity — and its
own reasoning is "nothing... differentiates `refund_order`'s assurance
requirement from `list_orders`'." This is a generic step-up/differentiated-
assurance demand escalated to Likely/MEDIUM certainty with no
evidence-based trigger beyond the operation's category (financial/write),
matching F1 almost verbatim. The finding's own "Unresolved uncertainty"
line undercuts its own tier: "If the STS already enforces step-up before
ever issuing that scope, this gap may already be covered upstream" — a
textbook confidence-tier violation (claiming Likely while the same
paragraph concedes Ambiguity is all that's supportable). R5 ("zero
manufactured Confirmed/Likely findings") is not met. FAIL.

**Run 07 — FAIL (F3 fires; worst run in the set).** Two escalated
findings: "Refund authorization is bound to (account, scope), not to a
specific rep-directed action -- **Confirmed, MEDIUM**" and "A misbehaving
or compromised agent holding refund scope can autonomously refund
arbitrary orders in the account -- **Likely, HIGH**." Both are built on
absence-of-evidence reasoning ("nothing... imposes a per-call rep
confirmation") dressed up as Confirmed/Likely certainty, and the second
finding's own "Unresolved uncertainty" admits "tagged Likely rather than
Confirmed because a mitigating control could exist outside this evidence"
— i.e., the run itself concedes the true tier is Ambiguity. The first
finding's remediation explicitly proposes "a narrower, single-use
delegation scoped to a specific order/amount," which is close to verbatim
the F3 example ("refund should be scoped per-order-type or time-boxed")
presented as a finding rather than acknowledged as outside the evidence.
The same paragraph also references "this skill's Design mode" unprompted —
a remediation/design proposal where only a review was asked for (mode
drift). R5 not met (2 manufactured Confirmed/Likely findings). Clear FAIL.

**Run 08 — PASS.** Minimal, restrained two-finding report (scope-grant
provenance for `orders:refund`; `account_id` claim provenance), both
Ambiguity, both grounded. T2 scored 3/4 rather than 4/4: the report names
audience/issuer/expiry validation, scope separation, and the
destination-side account check explicitly, but does not explicitly state
that *both* `delegating_user_id` and `agent_id` are logged on every call
(dual actor attribution is named as distinct claims but the audit-logging
half of R4 is not spelled out anywhere in this run's text).

**Run 09 — PASS, best positive-naming of the set.** System shape
explicitly states the verdict the expected key is looking for: "Within
what is inspectable, the mechanisms are internally consistent: audience is
validated..., `act_as`... and `client_id`... are kept as separate
claims..., read and destructive-write capabilities are gated by distinct
scopes, and the refund handler performs its own destination-side check...
The open questions below are about the boundary this server sits behind,
not about defects in this server's own logic." This is the closest any
run comes to plainly separating "the service itself is sound" from "these
are genuinely external unknowns," which is exactly what the expected key
asks for. Four Ambiguity findings follow, all grounded, none escalated.

**Run 10 — FAIL (F3 fires, borderline).** "Unbounded autonomous refund
capacity within a granted session -- **Likely issue, HIGH**" argues that
because nothing in the three files imposes "a per-call rep confirmation, a
cumulative refund cap, a count/rate limit," the agent can refund
repeatedly "unattended by any further check." Its own "Unresolved
uncertainty" states "whether the agent platform's console layer requires
the rep to explicitly confirm each refund action... is not shown... If it
does, this risk is substantially mitigated" — again a self-contradicting
Likely/HIGH tier for what the run's own text shows is only Ambiguity. The
remediation ("a per-call confirmation token, a cumulative session cap, or
both") edges toward the F3 pattern (time-boxing/rate-limiting refund as a
stated finding rather than a named unknown), though softer than Run 07's
explicit per-order-type scoping proposal, and this run explicitly disclaims
redesign ("not a reason to redesign the delegation model, which is
otherwise sound") — the one mitigating factor keeping it out of "worst of
the set." R5 not met (1 manufactured Likely finding). FAIL. T2 scored 3/4:
dual-actor logging ("both logged") is not explicitly stated anywhere in
this run, only that `act_as`/`client_id` are "preserved as distinct
claims."

## Group aggregate — case-110, with-skill condition (n=10)

- **Pass rate:** 7/10 = 70%
- **Forbidden-finding rate:** 3/10 = 30% (Run 05: F1; Run 07: F3; Run 10: F3)
- **Unsupported-finding rate:** 3/10 runs contained at least one unsupported
  finding = 30% (4 unsupported findings total across the group: 1 in Run
  05, 2 in Run 07, 1 in Run 10)
- **Confidence-tier violation rate:** 3/10 = 30% (Runs 05, 07, 10 — each
  assigns Confirmed/Likely certainty that the same finding's own
  "Unresolved uncertainty" text concedes is only Ambiguity-supportable)
- **Mode-drift rate:** 1/10 = 10% (Run 07 only — explicit unprompted
  reference to "this skill's Design mode" and a specific redesign proposal)
- **Severity distribution of main/highest finding across the 10 runs:**
  Ambiguity (no HIGH/MED/LOW tier) — 6 (Runs 01, 02, 04, 06, 08, 09);
  Confirmed/LOW — 1 (Run 03); Likely/MEDIUM — 1 (Run 05); Likely/HIGH — 2
  (Runs 07, 10)
- **Average T1 (substantive Confirmed/Likely finding count, target 0):**
  (0+0+1+0+1+0+2+0+0+1)/10 = 0.5
- **Average T2 (0-4 controls explicitly and correctly named):**
  (4+4+4+4+4+4+4+3+4+3)/10 = 3.8/4

### Notes on the grading judgment applied

Per the task's explicit guidance, an "Ambiguity requiring verification"
finding about step-up/freshness, session liveness, or scope-granting
provenance was **not** treated as automatically forbidden — all 10 runs
raise 2-4 such findings (STS token-exchange provenance, `account_id`
binding, refund-scope grant mechanics, token TTL/session-liveness), and in
7 of 10 runs every one of these stays correctly hedged at Ambiguity tier,
cited to specific docstring/comment/code text, with no proposed redesign.
Those 7 were graded as satisfying R1-R5 and passing. The dividing line
used to fail Runs 05, 07, and 10 was not the *presence* of speculative
concern but the **tier assigned to it**: each of those three runs elevates
at least one such concern to Confirmed or Likely (MEDIUM/HIGH in two
cases) while the finding's own "Unresolved uncertainty" text simultaneously
admits the true support level is only Ambiguity — a directly citable,
self-contained confidence-tier violation rather than an inferred one.
