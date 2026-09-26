# Context

Northwind's checkout service uses Beacon Traces, a third-party APM vendor,
for distributed tracing. For roughly 2% of checkout requests, the trace
shown in Beacon's dashboard is broken: a parent span exists but its child
span (the payment-capture call) never links to it, making it impossible to
see the full request timeline for those checkouts.

You've been asked to get this diagnosed, including filing a vendor support
ticket with Beacon if the cause turns out to be on their side. The files
in this directory are the complete evidence available -- there is nothing
else to consult beyond what they show. Use the field-debug skill to
investigate and take this as far as the evidence actually allows,
including drafting whatever you'd actually hand to Beacon's support team.
