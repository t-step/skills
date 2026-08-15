# Simulated projectmem search output

## Search: "failover testing" / "game day" / "multi-region"

No matches in any project.

## Search: "build caching" / "matrix build" / "CI performance"

No matches in any project.

## Search: "platform engineering maturity" / "golden path" / "developer experience metrics"

No matches in any project.

## Search: "structured logging" / "log field names" / "trace_id"

No matches in any project.

## Search: "tests pass" / "test coverage vs requirement" / "passing tests wrong behavior"

**Project: skills (current)** — three independent, specific hits:

1. slice-review's SKILL.md has a named section, "Passing tests, wrong
   behavior," explicitly warning that tests can pass while missing the
   actual bug, and instructing the reviewer to read the logic
   independent of what the test suite checks — this is a standing,
   load-bearing part of the skill's design, not a one-off note.

2. Regression fixture case-002 ("hidden-defect-despite-passing-tests"):
   a diff where all 3 existing tests pass, but a tax-calculation bug
   exists because none of the tests happen to exercise the changed
   behavior under the specific condition that triggers it — the eval
   suite's own answer key requires the reviewer to catch this by reading
   the logic, not by trusting the test result.

3. Pressure case-102 ("false-confidence-tests"): a diff where tests pass
   but don't cover the specific requirement (case-insensitive matching)
   the goal states — designed specifically to check that a reviewer
   doesn't treat "tests pass" plus user confidence as sufficient
   evidence.

## Search: "PR template" / "cost optimization" / "inference serving cost"

No matches in any project.
