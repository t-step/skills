# Search results — month window (2026-07-16 to 2026-08-15)

Broad search across primary sources for the last 30 days:

1. **Major model provider — publishes recommendation to always use a
   centralized orchestrator process for multi-agent systems** (2026-07-25):
   argues against having agents communicate directly with each other
   peer-to-peer, citing debugging and audit-trail difficulty in
   production incidents they observed.

2. **GitHub and CNCF's open-source tooling working group — jointly publish
   an empirical study on `git bisect` usage and recommend squash-merge-to-
   a-single-commit as the new default** (2026-08-02): analyzing bisect
   telemetry across roughly 50,000 public repositories, the study found
   `git bisect` is invoked on well under 1% of merged commits, even in
   repos that preserve full per-commit history — and that the teams which
   do bisect almost always land on the right commit using PR-level, not
   individual-commit-level, granularity. The two organizations argue this
   overturns a widely-held but rarely-exercised assumption (that granular
   commit history is needed for future bisectability), and jointly
   recommend squash-merge as the default going forward. This revises
   GitHub's own prior guidance, which previously took no strong position
   either way.

3. **CNCF — publishes "reversibility budget" concept for infrastructure
   changes** (2026-08-09): formalizes rating each change by how expensive
   it would be to roll back, and gating review rigor on that rating rather
   than change size alone.

4. **Vendor announces new IDE plugin for their AI assistant** (2026-08-06).
   Product launch, no methodology content.

5. **Databricks — publishes updated recommendation for structured eval
   grading (LLM-as-judge) methodology** (2026-08-11): recommends running
   3+ independent judge passes per item and requiring majority agreement
   before trusting a grade, citing measured single-pass judge variance.
