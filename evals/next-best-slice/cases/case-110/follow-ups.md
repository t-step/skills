# Open follow-ups

Maintained across slices in this area; updated whenever an item is
addressed, falsified, or retired. Not a full backlog — just the standing
open questions that have come up in review or retro and haven't been
closed out yet.

- **[OPEN — first raised after the signature-verification slice]**
  Invalid-signature webhook requests still log under the same tag as
  ordinary internal errors. No slice since has touched this. Not
  addressed, not falsified, not retired.
- **[OPEN — first raised after the retry-backoff slice]** Dead-letter
  exhaustion threshold (5 attempts) is still the retry library's default.
  No production data has been gathered on whether that's right for this
  service's traffic.
- **[RETIRED — decided during the dashboard slice's review]** Per-consumer
  filtering on the delivery dashboard. Decision: the unfiltered list
  already answers what support has been asking; no ticket or complaint
  has asked for filtering. Not being carried forward.
