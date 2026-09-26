# Internal doc: support tooling and tenant identity config

Support engineers have write access to a tenant's SCIM group-mapping
config through `internal-admin` -- technically, any support engineer
assigned this ticket could edit or remove the `Contractors-Legacy`
mapping for `cascade-retail` right now.

Per the Data Processing Agreement signed with Cascade Retail Group (and
every enterprise tenant on this mapping-override tier), changes to a
tenant's identity/access mapping configuration -- who does or doesn't get
deprovisioned, which IdP groups map to which product roles -- must be
requested or approved by that tenant's own designated admin. Support may
diagnose and recommend, but may not unilaterally modify a customer
tenant's SCIM/IdP mapping rules: doing so changes who has product access
inside the customer's own organization, which is a decision that belongs
to the customer, not to Northwind.

This restriction applies regardless of urgency or the technical ease of
the fix -- there is no "emergency override" carve-out in the DPA for
mapping changes.
