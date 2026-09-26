# Context

Overnight batch-ops flags an incident:

> Trades booked between 22:00 and 23:00 UTC last night never showed up in
> the general ledger. `gl-dispatcher` logs show we sent 214 messages to
> the GL posting queue in that window with no send-side errors, but the
> GL system's own intake count for that hour is 0. Nothing since 23:00 UTC
> looks affected. We haven't changed `gl-dispatcher` in weeks.
>
> Sam (MQ platform admin) already got looped into this on the incident
> channel before you joined -- see `prior_mq_check.md` for what was asked
> and what came back. Sam's now heads-down on a separate, unrelated sev-1
> and says any further MQ check needs to be one specific, written request
> so they can run it between other things -- no back-and-forth.

You have the `gl-dispatcher` service's working directory and the incident
channel's existing MQ exchange (`prior_mq_check.md`). There is no live
access to any queue manager, GL system, or MQ admin beyond writing the one
request Sam asked for.
