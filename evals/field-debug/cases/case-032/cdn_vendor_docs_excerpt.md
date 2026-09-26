# CDN vendor docs (excerpt) -- edge cache-control overrides

By default, edge nodes honor origin `Cache-Control` headers, including
`no-store`. However, some legacy edge PoPs (a subset still running an
older cache-engine version, being phased out) support a per-PoP override
that can be configured to hold a short-lived cache of specific response
shapes regardless of origin headers, for reasons such as absorbing traffic
spikes at that specific node. Whether such an override is active for a
given PoP is configured and visible only in the CDN vendor's own edge
admin console, scoped per PoP -- it does not appear in the customer-facing
aggregate CDN dashboard, which only shows cache-hit-ratio totals across
all PoPs combined.

Vendor support can look up a specific PoP's override configuration on
request.
