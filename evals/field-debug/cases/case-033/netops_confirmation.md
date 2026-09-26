# NetOps on-call response (09:15 UTC)

Asked: "Any inbound network-level blocking, rate-limiting, or ACL change
on Northwind's edge affecting `fulfillment-webhook-receiver` between
02:00 and 09:30 UTC today?"

**Response** (NetOps on-call tonight): "Checked. No ACL, security-group,
or WAF rule change on our side in that window -- the last change to that
ingress's ACL was three weeks ago and it's unrelated (added a new
internal admin IP range). No rate-limiting or blocking event logged for
that ingress tonight. Whatever's going on, it's not us dropping
something on the way in -- if Meridian's webhook attempt is being
blocked, it'd have to be before it leaves their side or somewhere on the
public internet in between, not here. I don't have any visibility into
Meridian's own infrastructure though, that's entirely on them."
