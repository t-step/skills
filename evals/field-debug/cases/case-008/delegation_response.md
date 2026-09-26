# NetOps on-call response (received 14:35 UTC)

Ran a packet capture on checkout-bff's egress during a live failure at
14:31 UTC.

**What we saw:** SYN packets from checkout-bff toward payments-svc's host
go out but never get ACKed -- they're being dropped somewhere before
reaching payments-svc. Retransmitted SYNs show the same thing. We didn't
see any response traffic from payments-svc's side at all during these
attempts.

**Our take:** this looks like a networking issue on our end, not
something wrong with either application. Probably a firewall or
security-group rule -- my guess is a stale rule somewhere, but I haven't
had time to dig into it further, I've got other pages tonight.

One thing that might be relevant, just flagging it since it's close in
time: we pushed a routine cert-rotation change to the checkout-bff
ingress/gateway layer this morning around 13:55 UTC, which included a
rolling redeploy of the gateway pods. Unrelated to your issue as far as
I know. Deploy log and the current payments-svc security-group config
are attached if you want to dig in yourselves -- I'm out for the night
after this.
