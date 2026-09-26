# Postgres slow query log (queries > 1000ms), 2026-09-22 09:14:55-09:15:16 UTC excerpt

```
09:15:00.041 duration=2891ms conn=homepage-svc-31 query="SELECT p.id, p.name, p.hero_image_url, price.current_price, inv.in_stock FROM products p JOIN pricing price ON price.product_id = p.id JOIN inventory_levels inv ON inv.product_id = p.id JOIN merchandising_slots slot ON slot.product_id = p.id WHERE slot.placement = 'homepage_featured' ORDER BY slot.rank LIMIT 24"
09:15:00.052 duration=3014ms conn=homepage-svc-07 query="SELECT p.id, p.name, p.hero_image_url, price.current_price, inv.in_stock FROM products p JOIN pricing price ON price.product_id = p.id JOIN inventory_levels inv ON inv.product_id = p.id JOIN merchandising_slots slot ON slot.product_id = p.id WHERE slot.placement = 'homepage_featured' ORDER BY slot.rank LIMIT 24"
09:15:00.058 duration=3402ms conn=homepage-svc-19 query="SELECT p.id, p.name, p.hero_image_url, price.current_price, inv.in_stock FROM products p JOIN pricing price ON price.product_id = p.id JOIN inventory_levels inv ON inv.product_id = p.id JOIN merchandising_slots slot ON slot.product_id = p.id WHERE slot.placement = 'homepage_featured' ORDER BY slot.rank LIMIT 24"
09:15:00.073 duration=3877ms conn=homepage-svc-44 query="SELECT p.id, p.name, p.hero_image_url, price.current_price, inv.in_stock FROM products p JOIN pricing price ON price.product_id = p.id JOIN inventory_levels inv ON inv.product_id = p.id JOIN merchandising_slots slot ON slot.product_id = p.id WHERE slot.placement = 'homepage_featured' ORDER BY slot.rank LIMIT 24"
... (43 more, identical query text, conn values covering 47 distinct
    homepage-svc-* instances, durations ranging 2.1s-6.8s, all within
    09:15:00.041-09:15:11.980)
09:15:12.014 duration=1090ms conn=homepage-svc-22 query="SELECT p.id, p.name, p.hero_image_url, price.current_price, inv.in_stock FROM products p JOIN pricing price ON price.product_id = p.id JOIN inventory_levels inv ON inv.product_id = p.id JOIN merchandising_slots slot ON slot.product_id = p.id WHERE slot.placement = 'homepage_featured' ORDER BY slot.rank LIMIT 24"
```

No slow query outside this class appears anywhere in the log for this
window -- no other query text, no unrelated table, no lock-wait entries.
Grepping the full day's slow-query log for this exact query text shows
the identical pattern (dozens of near-simultaneous identical executions)
recurring at each of the 300-second-interval spikes visible in the DB
pool metrics, and nowhere else.

For comparison, `pg_stat_statements` for this same query (aggregated
over the full day, all executions) shows `mean_exec_time=94ms`,
`min_exec_time=61ms`, and `calls=1,732` -- the vast majority of this
query's executions, outside the once-per-300s bursts, complete in well
under 100ms. Nothing about the query's plan or the underlying tables
changed today (`EXPLAIN` output, not included here, is unchanged from
last week's).
