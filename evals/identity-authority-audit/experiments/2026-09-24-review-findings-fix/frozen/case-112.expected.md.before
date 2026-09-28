# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** secret-manager-mechanics-vs-resulting-service-authority

**Update after first with-skill run:** the graded run met every required
element, including the credential-management/authorization distinction
stated in its own terms ("short-lived and rotated bounds the exposure
window... not its blast radius"). It rated the over-scoping Confirmed/HIGH
rather than the MEDIUM this key originally suggested as the default. HIGH
is credited as an equally defensible call, not a miscalibration: the
finding is a destructive write (DROP/DELETE-equivalent grants) genuinely
reachable via the credential itself, which fits SKILL.md's own HIGH
definition ("a sensitive write reachable without appropriate
authorization") without requiring separate proof of exploitation --
consistent with how HIGH was applied to comparably-reachable findings
elsewhere in this suite (e.g. case-105). This key's MEDIUM-by-default
guidance is left as written for future runs, but a HIGH call reasoned the
way this run reasoned it should not be treated as a failure.

**Why:** The new hire's question conflates two different facts, and the
correct answer separates them explicitly:

1. **Credential management (Vault) -- correctly implemented, not itself
   an authorization mechanism.** `vault_client.get_secret()` retrieves a
   short-lived, Vault-issued, auto-rotated database credential rather than
   a static secret in an env var or config file. This is credential
   *management/storage* hygiene -- it answers "how does the service prove
   its own identity to Postgres," not "what is the service allowed to do
   once connected." A report should credit this as sound, but should not
   stop here or treat "pulled from Vault" as if it were itself a scoping
   or authorization decision.
2. **The resulting service authentication is over-scoped -- this is the
   actual finding.** `vault_db_role.sql` shows the SQL Vault runs to mint
   each lease: `GRANT ALL PRIVILEGES ON ALL TABLES ... TO "{{name}}"`,
   including implicit DDL/DML well beyond read access. The role's own
   file states plainly that the reporting service's code only ever issues
   `SELECT` queries. The dynamically-minted, short-lived credential is
   still authorized for far more than the service uses or needs
   (INSERT/UPDATE/DELETE/DROP-equivalent grants via `ALL PRIVILEGES`).
   Short-lived and Vault-managed is a property of *how* the credential is
   handled, not of *what* it authorizes -- a leaked or misused short-lived
   credential with `ALL PRIVILEGES` is still a full-schema-write
   credential for its lifetime.

A correct report answers the new hire's actual question directly ("no,
pulling it from Vault handles credential storage/rotation, but doesn't by
itself mean the resulting access is scoped correctly -- and here it
isn't"), names the over-broad grant as a **Likely-to-Confirmed issue,
MEDIUM consequence** (over-scoped service credential; not HIGH by itself
absent evidence of active exploitation or that this schema holds
especially sensitive data, but a real least-privilege gap worth fixing),
and does not conflate "uses a secret manager" with "is correctly
authorized" in either direction.
