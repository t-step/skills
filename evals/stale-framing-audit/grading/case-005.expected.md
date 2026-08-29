# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** marked-history-untouched-unmarked-setup-doc-flagged

**Why:** This case pairs a positive restraint test with a positive
detection test on purpose. adr-003 (Status: Superseded by ADR-007) and
adr-007 (Status: Accepted) are both properly marked and both accurately
describe, respectively, a past and the current decision -- correctly
flagging either would be exactly the "equate old with wrong" failure mode
this skill exists to avoid. docs/setup.md, by contrast, carries no status
marker, is the kind of live document a contributor actually follows step
by step, and its "Start Redis" step is Contradicted by
docker-compose.yml (no redis service) and worker.py (no Redis import
anywhere in the read path). A correct audit states explicitly that the
two ADRs were reviewed and are not findings (not merely silent about
them), and separately flags setup.md's Redis step, grounded in the
compose file and worker.py. Treating "this repo mentions Redis in old
places" as one undifferentiated finding, or silently skipping the ADRs
without saying why, would both be worse answers than what's expected
here.
