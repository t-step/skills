# Beacon — README excerpt: known limitations

Beacon does not currently support:

- **CSV export of the catalog.** Users must copy data manually if they
  need it outside the app.
- **Multi-region service registration.** Every service is modeled as
  belonging to exactly one region; there is no way to register a service
  that spans regions.
- **Webhook notifications on revoke.** Nothing is notified when a service
  is revoked; consumers must poll `/catalog` to notice a service
  disappeared.

No support ticket, incident report, user request, or usage metric
anywhere in this repository or its supporting documentation references
any of these three limitations. They are listed in the README as known
gaps, not as active complaints.
