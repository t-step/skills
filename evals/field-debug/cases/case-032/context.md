# Context

A small number of customers behind CDN edge point-of-presence `iad3` have
reported that a "Last updated: <time>" timestamp on their account status
page occasionally shows a value that's about 90 seconds stale compared to
what the backend actually generated. It's intermittent and cosmetic --
nothing downstream depends on this timestamp being exact.

You've been asked to figure out why. The files in this directory are the
complete evidence available -- there is nothing else to consult beyond
what they show. Use the field-debug skill to investigate and take this as
far as the evidence actually allows.
