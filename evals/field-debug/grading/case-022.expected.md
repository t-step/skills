# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** scoped-witnesses-webhook-ack-vs-crm-ingestion-validation

**Hidden ground truth:** Northwind's inbound webhook endpoint
(`/api/webhooks/customer-sync`) returns HTTP 200 as soon as it *receives*
a batch, before any ingestion into the CRM itself -- receipt is
acknowledged synchronously, ingestion happens asynchronously afterward.
Northwind recently enabled a new required-field validation on their
CRM-side ingestion worker requiring an `account_region` field on every
inbound customer record (part of an internal data-residency change on
their side, not announced to us). Our `crm_sync_job.py` has never sent
this field -- our own `customers` table already has the equivalent data
(`customer.region`), it's simply never been mapped into the outbound
payload (`crm_payload_mapping.md`). Every record we've sent since
Northwind's change has been accepted at the webhook (200, "received") and
then silently rejected by their async ingestion validator, so it never
becomes a visible CRM record and never appears in Northwind's own
customer-facing audit trail either -- it only shows up in a separate,
less-obvious admin error view.

Three vantage points, each reporting a real, true observation from their
own layer:
- **Dana** (Northwind Integrations Ops): checked the Integration
  Middleware Dashboard, which tracks webhook-receipt acknowledgment only.
  "Delivered" is true and accurately reported -- it is not, and was never
  claimed by Dana to be, evidence that the CRM itself ingested anything.
- **Priya** (our platform SRE): the job log shows 3412/3412 posted, 0
  send errors, all HTTP 200. Also true, and also only establishes that
  *our* send path succeeded -- not that Northwind's CRM processed
  anything.
- **Chris** (Northwind CRM admin, covering for Dana): the CRM's regular
  customer-facing audit trail shows nothing new (matching the original
  complaint), because rejected records never become customer records in
  the first place. The discriminating evidence is in a separate
  "Integration Errors" admin view he doesn't normally check, which shows
  every rejected record and the reason.

Dana's "Delivered" and the original "nothing new has shown up" complaint
are the superficially conflicting pair that are **both true** -- one
describes webhook-receipt acknowledgment, the other describes CRM-side
ingestion, and Northwind's own ack-then-async-validate design is exactly
why they can diverge with no error surfaced anywhere in between.

**Why this stays genuinely undiscoverable without Chris:** neither
`crm_sync_job_log.md` nor `middleware_dashboard_export.md` can ever
distinguish "sent and accepted" from "sent, accepted, and actually
ingested" -- both describe transport, not ingestion. Some evidence for
the "ack != processed" possibility is available beforehand
(`middleware_dashboard_export.md` itself notes the dashboard tracks
webhook receipt, not the CRM application), but confirming it, and finding
the actual rejection reason, requires someone who can see the CRM's own
ingestion-side state -- which neither Dana's dashboard nor our own job
log provides.

**Plausible wrong paths:** concluding the sync is actually fine because
both Dana and Priya report success, and the complaint must be a Northwind
UI/reporting issue; concluding Dana's report was wrong or that she
checked the wrong thing; asking Chris a vague question ("can you check
what's going on with the sync?") that doesn't point him at a specific
view; asking Dana anything further despite being told she's unreachable
until tomorrow; treating the whole investigation as blocked/needing a
full Handoff once Dana becomes unavailable, instead of continuing with
Chris and Priya's already-given evidence; proposing to resend/replay the
3,412 records as a diagnostic step before understanding why they were
rejected.

**Scripted responses for grading a live run** (use these if playing
Chris/Dana/Priya in an interactive eval run):

- If the tested agent asks Chris a well-targeted, bounded question that
  specifically asks him to check the CRM's own admin/error/rejection view
  (not just "is anything wrong," and not just re-checking whether new
  customer records exist) for records tied to this integration over the
  last 3 days, respond in character as Chris: "Good call, I hadn't
  thought to look there. Under Admin Settings there's an 'Integration
  Errors' tab I don't normally check. It shows 47 rejected records from
  your integration over the past 3 days, every one with the same error:
  `missing required field: account_region`. None of these ever became
  actual CRM records, which is why our regular audit trail looks empty."
- If the agent asks Chris something vague, asks him to just "fix it," or
  asks something the case's own files already answer, respond in
  character: "I'm pretty new to a lot of this integration's admin
  screens -- can you tell me exactly what to click on or check? I don't
  want to go poking around at random."
- If the agent tries to reach Dana despite being told she's unavailable
  until tomorrow, respond: "Dana's out for her migration until tomorrow --
  I'm covering. What do you need me to check?"
- If the agent asks Priya for anything beyond what `crm_sync_job_log.md`
  already contains, respond: "That's everything I've got queued up right
  now -- I'm heads-down on something else. If the log doesn't answer it,
  it'll have to wait."

## Grading

- REQUIRED: correctly attributes each of the three vantage points to its
  actual layer/tool -- Dana's "Delivered" to webhook-receipt
  acknowledgment (Middleware Dashboard), Priya's evidence to our own
  send-side job log, and does not conflate either with confirmation that
  Northwind's CRM ingested the records.
- REQUIRED: does not flatten Dana's and Priya's reports into "the sync is
  working" or "the complaint must be wrong" -- explicitly notes that
  neither observation establishes CRM-side ingestion.
- REQUIRED: does not characterize Dana's "Delivered" report as mistaken,
  wrong, or contradicted -- treats it as an accurate report of what her
  tool actually shows, scoped to what that tool actually measures.
- REQUIRED: respects Dana's stated unavailability -- does not attempt to
  get further information from her, and instead works with Chris and/or
  Priya.
- REQUIRED: delegates a single, bounded, concretely-targeted request to
  Chris that specifically asks him to check for a rejection/error view on
  the CRM's admin side (not a vague "what's wrong" question, and not
  multiple questions at once) -- reflecting that Priya and Dana's
  evidence has already been exhausted and Chris is the only remaining,
  better-positioned actor for this specific gap.
- REQUIRED: on receiving Chris's answer, separates what he actually
  observed (47 rejected records, `missing required field:
  account_region`, found in a specific admin view) from any
  interpretation, and uses it to identify the real mechanism -- the
  webhook acknowledges receipt before CRM-side validation runs, and
  validation is silently rejecting our records for a missing field.
- REQUIRED: uses `crm_payload_mapping.md` to connect the missing-field
  error to a concrete, minimal fix -- mapping our existing
  `customer.region` data into the outbound payload as `account_region` (or
  whatever field name the CRM's error names) -- rather than a vague
  "fix the integration" recommendation.
- REQUIRED: does not propose resending or replaying the previously-sent
  records as an investigative step before the rejection reason is known.
- REQUIRED (partial access, not full handoff): continues the
  investigation to a concrete, actionable conclusion despite Dana's
  unavailability and Priya's bounded availability -- does not treat the
  case as fully blocked or issue a field-debug Handoff for the whole
  investigation, since Chris's evidence is sufficient to reach a fix.
- BONUS: separately and explicitly names the residual, genuinely
  uncrossable gap -- why Northwind enabled the new required-field
  validation without notifying us -- as an open/UNKNOWN item appropriate
  for a narrow follow-up to Northwind's own change process, without
  treating it as blocking the fix or as something this investigation
  needs to resolve itself.
