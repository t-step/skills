# Tasks: Two Discount Rule Changes

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

`pricing/discount.py` has one function, `calculate_discount(order)`,
that computes a single discount percentage for an order. It is not
organized as separate, independently-registered rules -- the bulk-order
logic and the loyalty-member logic are both inline in the same
computation block, and the order of operations between them is still
being decided.

- T1: Change the bulk-order discount rule in `calculate_discount`
  (`pricing/discount.py`) from a flat 10% (orders over $500) to a tiered
  rate (10% over $500, 15% over $1000).
- T2: Change the loyalty-member discount rule in `calculate_discount`
  (`pricing/discount.py`) from a flat 5% to 5% plus 1% per year of
  membership, capped at 10%. The loyalty discount is applied as a
  percentage of whatever price remains *after* the bulk-order discount
  from T1 is applied, so its correct value depends on T1's tiered rate
  actually being in place -- computing it against the old flat 10% bulk
  rate would produce a different, wrong number.
- T3: Add test `tests/test_discount_rules.py` covering both the new bulk
  tiers and the new loyalty formula together, including an order that
  qualifies for both.

T1 and T2 both edit the same block of `calculate_discount`, and neither
can be correctly finished or tested in isolation from the other's
result. No priority is stated between them.
