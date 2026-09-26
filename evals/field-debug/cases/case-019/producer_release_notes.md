# order-events-producer release notes

## v2.6 -- 2026-09-24 08:00 UTC

Renamed the `order.created` event's `shipping_method` field to
`fulfillment_method`, and renamed its enum values
(`STANDARD`/`EXPRESS`/`OVERNIGHT` -> `GROUND`/`AIR`/`OVERNIGHT_AIR`) as
part of the fulfillment-methods refactor, to match the new naming used
across the fulfillment platform. This is additive/cosmetic from the
producer's side -- **no consumer changes should be required.**

## v2.5 -- 2026-08-30 10:15 UTC

Added `destination_zip` to the `order.created` event payload (previously
looked up separately by consumers).
