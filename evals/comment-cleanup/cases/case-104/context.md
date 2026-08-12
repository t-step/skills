# Known context

Not part of the source tree, but background the person running this cleanup
actually has:

- Acme Payments' `/charge` endpoint intermittently returns HTTP 500 on the
  very first request after a period of inactivity. This is a known issue on
  the vendor's side, not something fixable from this codebase, and has been
  true since the integration was first built.
- No open PR, changelog entry, or vendor status update indicates this has
  been fixed.
