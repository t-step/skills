# Context

A finance-tooling engineer, after a near-miss where an expense was
approved by someone who shouldn't have been able to, asks for a review of
the two Slack interactive-button handlers before they ship a similar
pattern for a third workflow:

> Both of these check the Slack request signature before doing anything,
> so I assumed they were both safe. Can you look at whether that's
> actually true for both of them, or just one?

Files in this directory are the complete evidence available about this
system -- there is nothing else to consult.
