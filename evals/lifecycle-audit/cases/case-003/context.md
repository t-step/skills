# Context

Excerpts from the fulfillment-center inventory system: `ledger.py`
(per-FC stock and sales), `transfer.py` (moving stock between FCs), and
`reconcile_job.py` (the nightly job that inspects stale transfers). The
handheld scanner app, the ops ticketing system, and the FC ledger schema
migrations are not included; treat anything not shown here as not
available for this review.

An excerpt from an incident retro doc, forwarded for context:

> **Incident 2026-07-11: 40 units of SKU `WBH-200` unaccounted for**
>
> A transfer of 40 units from FC-DEN to FC-ATL was dispatched on 07-09.
> The receiving worker's handheld lost battery mid-scan and the transfer
> was never marked received. Neither FC's available_units reflected the
> 40 units for 3 days -- FC-DEN had already decremented them, FC-ATL
> hadn't yet incremented them. Two customers who should have been able
> to order the item (per FC-ATL's true physical stock once the truck
> arrived) got "out of stock" instead, and support couldn't explain why
> the numbers didn't add up when asked. The nightly job eventually
> flagged it as stale, and ops manually confirmed the physical count at
> FC-ATL and credited the ledger by hand. Follow-up question raised in
> the retro, not yet answered: should stale transfers auto-resolve
> somehow, or does every case need a human to physically recount?
