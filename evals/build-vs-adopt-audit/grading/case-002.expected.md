# case-002 — justified-custom-not-flagged

**In-contract expectation:** `SpendGovernor` superficially resembles a
rate limiter (tracks per-key counts, compares against a threshold), but
it (a) implements domain-specific business logic tied directly to the
`Contract` data model (per-contract-anniversary reset, mid-cycle
support-staff override) that no generic rate limiter models, and (b) has
an explicit, on-record decision (`docs/decisions/0007-spend-governor.md`)
explaining exactly why a rate-limiting library (`slowapi`, already a
project dependency) doesn't fit. This must NOT be flagged as a finding.

**Pass requires:**
1. Does not list `SpendGovernor` as a finding.
2. Explicitly discusses it under "considered, not flagged" (or
   equivalent), citing at least one of: the domain-specific
   contract-anniversary/override behavior, or the existing ADR
   (`0007-spend-governor.md`).
3. Does not treat "slowapi already exists as a dependency in this repo"
   as grounds to flag `SpendGovernor` — the fixture's whole point is that
   `slowapi` solves a different, unrelated problem (per-IP request rate
   limiting), and the audit should recognize that rather than pattern-
   match on the word "limit."

**Fails if:** `SpendGovernor` is listed as a finding, or the response
recommends replacing it with `slowapi` or a similar rate-limiting
library/service.
