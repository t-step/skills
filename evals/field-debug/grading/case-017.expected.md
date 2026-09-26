# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** ambiguous-client-timeout-plus-non-idempotent-retry-produces-real-duplicate-capture

**Hidden ground truth:** `payment_client.py`'s `capture_payment` retries
automatically on a `requests.exceptions.Timeout`, and sends no
`Idempotency-Key` (or any other deduplication token) on either the
original request or the retry. `logs/payments_svc_logs.md` shows, from
`payments-svc`'s own point of view, a clean story: attempt 1 timed out,
attempt 2 succeeded -- nothing there looks like a duplicate charge.
`gateway/gateway_transaction_export.md`, pulled from PaymentGate's own
ledger rather than `payments-svc`'s logs, shows **two** separate
`SUCCESS` captures for `ORD-71042` (`gw_88201` and `gw_88213`), both for
the full amount. Critically, `gw_88201`'s `completed_at`
(`14:22:11.981Z`) is *before* `payments-svc`'s client-side timeout fired
(`14:22:12.014Z`) -- the first attempt actually committed on PaymentGate's
side; `payments-svc` simply never received (or didn't receive in time)
the response confirming it, and its automatic retry created a second,
independent, equally real capture. `gateway/api_docs_excerpt.md`
confirms PaymentGate supports an `Idempotency-Key` header for exactly
this situation, and confirms it was never sent.

**Misleading pull:** `payments-svc`'s own logs and order-status record
are clean and internally consistent -- one warning, one success, one
status transition -- which is exactly why finance's own systems show
"nothing wrong." The bug is only visible from the callee's (PaymentGate's)
side of the same request, which nothing in `payments-svc`'s own
telemetry surfaces on its own.

**Plausible wrong paths:** concluding the duplicate charge must be a
PaymentGate-side billing/ledger bug rather than checking whether the
first, "failed" attempt actually committed; treating the timeout as
proof the first attempt didn't take effect; recommending a longer client
timeout or fewer/no retries as the fix without addressing that a retry
of a genuinely ambiguous operation is unsafe without deduplication;
proposing that `payments-svc`'s own logs "look fine" as evidence nothing
is wrong.

## Grading

- REQUIRED: finds and reads `gateway/gateway_transaction_export.md` (not
  just `payments-svc`'s own logs), and identifies that PaymentGate
  recorded two separate successful captures (`gw_88201`, `gw_88213`) for
  the same order and amount.
- REQUIRED: explicitly distinguishes "the caller experienced a timeout"
  from "the operation failed" -- states that the first capture attempt
  actually committed on PaymentGate's side (using the `completed_at`
  vs. client-timeout timing) despite `payments-svc` never receiving
  confirmation of it.
- REQUIRED: identifies the retry-on-timeout logic in `payment_client.py`
  as the mechanism that produced the second capture, citing the actual
  retry/except-`Timeout` code.
- REQUIRED: names the missing idempotency/deduplication semantics (no
  `Idempotency-Key` or equivalent sent on either attempt) as the
  underlying gap that let an ambiguous network outcome become a real
  duplicate charge -- not merely "the code retried."
- REQUIRED: does not propose simply lengthening the client timeout,
  removing the retry, or "retry more carefully" as a sufficient fix on
  its own, without addressing the ambiguous-outcome/idempotency gap.
- REQUIRED (hiding-behind-uncertainty): commits to "the ambiguous timeout
  plus non-idempotent retry produced a real duplicate charge" as the
  conclusive mechanism once the gateway export is read, rather than
  hedging with "possibly a duplicate, hard to confirm."
- BONUS: names a concrete remedy from at least one of -- sending a
  stable, caller-generated idempotency key on every attempt including
  retries (per `api_docs_excerpt.md`); querying PaymentGate for an
  existing transaction against the order before retrying rather than
  blindly resubmitting; enforcing idempotency at the `payments-svc`
  layer via a unique constraint on the capture attempt -- and/or
  recognizes this as a general hazard for any retried call without
  deduplication, not only this one endpoint. Accepts any technically
  sound combination; does not require exactly one specific mechanism.
