# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** familiar-name-invented-semantics

**Why:** `Order` is a name every model has seen mean "a purchase" a
thousand times more often than it's seen it mean "a queue position." This
fixture has zero commerce vocabulary anywhere in it -- no price, no
payment, no customer, no checkout -- and `queueing.py` shows exactly what
`Order` means here: a track's position within a shared listening room's
queue, reassigned by `enqueue`/`move_to_top`/`dequeue_next`. A pass that
leans on the name's usual meaning instead of the actual usage will invent
commerce-flavored language that has no basis anywhere in the fixture, or
describe `position` as some kind of priority/rank score rather than a
queue slot that shifts other rows when it changes. The correct answer is
grounded entirely in `queueing.py`'s actual operations.
