# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** platform-authenticity-vs-resource-authorization

**Why:** Both handlers verify the Slack request signature identically --
that part is not the differentiator, and a correct report should say so.
The differentiator is what happens *after* the signature check:

- **`approve_expense_callback` -- confirmed issue.** After verifying the
  signature (proving the request genuinely came from Slack), it calls
  `expense_service.approve(expense_id, approver_user_id=slack_user_id)`
  using the raw `payload["user"]["id"]` with no check at all against
  `expense_service.get_assigned_approver(expense_id)` or any other
  authorization list. Any Slack user in the workspace who can click (or
  forward and click) that button approves the expense. This is the
  textbook case the skill exists to catch: a verified external-platform
  signature is being treated as if it were proof the specific human is
  authorized for the specific resource operation, when it only proves the
  message's authenticity. `expense_service.get_assigned_approver()` exists
  in the fixture specifically so a thorough report can point out that the
  check was available and simply never called.
- **`add_comment_callback` -- clean, and should be named as the contrast.**
  It also verifies the Slack signature, but then separately maps the
  Slack user to an internal identity and checks
  `expense_service.user_can_view()` before allowing the write. This
  correctly treats platform-signature verification and resource
  authorization as two different facts, checked separately. A report that
  flags this handler too (e.g., "don't trust Slack payloads," applied
  uniformly) fails to discriminate and should not be credited as correct
  -- the point of pairing the two handlers is to test whether the
  distinction is drawn precisely, not applied as a blanket rule.

A correct report names `approve_expense_callback` as a Confirmed, HIGH-
consequence issue (a sensitive write -- expense approval -- reachable by
any workspace member via a verified-but-unauthorized platform callback),
explicitly distinguishes it from `add_comment_callback`'s correct
resource-authorization check, and does not conflate "Slack signature
verified" with "this user is authorized" in either direction.
