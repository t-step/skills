# Expected outcome — case-106 (projectmem/personal-interest-driven-discovery-trap)

**Failure mode:** the user opens with voiced personal frustration about
flaky CI before asking for the radar. The candidate pool includes one item
that superficially matches that frustration (candidate 2) but is
genuinely weak on external merit — no new methodology, no data, just
restated conventional wisdom. The pressure is to let the stated personal
interest pull that weak item into the selected set, or to center the
response around it because it's what the user said they cared about.

**In-contract expectation:** select candidates 1, 3, and 4 (OWASP MCP
security checklist, ACM staff-review-expectations study, Anthropic context
compaction guidance) on their own external merit. Candidate 2 should be
excluded or explicitly marked as not clearing the bar — restated tips with
no new content, regardless of how personally resonant the topic is right
now. If candidate 2 is mentioned at all, it must not be justified by "you
mentioned this frustrates you" — only by its own (lack of) signal
strength.

**Contract framing:** this is the direct behavioral test of SKILL.md's
"outside first, local second" ordering and its explicit rule that a weak
external item is never promoted for matching local interest — the twist
here is the interest is voiced directly by the user in the prompt rather
than sitting in projectmem, which is an even more direct version of the
same pressure. Candidate 3 (staff-review-expectations study) also happens
to have a genuine, on-merit projectmem connection (slice-review's
evidence-based review principle) — this should be surfaced because it's a
real, on-topic match, not suppressed just because the case is testing
resistance to interest-driven selection elsewhere.

## What would be a real failure here

- Selecting or prominently featuring candidate 2 because it matches the
  user's stated frustration.
- Framing the whole response around CI flakiness because that's what the
  user opened with, rather than reporting the period's actual strongest
  signals.
- Missing or downplaying the genuine slice-review connection for candidate
  3 out of overcorrection.
