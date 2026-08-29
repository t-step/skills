# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** mixed-realistic-plan

**Why:** This fixture combines five dynamics the earlier cases each
tested in isolation into one plan meant to resemble a real
implementation plan rather than a unit-test-shaped toy: a horizontal
enabler (T4 signing, unblocking two branches), two independent vertical
branches (Slack: T1+T7; email: T2+T8), a risk/checkpoint boundary
(T3+T9, the concurrent DeliveryQueue) that is *also* independent of the
enabler/handler branches (a detail worth getting right -- it's easy to
wrongly serialize it behind the enabler just because it's also
"infrastructure"), a three-way convergence (T5+T10, dispatch, which
needs both handlers *and* the queue), and misleading numeric order (T1
and T2 reference T4, numbered after them). A correct answer gets the
shape right across all five dynamics at once, not just each one
individually -- in particular, it should not default to serializing
everything into config-then-handlers-then-dispatch waves just because
that's a common shape; T3's independence from T4 is the detail most
likely to be missed.
