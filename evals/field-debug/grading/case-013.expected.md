# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** poc-authenticates-as-builder-personal-account-against-dev-tenant

**Hidden ground truth:** two facts compound into one real production
blocker, neither of them dramatic on its own:

1. `make login` (per `README.md`) runs an OAuth flow against **the
   individual engineer's own ServiceNow user account** and caches that
   person's refresh token at `~/.snow_token`. `integration.py`'s own
   comment states plainly that every ticket this bridge creates is
   attributed, in ServiceNow's audit log, to whichever human last ran
   `make login` -- not to a service identity. In production this means:
   every auto-created incident is misattributed to one employee; the
   bridge's ServiceNow access is scoped to whatever *that person's*
   ServiceNow permissions happen to be (unknown -- could be broader or
   narrower than the bridge needs); and the whole integration breaks the
   moment that person's password rotates, their account is
   deprovisioned, or they simply leave, with no ownership path back to
   who should fix it.
2. All pilot evidence (`README.md`'s "Status" section, the test suite) is
   against `dev41823.service-now.com` -- a sandbox instance, per
   `.env.example` and the README. Nothing here demonstrates the
   production instance's assignment-group names, permission model, or
   incident-volume behavior; treating the dev-tenant pilot as evidence
   the same config will behave identically in production is an unearned
   assumption, not a confirmed fact.

**What this case is not:** it is not a hidden app-level-auth trap like
`case-007` -- there is no ingress/SSO layer here to credit, and the
identity problem is real, not manufactured. A correct answer still avoids
recommending unrelated heavyweight production hardening (a message queue,
autoscaling, or comparable infrastructure investment) that nothing in
this fixture's evidence calls for at this pilot's scale; the *primary*
blocker this case is built to test is specifically about *whose* identity
and *which* tenant, not about scale or reliability engineering. That said,
`integration.py` has no error handling, no retry, and no dedup/
idempotency key anywhere on the webhook-to-ticket path, and alert-webhook
redelivery causing duplicate tickets is a real, evidenced, in-scope risk
(distinct from unneeded *infrastructure* like a queue or autoscaler) --
naming that gap with that evidence is a legitimate finding, not
cargo-culting, and must not be penalized.

**Plausible wrong paths:** treating "62/62 alerts became tickets in
testing" as evidence of production-readiness without noting it was all
against the dev tenant; naming `make login`'s personal-account pattern as
a vague "needs better auth" without naming the specific consequences
(attribution, break-on-offboarding, unknown permission scope); recommending
a message queue, autoscaler, or other heavyweight infrastructure investment
neither the ticket-creation flow nor the fixture's evidence calls for at
this scale; declining to give a verdict at all on the theory that
identity/authority questions belong to a separate specialist.

## Grading

- REQUIRED: names that production ticket-creation would run under one
  individual engineer's personal ServiceNow credential (via `make login`
  and `~/.snow_token`), not a service identity, as a concrete blocker --
  citing `integration.py`'s own attribution comment or equivalent
  reasoning, not a generic "needs auth" statement.
- REQUIRED: names at least two concrete consequences of that pattern from
  this list (audit-log misattribution to one person, breakage when that
  person's credential/account changes or they leave, and/or unknown/
  unreviewed permission scope tied to that individual) rather than one
  vague mention.
- REQUIRED: explicitly marks the pilot's "all 62 alerts worked" evidence
  as dev-tenant evidence only (`dev41823.service-now.com`), and marks
  production instance behavior -- assignment groups, permissions,
  real incident volume -- as UNKNOWN rather than assumed equivalent.
- REQUIRED: does not recommend a message queue, autoscaler, or comparable
  heavyweight infrastructure investment as a blocker -- nothing in this
  fixture's evidence calls for it at this pilot's scale. (A specific,
  evidenced idempotency/dedup-key gap on the webhook-to-ticket path itself
  -- e.g. noting no dedup key exists and a redelivered webhook would
  create a duplicate ticket -- is a legitimate, evidence-backed finding,
  not the cargo-culting this item exists to catch, and satisfies rather
  than fails this item.)
- REQUIRED: gives an actual verdict and concrete next step (e.g. "not
  production-ready until a dedicated service account with defined
  ServiceNow permissions replaces the personal-login flow, and the
  production tenant's permission/assignment-group config is verified") --
  does not refuse to assess the identity question or defer the entire
  answer to a separate specialist/skill.
- REQUIRED (hiding-behind-uncertainty): gives a real verdict (not
  production-ready, with the specific identity blocker named) rather than
  retreating into "more testing needed" or an all-UNKNOWN non-answer --
  the identity evidence here is conclusive even though the production
  tenant's specifics are genuinely UNKNOWN, and the two must not be
  conflated.
- BONUS: names the concrete ownership question this raises (who owns the
  service account, who's on-call if ServiceNow rejects a ticket in
  production, how the credential gets rotated) rather than stopping at
  "get a service account."
