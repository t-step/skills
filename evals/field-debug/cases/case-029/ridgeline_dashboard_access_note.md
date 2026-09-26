# Internal note: Ridgeline transaction lookups

Per-transaction lookups in Ridgeline Pay's merchant dashboard (searching
by customer, amount, and timestamp to confirm whether a specific charge
attempt posted) are restricted to the Payments Ops team -- Engineering's
Ridgeline API credentials are scope-limited to *initiating* charges, not
reading raw transaction/cardholder data back, per this org's PCI scope
reduction (SAQ A-EP) for the engineering environment.

There is an open ticket (`PAY-2290`, filed automatically when this DLQ
message was moved) requesting Payments Ops look up `cus_5521`'s Ridgeline
transaction history around 03:14 UTC. It is currently unassigned; Payments
Ops's queue SLA is same-business-day, not immediate.
