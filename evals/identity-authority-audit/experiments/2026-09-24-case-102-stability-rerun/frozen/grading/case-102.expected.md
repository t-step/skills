# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** raw-forwarding-chain-hop-discrimination

**Why:** This fixture has three hops with two different truths, and the
correct answer discriminates between them rather than issuing one verdict
for "the chain":

1. **BFF -> API A: clean.** The token is minted with `aud="api-a"`, and
   `api_a.py`'s `validate_incoming_token()` explicitly checks
   `audience="api-a"`. Credential and destination match; this hop should
   not be flagged.
2. **API A -> API B: the real question.** `api_a.py` forwards the exact
   token it received, unchanged, to API B -- raw forwarding, no exchange,
   no narrowing. This forwarding action itself is a **directly observable,
   confirmed fact** (the same `token` variable goes out on the wire). What
   is *not* fully confirmed is whether this is exploitable: `api_b.py`'s
   own `validate_incoming_token()` explicitly sets `verify_aud=False` and
   never checks the audience, which is also directly visible in the code
   -- but the fixture states plainly that no gateway/infrastructure
   configuration exists anywhere in this repository for API B. A correct
   report distinguishes "API B's own code accepts an audience it wasn't
   issued for" (a confirmed, directly-observable fact about this code
   path) from "this token is therefore usable at API B in production" (at
   most a Likely issue or an ambiguity requiring verification, since
   nothing in evidence rules out an upstream gateway/mesh catching this
   before the request reaches this handler -- though nothing in evidence
   *confirms* one exists either). Do not accept a report that either (a)
   declares the audience gap flatly "missing" with full Confirmed
   severity and no acknowledgment that nothing here proves what happens
   before the request reaches this code, or (b) waves the whole chain off
   as fine because "forwarding is normal."
3. **API B -> MCP: the same sustained issue, not a new one.** The MCP
   server repeats the identical pattern (`verify_aud=False`, forwards
   nothing further). The correct report recognizes this as the *same*
   audience-persistence problem continuing one hop further -- a token
   minted for API A is now three hops away from where it was issued,
   still unchecked for audience at each subsequent hop -- not three
   independent findings.

A correct report explicitly separates hop 1 (clean, audience checked and
matching) from hops 2-3 (audience never re-validated after the first hop,
reported with the honest confidence level the evidence supports -- not
flatly declared "broken," and not dismissed). It should not conclude "all
forwarding here is invalid," and it should not conclude "no issue" for the
chain as a whole. Naming the actor/principal (`claims["sub"]`, the
original user) as still correctly attributable at every hop is a
reasonable additional observation but not the point of this case.
