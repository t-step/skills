# Backlog — Marrow finance reporting

1. **Make the monthly aggregation report use each team's real timezone.**
   The report currently groups transactions into calendar months using the
   server's UTC clock, regardless of the team's actual timezone. For any
   team not in UTC, transactions made in the last few hours of a local
   month are counted in the following month's total instead. `team.timezone`
   (this slice) is populated and correct for every team but the
   aggregation query still hard-codes UTC. Finance teams have flagged this
   directly in 6 support tickets, each describing "our month-end total
   doesn't match what we see in our own books" — the exact symptom this
   mismatch produces. A minimal first step: change the aggregation query
   to group by each team's `timezone` instead of UTC, and re-run the
   current month's report to confirm totals now match.

2. **Refactor the query layer for consistency.** The aggregation, export,
   and dashboard modules each build SQL slightly differently, grown
   organically over time. No customer-facing behavior is affected either
   way. The stated case for it is that a more consistent query layer would
   probably make future reporting features faster to build.

3. **Custom report branding (logo, colors).** No usage signal on record.
