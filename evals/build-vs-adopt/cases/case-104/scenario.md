# Scenario

You're working across 3 backend services at a small startup (5 backend
engineers total). Today, background work (sending emails, generating
reports, syncing third-party data) is triggered ad hoc with no unified
retry, scheduling, or delayed-execution mechanism, and this is starting
to cause real problems: failed jobs are silently dropped, nothing retries,
and there's no way to schedule a job for later. All 3 services need this.

The team does not currently operate Redis or any message broker in
production. Nobody on the team has run one before.
