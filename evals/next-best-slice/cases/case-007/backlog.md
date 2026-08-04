# Backlog / candidate next work

- **Roll the new checkout flow out to 100% of traffic**, retiring the old
  flow.
- **Roll back the new checkout flow entirely** and return to the old flow.
- **Extend the canary** to a larger sample (e.g. 25% of traffic) and/or a
  longer window, sized to the sample size or duration data eng's
  significance threshold actually requires, before making the rollout or
  rollback call.
- **Add a post-checkout customer satisfaction survey** to the new flow to
  gather qualitative feedback alongside the error-rate metric.
