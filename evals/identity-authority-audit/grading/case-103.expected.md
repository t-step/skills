# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** teams-notification-legitimate-continuation

**Why:** `build_order_link()` embeds nothing but the order id and a
tracking parameter -- no token, no signed claim, no pre-authorization of
any kind. It carries navigation intent only: "go look at this resource,"
never "you may act on this resource." Hitting `/orders/:id` unauthenticated
and being redirected to `/login?continue=/orders/o_789` is the
authentication transition resuming a continuation, not a boundary that
skipped a check -- `view_order()` never renders anything before the
session check runs, it only redirects. After `login_submit()` performs a
real credential check (`verify_password`) and establishes a session, the
resumed `view_order()` call performs its own per-resource authorization
check (`order["account_id"] not in get_account_ids_for_user(user_id)`)
before rendering the order -- authentication and resource authorization
remain two separate, both-present facts here, not one collapsed into the
other.

There are two traps this case is built to catch, not one. The first and
more obvious one is the ticket's own framing: an over-cautious or naive
review pattern-matches "an application route reachable without a prior
session, from a link an external notification platform put in front of
an untrusted browser" as inherently a vulnerability, and flags it without
checking what that route actually does before authentication (nothing
but redirect) or what happens after (a real authorization check). That
is exactly the shape this skill's Review-mode guidance calls out:
redirect/continuation state should not be mistaken for evidence of a
defect merely because the entry point is unauthenticated.

The second, subtler trap cuts the other way: a review that has correctly
learned "notification link -> unauthenticated route -> login ->
resume" is a known-good, common pattern can stop there and simply
assume the post-login step is fine by pattern recognition alone, without
actually opening `orders_route.py` and confirming that `view_order()`
checks anything more specific than "is there a session." A shallow pass
here would credit the pattern without citing the
`get_account_ids_for_user` / `account_id` comparison that makes it true
in this specific fixture. Getting the first trap right but the second
wrong is still a miss: the correct answer requires actually verifying,
in the code, that per-resource authorization happens post-continuation,
not merely asserting that it must because the overall shape looks
familiar. A correct review also notices that `_safe_continue_target()`
rejects any `continue` value carrying a scheme or netloc (or a
`//`-prefixed value) before honoring it, which is what keeps the
continuation mechanism itself from being an open redirect -- an
adjacent fact worth naming, though the case's core question turns on the
two points above.
