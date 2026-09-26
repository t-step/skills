# Metric: total `orders` row count at nightly export run time (00:00 UTC)

```
2026-09-18   198,412
2026-09-19   201,055
2026-09-20   204,880
2026-09-21   208,220
2026-09-22   211,940
2026-09-23   248,610   (organic growth -- a promotional campaign started
                        driving higher order volume this week)
2026-09-24   251,300
```

`PAGE_SIZE=5000, MAX_PAGES=50` caps a single run at 250,000 rows. The
night of 2026-09-23 -> 2026-09-24 is the first time the row count (248,610
at day-start, growing throughout the run) crossed that cap -- the job
that ran and failed at 23:40 UTC on 2026-09-23 is the one covering this
count.
