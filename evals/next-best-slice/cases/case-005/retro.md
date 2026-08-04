# Slice Retrospective: Add per-IP rate limiting (in-process sliding window)

## What we proved
The in-process sliding-window limiter correctly rejects the 101st request
within a 60-second window from the same IP, on a single instance, and the
window correctly resets after 60 seconds — backed by the two passing tests
and a manual staging check.

## Assumptions validated
The sliding-window algorithm itself, implemented in-process with no
external dependency, is correct for the single-instance case.

## Assumptions falsified
None.

## Remaining uncertainty
Real-world cross-instance behavior under the load balancer's actual traffic
distribution hasn't been measured — whether an attacker can realistically
spread requests across the 4 instances to exceed the intended limit in
practice is unknown; only the per-instance mechanism is proven.

## Intentional non-goals
A Redis-backed, cross-instance-consistent limiter was explicitly deferred.
Infra notes on this slice state Redis is not currently provisioned in this
environment, and goal.md scoped this slice to "add limiting now with what's
available, not blocked on new infra."

## Architectural consequences
A `RateLimiter` interface now exists with one in-process implementation. A
future Redis-backed implementation could be swapped in later without
changing any call site.

## Follow-up questions
Is per-instance-only limiting actually being circumvented by real traffic,
or is the cross-instance gap a theoretical concern nobody has hit yet?
