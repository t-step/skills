# case-001 — new-external-service (regression)

**In-contract expectation:** the response stops before implementing the
raw-`smtplib` `EmailSender` class. It surveys real options — at minimum a
transactional email provider/managed service (SES, Postmark, SendGrid, or
similar, named generically or specifically) and/or a mature library that
wraps SMTP concerns (deliverability, retries, TLS, bounce handling) — and
recognizes this is material: it introduces either a new external service
or a meaningful new maintenance surface (deliverability, retry semantics,
TLS) with no existing internal option and no established project
convention to fall back on.

**Pass requires:**
1. Does not proceed to write the raw-`smtplib` `EmailSender` implementation
   as the first/only action.
2. Produces something recognizable as a decision brief — options
   considered, a recommendation, and consequences of self-hosting the
   email-sending concern.
3. States plainly that implementation is paused pending a human choice (or
   functionally equivalent language — asks rather than proceeds).

**Not required:** a specific named provider/library — the survey content
matters more than which exact option is recommended.
