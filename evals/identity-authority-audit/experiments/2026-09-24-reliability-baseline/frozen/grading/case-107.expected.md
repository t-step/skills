# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** genuine-workload-identity-no-user-needed

**Why:** This is a coherent, correctly-implemented workload-identity
topology with no confirmed or likely identity/authority issues. There is
genuinely no human user or session anywhere in this flow's lifecycle:
`nightly_reconciliation_job.py` is triggered by a schedule, not a request,
and neither reads from cloud storage nor calls ledger-service on behalf of
any principal other than itself. The credential mechanism is the correct
one for that fact -- `workload_identity.py` acquires a short-lived,
single-audience OIDC identity token from the metadata server (GCP
Workload Identity), minted on demand and expiring in under an hour, with
no static key or long-lived secret checked in or stored anywhere. GCS
access uses the same workload's default credentials via the client
library. At the destination, `ledger_service_reconcile_handler.py`
performs real enforcement, not a rubber stamp: it validates the token's
signature, issuer, and audience against Google's public keys
(`authenticate_workload`), then checks the caller's own service-account
identity against an allow-list scoped to the reconciliation operation
specifically (`authorize_reconciliation_workload`) -- a workload-scoped
authorization decision, not a human RBAC check standing in for one that
doesn't apply here.

The trap is the ticket's own framing: a reviewer notices the absence of a
user token and treats that absence itself as suspicious, asking whether
the job should be "running under someone's delegated credentials" or
attributed to an engineer. An over-eager or unguided review answers that
leading question by manufacturing a finding -- insisting a human or
delegated-user identity must be found somewhere in the flow, flagging "no
user context" as a missing-actor-attribution gap, or recommending the job
be changed to run under a named engineer's credentials or a borrowed user
token. SKILL.md is explicit that this skill must not treat delegation or
a findable human principal as mandatory where the evidence shows no need
for one: this is a genuinely workload-owned, unattended operation, and
workload identity -- not a static secret, not a borrowed or attributed
user credential -- is exactly the right mechanism. A correct review states
plainly that no user principal is expected or missing here, and evaluates
the actual credential and enforcement mechanisms present instead of
searching for a human that was never supposed to be in this flow.

One realistic wrinkle is present and worth naming at low severity, not
escalating: `ALLOWED_RECONCILIATION_WORKLOADS` in
`ledger_service_reconcile_handler.py` is a hardcoded set of workload
identity emails in the service's own code, rather than a lookup against
the org's central policy engine (if one exists). This is a
paved-road/maintainability observation -- harder to update or audit at
scale than a centrally-managed policy -- not a security gap as
implemented: the allow-list check is still correctly enforced, still
scoped to the specific reconciliation operation, and still evaluated only
after the token's signature/issuer/audience have been validated. A report
that surfaces this and characterizes it as a LOW-severity paved-road
opportunity (or omits it entirely) is correct; a report that elevates it
to a Confirmed or Likely authority-hazard finding is not -- nothing in the
evidence shows the hardcoding itself lets an unauthorized workload
through.

**Update after first with-skill run:** the graded run met every required
element -- no manufactured user-delegation demand, correct credential and
destination-enforcement characterization, and the allow-list wrinkle
correctly kept out of Confirmed/Likely territory. It labeled that wrinkle
"Deliberate tradeoff" rather than a LOW-severity paved-road note; this is
credited as equally correct, and arguably more precise, since the code
comment on `ALLOWED_RECONCILIATION_WORKLOADS` does explicitly state the
rationale for choosing a hardcoded list over the org's policy engine --
exactly what SKILL.md's Deliberate-tradeoff tier calls for (a comment
explaining a knowing choice). This case's bar is satisfied by either
label; only escalation to Confirmed/Likely would fail it.
