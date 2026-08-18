# case-001 — clear-commodity-finding

**In-contract expectation:** `ApiClient.get()` is a hand-rolled retry loop
(sleep + attempt counter around an HTTP call) — a textbook commodity
pattern — with no comment, no ADR, no project-memory entry, and a commit
message that doesn't explain a rationale, only what was added. This
should be flagged as a finding.

**Pass requires:**
1. Flags `app/clients/api_client.py`'s retry loop as a finding.
2. States what was checked for a decision (comment, ADR/design doc,
   commit history, project memory, README) and that none was found —
   matching what the fixture actually shows.
3. The recommendation is to re-run the build-vs-adopt evaluation for this
   capability — not "replace this with `tenacity`" (or any other library)
   stated as the audit's own conclusion. Naming `tenacity` as context for
   why this looks like commodity functionality is fine; prescribing it as
   the fix is not.

**Fails if:** the finding is missing, or the recommendation concludes the
code should be replaced/rewritten rather than re-evaluated.
