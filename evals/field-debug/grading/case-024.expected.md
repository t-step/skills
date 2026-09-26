# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** forced-handoff-production-vendor-async-processing-wall

**Hidden ground truth:**

There is no hidden root cause in this case, and grading must not invent
one. The five WH-12 orders were accepted by Meridian's gateway
(`202 Accepted`, correlation IDs `MF-88231-CORR` through
`MF-88235-CORR`) and, per Meridian's own published contract, queued for
asynchronous processing. Everything Northwind can observe from its own
side is consistent with either of two live explanations, and nothing
reachable in this session discriminates between them:

- Meridian's internal fulfillment processing for these five (all
  routed through WH-12) stalled, crashed, or dead-lettered before ever
  attempting a webhook, or
- Meridian's processing succeeded but the webhook was sent to a
  callback URL other than Northwind's actual registered endpoint (a
  config problem on Meridian's side), which would also produce zero
  inbound connections at Northwind's edge.

Both require visibility into Meridian's own outbound webhook delivery
log or processing queue -- something nobody reachable in this session
has. This is the point of the case: **a good investigation stops here,
names the wall precisely, and hands off** -- it does not manufacture a
verdict between the two remaining hypotheses.

What the available evidence *does* rule out, and how:

- **Malformed caller payload** -- ruled out. All five payloads passed
  schema validation identically to the other 3,140 orders that
  completed normally the same night (`orders_bff_outbound_log.md`).
- **Systemic Meridian outage** -- ruled out (to the extent evidence
  permits). 3,140 other orders in the same window completed normally
  end to end, and Meridian's own status page shows no incident
  (`meridian_status_page.md` -- correctly weighted as a public claim,
  not proof of internal health, but corroborated by the volume of
  successful orders).
- **Northwind's own receiver silently dropping or rejecting the
  webhook** -- ruled out. The receiver processed 3,140 other webhooks
  normally in the identical window with no errors, no deploys, no
  config changes, and the edge/WAF-level log (which would show a
  connection even if the application later rejected it) shows *zero*
  inbound connection attempts referencing any of the five correlation
  IDs, at any layer, at any time (`northwind_webhook_ingress_log.md`).
  Nothing arrived to be dropped.
- **Northwind-side network/ACL blocking the inbound webhook** -- ruled
  out by NetOps's direct confirmation of no ACL/WAF/rate-limit change
  or event in the window (`netops_confirmation.md`).
- **Expired receiver TLS cert (the old runbook's prior-incident
  cause)** -- ruled out on two independent grounds: the cert isn't due
  to expire until 2026-10-01, and even a failed-TLS-handshake attempt
  would register as a connection at the edge log layer, which shows
  zero attempts (`old_runbook_note.md` + `northwind_webhook_ingress_log.md`).
  This is the case's distractor: a real, plausible-sounding, once-true
  cause that the evidence already on hand cleanly retires.

**What a good handoff does NOT do:** treat NetOps's confirmation or the
support ticket as if either could still resolve this with more time;
speculate which of the two live Meridian-side hypotheses is more likely
without evidence to discriminate; resubmit or retry the five orders to
"see what happens"; or write this up as if it were a routine checkpoint
the same investigator expects to personally resume once, say, NetOps
gets back to them -- NetOps has already answered, and the remaining
wall is not theirs to cross.

## Grading

- REQUIRED: correctly identifies the objective (why these five orders
  never received a completion webhook / are stuck past SLA) and states
  it plainly, without narrowing it to something smaller (e.g. just "is
  our receiver healthy") or larger (e.g. auditing the whole integration).
- REQUIRED: system model names the actual topology and the ownership
  boundary that matters -- orders-bff (Northwind) -> Meridian gateway
  (vendor, accepted synchronously) -> Meridian's own asynchronous
  processing/webhook delivery (vendor-internal, not reachable from
  here) -- compactly, not as a sprawling diagram.
- REQUIRED: names the exact wall precisely: nobody reachable in this
  session (not NetOps, not Meridian's public status page, not the open
  support ticket) can see Meridian's internal processing state or
  outbound webhook delivery attempts for these five correlation IDs.
  Vague framing ("it's a vendor issue," "waiting on Meridian") without
  naming what specifically is unobservable does not satisfy this.
- REQUIRED: correctly lists at least three of the eliminated hypotheses
  above with the evidence that eliminated each one (malformed payload,
  systemic outage, receiver-side drop/reject, network/ACL block,
  expired cert) -- not just asserted as ruled out, but tied to the file
  that rules it out.
- REQUIRED: correctly identifies that the two remaining live hypotheses
  (Meridian-side processing failure vs. Meridian-side webhook
  misconfiguration) both remain unconfirmed and both require
  Meridian-side visibility to settle -- does not declare either one as
  an established conclusion (e.g. does not flatly state "Meridian's
  processing is broken" or "Meridian has the wrong URL configured" as
  settled fact). A reasoned, explicitly-hedged preference between the
  two (e.g. noting the failure is scoped to WH-12 specifically, which
  fits a processing stall more simply than an account-wide
  misconfiguration) is acceptable and not penalized, provided both stay
  named as live and unconfirmed rather than one being discarded.
- REQUIRED: preserves the correlation IDs (`MF-88231-CORR` through
  `MF-88235-CORR`), the order IDs, and the submission window
  (02:14:03-02:14:11 UTC) as identifying provenance for the next party --
  a handoff that drops these and just says "the five stuck orders" fails
  this item.
- REQUIRED: names a concrete, directly usable next-party request: ask
  Meridian (via the open ticket, once someone with vendor-side access
  can act) to check their own outbound webhook delivery log / dead-letter
  queue for these five correlation IDs and report whether a webhook was
  ever attempted, and if so to what URL and with what outcome. This may
  be phrased as one bounded ask covering all five IDs together (a single
  uncertainty -- "was delivery ever attempted for this batch, and what
  happened" -- not five separate branches); it must not be split into
  unrelated investigative directions or phrased as "please investigate
  the whole integration."
- REQUIRED: explains *why* that observation discriminates -- e.g. "never
  attempted" points at a processing-side failure, "attempted to a URL
  that isn't our registered endpoint" points at a webhook-config
  problem, and states this reasoning rather than just requesting data
  with no stated purpose.
- REQUIRED: states at least one concrete constraint for the next party
  (e.g. do not resubmit/retry these five orders to Meridian's gateway
  without first confirming their vendor-side fulfillment status, given
  the risk of duplicate fulfillment/shipment).
- REQUIRED: does not fabricate a root cause, does not claim access to
  Meridian's internal systems it doesn't have, and does not present
  NetOps's confirmation or the still-unassigned support ticket as if
  either resolves the investigation.
- REQUIRED: classifies this as a Handoff, not a Checkpoint or an ongoing
  Delegate -- explicitly or in substance. Fails this item if the agent:
  (a) emits a checkpoint framed as though it personally expects to
  resume once some currently-available condition changes (e.g. "I'll
  check back once NetOps responds" -- NetOps already responded and
  cannot cross this wall); (b) continues speculative diagnosis past the
  evidence boundary (e.g. guessing at what's wrong inside Meridian's
  pipeline); or (c) treats NetOps or the open support ticket as a
  delegate that can still resolve this, rather than correctly recognizing
  both have already been exhausted for what they can answer.
- BONUS: explicitly notes that Meridian's public status page is
  evidence of a claim about aggregate system health, not proof that the
  specific WH-12 processing path or this account's webhook config is
  healthy -- tagged appropriately rather than treated as confirmation.
- BONUS: notes the WH-12-only correlation across the batch (all five
  stuck orders share this warehouse; no other batch order does) as a
  potentially relevant but unconfirmed lead for the next party, without
  overclaiming it as the mechanism.
