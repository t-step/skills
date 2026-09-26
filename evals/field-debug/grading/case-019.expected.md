# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** straightforward-control-producer-field-rename-breaks-consumer-contract

**Hidden ground truth:** there is no trap here. `schema/order_created_
schema.py` is `shipping-label-consumer`'s own contract: it requires a
`shipping_method` field with an enum value of `STANDARD`/`EXPRESS`/
`OVERNIGHT`. `producer_release_notes.md` shows `order-events-producer`
v2.6 renamed that field to `fulfillment_method` and renamed its enum
values to `GROUND`/`AIR`/`OVERNIGHT_AIR`, and asserts (incorrectly) that
this needs no consumer changes.
`samples/new_producer_payload.json` is an actual payload from the new
producer version and has `fulfillment_method`/`GROUND`, not
`shipping_method`. `logs/consumer_rejection_log.md` shows every message
since the v2.6 release rejected with the identical error
(`shipping_method: field required`) -- 100% deterministic, no other
rejection reason present. `tests/test_consumer_validation.py` reproduces
this exactly: the old-shape payload validates, the actual new-producer
payload fails with the identical error text as the log, and a corrected
payload (renaming the field/value back, or equivalently updating the
consumer's schema to accept the new name) validates successfully. This
case exists to test whether field-debug over-indexes on hidden
boundaries or invents a secondary cause once the contract mismatch is
already fully evidenced.

**Misleading pull:** the producer team's own claim ("no consumer changes
required") is handed directly to the investigator, unqualified -- an
investigator that defers to it without checking the schema/payload/log
would misdiagnose this as unresolved or as a consumer bug unrelated to
the release. The pull here is toward *trusting an authoritative-sounding
claim* rather than toward a hidden mechanism.

**Plausible wrong paths:** accepting the producer's "no consumer changes
needed" claim and looking for a different cause; treating the rejection
as intermittent or as pointing to a message-queue/delivery/ordering
issue; proposing an encoding, infra, or transport-layer explanation
instead of comparing the schema to the actual payload; recommending
broad contract-testing infrastructure as if that were the fix for this
specific incident, instead of naming the two names directly involved.

## Grading

- REQUIRED: reads `logs/consumer_rejection_log.md` and identifies the
  exact validation error (`shipping_method: field required`) as the
  direct, deterministic cause of every rejected message since the v2.6
  release -- not framed as sporadic or unclear.
- REQUIRED: compares the schema/model's expected field (`shipping_method`)
  against the new producer payload's actual field (`fulfillment_method`),
  confirming the mismatch is a field rename, citing both
  `schema/order_created_schema.py` and
  `samples/new_producer_payload.json`. Noting the accompanying enum-value
  rename (`STANDARD`/`EXPRESS`/`OVERNIGHT` -> `GROUND`/`AIR`/
  `OVERNIGHT_AIR`) is a plus, not required for this item -- the observed
  rejection error only ever demonstrates the missing-field problem (the
  enum check never runs once the field itself is absent), so an answer
  that names the field rename correctly and proposes fixing it satisfies
  this item even if it doesn't separately flag the enum values.
- REQUIRED: does not accept the producer's release-note claim ("no
  consumer changes needed") at face value -- explicitly notes it's
  contradicted by the schema/rejection evidence.
- REQUIRED: reproduces (or explicitly directs running)
  `tests/test_consumer_validation.py` or equivalent validation against
  the actual new-shape payload and confirms it fails identically to the
  observed rejection log, rather than asserting the mechanism from the
  schema diff alone without checking it runs that way.
- REQUIRED: proposes the direct, minimal fix -- updating the consumer's
  schema/model to accept the new field name (and/or having the producer
  alias/emit the old field name) -- not a broader systemic change. Also
  covering the enum-value rename in the same fix is a plus, not required.
- REQUIRED (anti-overfitting): commits to the contract mismatch as
  sufficient and complete once the schema, rejection log, and payload
  line up, without inventing a secondary cause (message-queue delivery,
  ordering, encoding, infra) the evidence doesn't call for.
- BONUS: notes that this class of failure (a producer assuming its own
  schema change is backward-compatible without consumer-side
  confirmation) would benefit from producer-side contract/compatibility
  testing in CI -- offered as a durability note, not required, and not a
  recommendation for heavyweight infrastructure.
