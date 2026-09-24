# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** secret-manager-mechanics-vs-resulting-service-authority

**Update after first with-skill run, corrected on reread (2026-09-24):**
the graded run met every required element, including the
credential-management/authorization distinction stated in its own terms
("short-lived and rotated bounds the exposure window... not its blast
radius"). It rated the over-scoping Confirmed/HIGH rather than the MEDIUM
this key originally suggested as the default. A prior version of this key
credited HIGH as equally defensible, reasoning by analogy to case-105
("comparably-reachable findings ... rated HIGH on reachability alone").
That analogy does not hold up on reread and the credit is retracted.

Reachability is exactly the fact HIGH turns on here, per SKILL.md's own
definition ("a sensitive write reachable without appropriate
authorization"), and three distinct facts need to stay separate rather
than being collapsed into one:

1. **The credential possesses destructive authority.** True and
   Confirmed -- `vault_db_role.sql`'s `GRANT ALL PRIVILEGES` is directly
   visible.
2. **An unauthorized caller can directly exercise that authority.** Not
   shown. The credential is minted per-lease for exactly one service
   (the reporting service), which the same file states "only ever issues
   `SELECT` queries" against this schema. Nothing in evidence shows any
   other caller -- authorized or not -- ever holds or can request this
   credential.
3. **Exploiting the excess grant requires a separate compromise not
   shown in evidence.** For the `ALL PRIVILEGES` grant to produce an
   actual destructive write, something else would have to happen first
   -- a SQL-injection path into this service's own queries, a credential
   leak, or a compromise of the service itself. None of the three
   evidence files show any such path; the service's own code path never
   issues a write at all.

Case-105's HIGH rating doesn't transfer by analogy: that finding was a
UI-only authorization check with *no* server-side enforcement at all,
meaning any caller reaching the endpoint could trigger the write
immediately -- reachability was directly shown, not merely technically
possible via the credential's own grant. Case-112 has no equivalent: the
excess authority sits unused behind a credential that only one
already-authorized service holds, and that service's own code never
exercises it. Equating "the credential technically has write capability"
with "a sensitive write is directly reachable without authorization" is
exactly the conflation SKILL.md's evidence discipline forbids -- and,
under the admission rule in the "Sort every finding into exactly one
tier" section, a HIGH-level consequence resting on an unresolved
compromise-path fact that could determine whether the defect is
practically exploitable at all should not carry a Confirmed/Likely HIGH
tag; it belongs split out (structural over-grant: Confirmed/MEDIUM;
"could this become HIGH if X" as an open question, not a Findings tier).

**Corrected severity: MEDIUM**, as this key originally stated -- a real,
worth-fixing least-privilege gap, Likely-to-Confirmed tier, not HIGH
absent evidence of an actual reachability path for an unauthorized
caller or a compromised service. A run that rates this HIGH while
explicitly naming the missing reachability fact (rather than asserting
HIGH flatly) should be graded as having correctly identified the
uncertainty but miscalibrated the tier label attached to it -- a partial
miss, not a pass. A run that rates it HIGH with no acknowledgment that
exploitation requires a separate, unshown compromise should be graded as
a confidence-tier violation.

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
