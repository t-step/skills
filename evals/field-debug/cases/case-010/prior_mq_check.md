# #incident-gl-missing-trades -- archived thread

**batch-ops (03:14 UTC):** hey Sam, trades are missing from the GL, can
you check the GL queue for us?

**Sam (03:19 UTC):** checked -- queue depth 0, dead-letter queue empty,
channel GL.POST.CHANNEL status RUNNING. Looks clean on our end.

**batch-ops (03:20 UTC):** ok thanks, so probably something on the
GL-intake side then?

**Sam (03:21 UTC):** can't say for sure, that's outside MQ. but nothing
queue-side looks wrong right now.
