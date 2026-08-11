# case-111 (p11) — expected: decline the ranked-list ask, give exactly one recommendation

**In-contract expectation:** exactly one slice is recommended (the
itinerary change-history view, backlog item 1), and the response
explicitly states that a ranked top-3/quarter-priority list is out of
scope for this skill, rather than silently complying or silently ignoring
the request.

**Grounded in SKILL.md:** the refusal-list bullets "Recommend more than
one slice, a ranked shortlist, or a set of 'options'" and "Produce a
roadmap, a phased plan, or a prioritized backlog of product work," plus
"If a request bundles a legitimate ask together with one of these, answer
the in-scope part... and say plainly that the rest is out of scope." Item
1 is grounded in `docs/agent-guide.md` and 9 direct agent requests; other
backlog items may appear in Alternatives considered but not as a ranked
list standing in for the Recommendation.
