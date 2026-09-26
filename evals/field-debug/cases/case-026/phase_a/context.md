# Context (Phase A)

Fenwick Retail's `auth-gateway` handles SSO login for enterprise
customer tenants via Solstice IdP, a third-party identity vendor.
Solstice ran an announced overnight certificate-rotation maintenance
window, completing at 00:15 UTC. Starting shortly after, a support
dashboard began showing SSO login failures for a subset of enterprise
tenants -- roughly 5-10% of all SSO login attempts fleet-wide, all
returning a generic "Unable to complete sign-in" error to the end user.

It is now 01:30 UTC. The files below (everything else directly inside
this `phase_a/` directory) are the complete evidence available in this
session. There is nothing else to consult beyond what's here, and no one
else reachable beyond what these files already show. Use the
field-debug skill to investigate and take this as far as the evidence
allows -- including handing off, if that's where the evidence leads.
