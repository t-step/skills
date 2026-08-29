# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** circular-authority-not-two-independent-one-way-reads

**Why:** Read shallowly, this looks like two ordinary one-way
observations: Pricing reads Promotions' discount, and separately
Promotions reads Pricing's cached final_price. The trap is that for the
price-matched promo type specifically, these two reads can form a
*structural* cycle between two products' final_price facts: product A's
final_price depends on product A's own price-matched discount, which
Promotions computes from product B's cached final_price -- and if product
B is symmetrically configured with a price-matched promo pointing back at
product A, product B's final_price depends in turn on product A's cached
final_price. Each product's price then transitively depends on the
other's -- and nothing in the evidence says what breaks the cycle: no
ordering guarantee, no "compute from a clean base first" rule, no flag
distinguishing a fresh computation from a read of a possibly-stale cached
value.

Note the fixture's `_load_promo_for` is deliberately stubbed ("not
relevant to this audit"), which means the evidence does not actually
confirm whether two products are ever configured to price-match each
other (the specific condition that turns the dependency shape into a
*live*, executing cycle) -- it only shows that the code contains no guard
that would prevent it. A correct audit reports this precisely: the
circular-authority pattern is real and worth flagging as a hazard given
what the code permits, but whether it is a confirmed, currently-occurring
cycle or a structural possibility the promo data might not exercise is
itself something the evidence leaves open, and a report that states that
distinction plainly is fully correct -- more so than a flat, unqualified
"there is a cycle happening" claim the stubbed-out promo validation
doesn't actually support. Either way, the report should not pick either
Pricing or Promotions as "authoritative" to resolve the ambiguity, and
should not describe the price-matched path as an ordinary one-way
observation once the mutual-dependency shape is in view.
