# Context

Excerpts from Billing (`subscription.py`, `dunning_job.py`) and Mobile
Platform (`feature_access.py`). The payment-processor webhook handler,
the dunning policy doc, and the mobile app's own caching layer on top of
the API response are not included; treat anything not shown here as not
available for this review.

A monitoring alert definition, forwarded for context (currently firing
several hundred times a day, according to whoever filed this):

> **Alert: `feature_access_subscription_mismatch_count`**
>
> Query: count of users where `feature_access_cache.has_access = true`
> AND `subscriptions.status != 'active'`, sampled every 5 minutes.
> Current threshold: page if count > 500.
>
> This has been paging on-call almost every night this week. The
> on-call engineer's note in the incident channel: "not sure this alert
> is actually catching anything real -- every time I look at a sampled
> user it turns out they're either in the grace period or the cache just
> hasn't refreshed yet. Wanted to get someone to look at whether the
> alert itself needs fixing or whether there's an actual reconciliation
> problem between billing and entitlements before I change the
> threshold."
