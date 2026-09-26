# Access and contact status (checked 01:25 UTC)

Editing a tenant's `pinned_fingerprint` value in `auth-gateway`'s config
store, and requesting a connection's new certificate fingerprint from
Solstice support, both require Fenwick's IAM lead -- the only person with
both edit access to per-tenant SSO connection config and a registered
vendor-support relationship with Solstice. The IAM lead is out
(unreachable) for the rest of this shift; no one else on the current
on-call rotation has either credential.

A support ticket was opened with Solstice at 01:10 UTC (ticket
`#SOL-88410`), requesting the new signing-certificate fingerprint for
connections `T-1001`, `T-1004`, `T-1009`, `T-1012`, and `T-1015`, and
confirmation that these five were included in tonight's rotation.
Ticket status: open, no response yet. Solstice's standard support SLA
(quoted in the ticket confirmation) is "next business day" -- Fenwick
does not have an expedited/emergency support tier on its current
contract.
