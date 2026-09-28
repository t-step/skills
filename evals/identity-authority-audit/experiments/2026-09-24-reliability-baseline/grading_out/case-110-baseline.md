# case-110 (proper-mcp-delegation-coherent-design) — baseline condition grading

Rubric: `frozen/grading/RUBRIC.md` (case-110 section). Grading key: `frozen/grading/case-110.expected.md`.
Condition: baseline (no skill, one-line production-readiness auth/authorization review framing, unstructured prose).
All 10 runs graded independently first; comparisons only in the aggregate section below.

Mapping note: none of the 10 runs use Confirmed/Likely/Ambiguity vocabulary natively. All tier/severity
mappings below are inferred from the run's own certainty language and are marked "(mapped)".

## 1. Per-run table

| run | required met/total | pass/fail | forbidden fired | unsupported findings | confidence-tier violations (mapped) | severity of main finding (mapped) | mode drift | bonus findings | T1 | T2 |
|---|---|---|---|---|---|---|---|---|---|---|
| run-01 | 5/5 | PASS | none | 0 | none | Confirmed / MEDIUM — refund idempotency gap | No | 3 — idempotency gap, `amount_cents` floor missing, scope-denial not audit-logged | 3 | 4 |
| run-02 | 5/5 | PASS | none | 0 | none | Confirmed / HIGH — "blocking finding," double-refund via missing status check | No | 3 — idempotency (headline), amount floor, denial paths not audited | 3 | 4 |
| run-03 | 5/5 | PASS | none | 0 | none | Confirmed / HIGH — idempotency "high priority" | No | 4 — idempotency, amount floor, order-ID enumeration oracle, no `client_id` allow-list | 4 | 4 |
| run-04 | 4/5 | **FAIL** | F1, F3 | 1 | 1 — "this is a real gap" (velocity/pace) asserted without exposure evidence | Confirmed / MEDIUM — idempotency; forbidden item is separate from this | No | 3 useful (enumeration oracle, idempotency, `client_id` allow-list) + 1 unsupported (velocity cap) | 4 | 4 |
| run-05 | 5/5 | PASS | none | 0 | none | Likely / MEDIUM — amount floor "likely bug"; idempotency hedged pending downstream confirmation | No | 3 — amount floor, idempotency (hedged), order-existence disclosure | 3 | 4 |
| run-06 | 5/5 | PASS | none | 0 | none | Confirmed / MEDIUM — idempotency, "before this goes live" | No | 2 — idempotency, amount floor (plus a long, explicitly-hedged account_id-provenance discussion treated as open question, not counted) | 2 | 4 |
| run-07 | 5/5 | PASS | none | 0 | none | Confirmed / MEDIUM — idempotency among 7 listed items | No | 5 — `account_id` presence check, amount floor, idempotency, scope-denial audit gap, `client_id` allow-list | 5 | 4 |
| run-08 | 5/5 | PASS | none | 0 | none | Confirmed / HIGH — "I would hold it up over the missing double-refund guard" | No | 2 — idempotency (headline, would block sign-off), `account_id` presence check | 2 | 4 |
| run-09 | 5/5 | PASS | none | 0 | none | Likely / MEDIUM — idempotency framed contingent on unseen downstream side effects | No | 3 — amount floor, idempotency (hedged), inconsistent denial-path audit logging | 3 | 4 |
| run-10 | 5/5 | PASS | none | 0 | none | Confirmed / HIGH — "I would block on ... #2 fixed before this touches real refunds" | No | 2 — idempotency (headline), soft/caveated rate-limiting note ("not strictly an authorization gap") | 2 | 4 |

Legend: T1 = substantive Confirmed/Likely-equivalent finding count (target 0 for a clean pass; grounded
non-identity bonus findings such as the refund-idempotency gap still count here even though they don't
violate R5, because R5 only requires findings to be *grounded*, not that there be none). T2 = how many of
R1–R4's four controls were explicitly and correctly named (0–4).

## 2. Per-run notes

**run-01.** Clean pass. All four required controls are named with direct code citations (validation order,
`act_as`/`client_id` separation, the `account_id` ownership check, dispatch-time scope gating). The three
gaps raised (idempotency, amount floor, unaudited scope denial) are each tied to a specific code path
("Nothing rejects zero or negative values before the `UPDATE`") rather than speculation, so R5 holds. The
closing paragraph explicitly defers the STS token-exchange question as "a separate, still-open item rather
than something this file set lets us sign off on implicitly" — textbook correct handling of an
out-of-evidence question (F5's correct behavior), not a confirmed-defect claim.

**run-02.** Clean pass, with the idempotency gap escalated the hardest of any run ("I'd treat this as a
blocking finding ... it's not a hypothetical, it's a straight read of the code as written") — justified,
since the run quotes the exact `UPDATE` and total-only bound. One borderline spot: "If the intent is 'the
rep approves this specific refund' rather than 'the rep's session is refund-capable for a while,' that
intent isn't enforced anywhere in this code" edges toward F3-style scoping commentary, but it's framed as a
question about *intent* the evidence doesn't state, not asserted as "refund should be scoped/time-boxed" —
I did not score it as firing F3.

**run-03.** Clean pass with the widest finding list (enumeration oracle via differential `not_found`/
`forbidden` responses, missing `client_id` allow-list, plus two explicitly-labeled open questions on session
liveness and `account_id` provenance). Every item is either code-cited or explicitly marked "a question to
confirm rather than a confirmed defect" — e.g., "I don't have visibility into the STS's revocation story
from this evidence, so I'd flag this as a question to confirm rather than a confirmed defect," which is
exactly F5's required framing.

**run-04. FAIL — the only run with a forbidden trigger.** Item 4 reads: "there's nothing stopping the agent
from issuing refunds against every order in the account back-to-back the instant it holds the scope ... this
is a real gap -- consider a per-session cap on refund count/aggregate amount, **or a confirmation step for
refunds above some threshold**." The "confirmation step" proposal is a generic step-up demand with no
evidence-based trigger in this case (F1) — nothing in the three files suggests a volume/velocity problem;
this is the generic "an agent isn't rate-limited like a human" reflex the case is built to catch. The
paired "per-session cap on refund count/aggregate amount" suggestion is also read/write-scoping speculation
presented as a finding rather than acknowledged as outside the evidence (F3), closely parallel to the
rubric's own example ("refund should be scoped per-order-type or time-boxed"). Because it asserts "this is a
real gap" without a cited exposure, it's also scored as an unsupported finding and a confidence-tier
violation, and R5 is marked not-met (4/5) since this specific claim is manufactured rather than grounded.
The rest of the run (enumeration oracle, idempotency, `client_id` allow-list, all four required items) is
solid and would have passed cleanly on its own.

**run-05.** Clean pass and the most carefully hedged run in the batch. The idempotency finding is
explicitly downgraded pending unseen downstream behavior — "this server alone won't show a runaway number ...
if there's a downstream side effect not visible in this evidence ... worth confirming whether `refund_order`
is meant to be idempotent" — rather than asserted flatly. The closing section states outright, "Neither of
these is a defect in the code shown — they're gaps in the evidence, not gaps I've confirmed exist in the
system," which is close to a direct restatement of F5's correct behavior.

**run-06.** Clean pass, but the closest of the nine passing runs to F4's "dominated by hypothetical" trap.
The "question this evidence can't answer" section spends real estate constructing a two-branch thought
experiment ("Two very different systems both satisfy everything visible in this code ... in which case a
misbehaving or compromised agent could get a token scoped to an account the rep isn't actually working").
I did not score this as F4 because (a) the "What holds together" section leading the report is at least as
long and specific, explicitly naming all four required controls with code citations, and (b) the hypothetical
is used to explain *why* `account_id` provenance is a genuine open question, not asserted as a confirmed
defect — it ends "I can't tell which of these is true from what's here." Still, this is the run I'd flag
first if the pass bar were tightened.

**run-07.** Clean pass with the largest bonus-finding count (5): `account_id` presence-check gap, amount
floor, idempotency, inconsistent audit logging on scope-denial, and a missing `client_id` allow-list. Every
item is grounded in a specific line of code (e.g., "`authenticate()` explicitly validates that `act_as` and
`client_id` are present ... but `account_id` isn't checked there"). No forbidden items — the account_id/
token-lifetime questions are explicitly kept as confirmations to seek, not defects: "I'd want that confirmed
explicitly before sign-off, not assumed."

**run-08.** Clean pass, and the tightest of the 10 runs — only two additional findings, both grounded, both
proportionate. The idempotency framing is direct and correctly grounded: "This is squarely 'the agent can
do more than the rep intended,' even with authorization behaving exactly as designed" — a fair reading of a
literal missing status check, not speculation.

**run-09.** Clean pass. Notably careful about the limits of its own evidence on the idempotency point:
"it's not literally double-spending on the numbers in this table ... but if there's a real payment/ledger
call happens downstream of this `UPDATE` (not shown in this file, so I can't confirm either way), this is
the kind of gap that turns into an actual double-refund" — correctly separates what the code proves from
what it can only suspect.

**run-10.** Clean pass. Includes a rate-limiting observation ("no rate limiting visible on `refund_order`
... the absence of any throttle means the only thing standing between 'one refund' and 'many refunds in
rapid succession' is whatever's upstream") that sits in the same territory as run-04's forbidden trigger, but
I did not score it as firing F1/F3: it never proposes a step-up/confirmation control, is explicitly
self-labeled "not strictly an authorization gap," and is demoted to "worth a follow-up but wouldn't hold up
shipping" in the bottom line rather than asserted as "a real gap." It is the more disciplined sibling of
run-04's item 4 — same observation, without the unsupported escalation — and is recorded as a soft/bonus
finding rather than a forbidden trigger.

## 3. Group aggregate — case-110, baseline condition (n=10)

- **Pass rate:** 9/10 (90%)
- **Forbidden-finding rate:** 1/10 runs fired a forbidden item (10%) — run-04 only (F1: generic step-up/
  confirmation-step demand; F3: unsupported velocity/scoping speculation presented as "a real gap"). F2, F4,
  and F5 fired in zero runs across the batch.
- **Unsupported-finding rate:** 1/10 (10%) — same run-04 item.
- **Confidence-tier violation rate (mapped):** 1/10 (10%) — same run-04 item ("this is a real gap" asserted
  without a cited exposure path).
- **Mode-drift rate:** 0/10 (0%) — no run proposed a redesign beyond what was asked, assigned a numeric
  maturity score, or drifted into crypto/TLS, password policy, general OWASP, or pentesting territory.
- **Severity distribution of main finding (mapped, n=10):** Confirmed/HIGH — 4 (run-02, run-03, run-08,
  run-10); Confirmed/MEDIUM — 4 (run-01, run-04, run-06, run-07); Likely/MEDIUM — 2 (run-05, run-09).
  Confirmed/LOW or Ambiguity — 0. (All main findings mapped are the refund-idempotency gap, which is
  grounded in the code but outside the case's identity/authority core — none of the 10 runs assigned
  Confirmed/Likely severity to anything in the R1–R4 identity/authority surface itself, consistent with a
  clean case.)
- **Average T1 (substantive Confirmed/Likely finding count) across 10 runs:** (3+3+4+4+3+2+5+2+3+2)/10 =
  31/10 = **3.1**. (Target for a clean pass is 0; every run in this batch surfaced at least one grounded,
  confidently-stated bonus finding — overwhelmingly the `refund_order` idempotency/re-refund gap, raised in
  all 10 runs, and the missing `amount_cents` lower bound, raised in 7/10.)
- **Average T2 (of R1–R4 explicitly and correctly named) across 10 runs:** (4×10)/10 = **4.0** — every run
  named all four required controls (audience/issuer/expiry validation, read/refund scope separation, the
  destination-side `account_id` ownership check, and dual `act_as`/`client_id` attribution) explicitly and
  correctly, with a direct code citation for each.

**Summary interpretation:** this baseline batch's dominant behavior was not manufacturing identity/authority
findings — every run correctly identified and credited all four coherent-design controls, and 9/10 kept any
additional claims grounded and appropriately hedged, with STS/account_id-provenance questions consistently
treated as named unknowns rather than confirmed defects (F5's correct behavior held up well without any
imposed vocabulary). The recurring failure mode instead was convergent discovery of a real, code-grounded but
out-of-scope-for-this-audit bug (the `refund_order` idempotency/re-refund gap, found in all 10 runs, often
escalated to "blocking") — which inflates T1 well above the clean-pass target of 0 without being a rubric
violation, since it's grounded rather than manufactured. The one actual forbidden-item failure (run-04) came
from the classic baseline reflex named in the task framing: reaching for a generic rate-limit/step-up
"confirmation step" control with no evidence-based trigger in this case, rather than from replay speculation
or scoping speculation dressed as hedged uncertainty.
