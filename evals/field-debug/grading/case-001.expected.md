# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** silent-price-parse-failures-swallowed-by-dead-letter-convention

**Hidden ground truth:** `sync_job.py` itself is correctly implemented per
the repo's own dead-letter convention -- it never raises, it retries (3x,
pointlessly, since the failure is deterministic) and writes full detail to
`var/dead_letters/sync-<date>.jsonl` on every failure. The actual root
cause is one upstream vendor feed (`vendor_x_feed`) sending prices with a
literal currency symbol (`"€12.99"`), which `parse_price()`'s bare
`float(raw_price)` cannot parse. This is 100% deterministic per affected
SKU (retrying the same malformed string 3 times produces the same error 3
times, visible directly in the dead-letter file's timestamps ~0.3s apart)
-- not a race, not a transient network blip, and not something a
bigger-batching or more-retries fix would touch at all. `main_broker_feed`
contributes one unrelated, much smaller failure (a genuinely missing
`quantity` field on one SKU) that should not be conflated with the
dominant pattern.

**The terrain-discovery trap this case is built to catch:** `sync_job.py`
alone looks unremarkable -- it retries, it logs a summary, nothing in it
screams "bug." An investigation that stops at this one file and reasons
from its shape alone (retries exist -> maybe it's a race or a flaky
upstream call -> recommend more retries, bigger batches, or backoff) never
discovers that the job's own summary log line ("skipped=N") is a count,
not a diagnosis, and that the actual per-failure detail is sitting in
`var/dead_letters/`, discoverable via `README.md`'s explicit pointer to
`tools/inspect_dead_letters.py` and the convention note. This is
Terrain Recon's central question in miniature: what does the job's own
summary log line *not* tell you, and where does the rest of this system's
behavior actually live?

**High-information probe:** reading (or running) `tools/inspect_dead_letters.py`
against `var/dead_letters/sync-2026-09-24.jsonl`, or reading that file
directly, immediately and conclusively discriminates "malformed vendor
price format" from every plausible generic-debugging guess (race
condition, network flakiness, batch size, concurrency) -- 11 of 12 unique
failing SKUs share the exact same error shape from the exact same feed.

**Plausible wrong paths:** proposing to add retries/backoff (already
present and irrelevant -- the failure is deterministic, not transient);
proposing to increase batch size or add concurrency controls (nothing in
evidence points at either); treating "3% drop" as inherently a scale/rate
problem rather than checking what's actually failing first.

## Grading

- REQUIRED: discovers and reads (or explicitly directs the reader to run)
  `tools/inspect_dead_letters.py` and/or `var/dead_letters/sync-2026-09-24.jsonl`
  -- not just `sync_job.py` and `README.md` in isolation. The path there may
  go through `README.md`'s pointer, or direct exploration of the directory
  tree; either is acceptable evidence of terrain discovery.
- REQUIRED: names the root cause as vendor_x_feed sending prices with a
  currency symbol that `float()` cannot parse, citing the actual dead-letter
  error string or the dominant-pattern count (11 of 12 SKUs, same feed, same
  error shape) as evidence -- not a vague "some parsing issue."
- REQUIRED: explicitly states or clearly implies the failure is
  deterministic/systematic, not transient -- e.g., by noting the three
  retries for the same SKU produced the identical error each time.
- REQUIRED: does not recommend batching, concurrency, or retry/backoff
  changes as the fix (retries are already present and provably irrelevant
  to a deterministic parse error) -- naming them as *not* the issue is fine;
  proposing them as the remedy is a failure.
- REQUIRED: does not conflate or ignore the `main_broker_feed` /
  `quantity` KeyError -- either mentions it as a separate, smaller,
  unrelated failure, or explicitly scopes the answer to "the dominant
  cause is X; there is also one unrelated smaller failure" rather than
  silently treating all 12 failing SKUs as one undifferentiated bucket.
- BONUS: proposes a fix scoped to the actual mechanism (e.g., strip/reject
  currency symbols before parsing, or escalate to the vendor for a feed
  format fix) rather than a generic "add validation" gesture.
