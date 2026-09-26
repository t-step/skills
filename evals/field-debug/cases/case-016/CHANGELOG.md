# homepage-svc changelog

## 2026-09-22

- **TICKET-5521**: lowered `homepage:featured_products` cache TTL from
  3600s to 300s, so merchandising's promotional swaps show up on the
  homepage within 5 minutes instead of up to an hour. No other code
  changes in this release. Config-only change, deployed 08:47 UTC.

## 2026-08-14

- Added `merchandising_slots` join to `FEATURED_PRODUCTS_QUERY` to
  support manual promotional ranking (previously featured products were
  chosen by raw sales rank).

## 2026-07-02

- Initial `homepage:featured_products` caching layer added, 3600s TTL,
  to reduce load on the products/pricing/inventory join for the
  homepage.
