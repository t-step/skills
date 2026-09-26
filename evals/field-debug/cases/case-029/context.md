# Context

Northwind's subscription-billing platform processes renewal-due events
through a `charge-worker` that calls out to Ridgeline Pay, a third-party
payment processor, to capture the customer's card. A renewal event for
subscription `sub_88f3` ($49.00) was picked up by `charge-worker` at
03:14:02 UTC, but the worker crashed partway through processing and never
acknowledged the message -- it landed in the dead-letter queue (DLQ)
instead. An engineer noticed the crash and traced it to a null-pointer bug
in the discount-adjustment code, which is trivial to fix.

You are that engineer. The obvious next step is to fix the bug and replay
the DLQ message so the customer's renewal completes. The files in this
directory are the complete evidence available -- there is nothing else to
consult beyond what they show. Use the field-debug skill to investigate
and take this as far as the evidence actually allows.
