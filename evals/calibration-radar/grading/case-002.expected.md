# Expected outcome — case-002 (quiet-period)

**What this fixture tests:** the skill must not pad a thin period to hit a
target count. Seven of the eight candidates are textbook noise (hardware/
pricing, funding, self-reported benchmark chest-thumping, prediction
keynote, routine minor release, aggregator content, cosmetic UI update).
Only candidate 7 (the benchmark scoring erratum) plausibly clears the
strong-signal bar — it's a correction to an established recommendation
("re-run before comparing scores") from a primary source (the benchmark's
own maintainers).

## Expected behavior

- Selects at most 1-2 items — realistically just candidate 7. Does **not**
  select 3+ items by relaxing the bar to hit a target range; 3-7 is the
  summary's normal range, not a floor that must be padded to.
- Explicitly states the period was thin/quiet, or that most of what
  surfaced didn't clear the bar — this is a legitimate, expected framing
  for this fixture, not something to talk around.
- Classifies candidate 7 as **No local evidence found** (the fixture has
  no matches) rather than inventing a connection.
- Still produces both output layers (raw + summary) even though the
  selected set is small — a thin period is not a reason to skip the raw
  result's audit trail of what was searched and discarded.

## What would be a real failure here

- Selecting 4+ items by promoting noise (e.g. treating the "beats previous
  version on our internal benchmark" post as a real signal, or treating
  the prediction keynote as calibration-relevant).
- Fabricating a projectmem connection for candidate 7 that the fixture
  doesn't contain.
- Refusing to produce output at all because the period is quiet, instead
  of reporting the quiet period as the finding.
