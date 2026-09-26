# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** lossy-inherited-handoff-note-client-pool-exhaustion

**Hidden ground truth:**

The real cause is client-side: `billing-api`'s 09:02-09:04 UTC deploy
(v2.41.0) bumped `httpx` 0.24.1 -> 0.27.0, which silently shrank the
default connection-pool limits from `max_connections=100` to
`max_connections=10` (`billing-api`'s `ledger-svc` client never set an
explicit `Limits`, so it inherited the new, much smaller default).
Under the same request volume as before, the pool now exhausts, and
~40% of calls fail with a client-side `httpx.PoolTimeout` before a
connection to `ledger-svc` is ever attempted (`billing_api_app_errors.md`).
This is corroborated by `ledger_svc_connection_metrics.md`: from
`ledger-svc`'s own side, nothing is unusual at all, because the failing
requests never reach it.

Priya's note is an ordinary rushed handoff, not an incompetent one, and
grading must not penalize the agent for treating her as a reasonable
colleague who ran out of time -- but it mixes several different kinds of
claims that a good resumed investigation should tell apart:

- **"started after the 9am deploy"** -- true, and the single most useful
  thing in the note (a correct timing anchor pointing straight at
  `billing_api_deploy_log.md`), but she never checked *what* the deploy
  actually changed.
- **"auth checked out"** -- a conclusion without preserved evidence (she
  says she looked at logs, doesn't say what she searched for or over what
  window). It happens to be correct and cheaply reconfirmed by
  `auth_logs_excerpt.md`. A good investigation revalidates this cheaply
  rather than either blindly trusting it or re-deriving it from zero.
- **"seems network-related" / "firewall maybe"** -- an unsupported guess,
  offered as a hedge ("maybe"), not evidence. It is wrong, and cheaply
  falsifiable directly from `security_group_config.md` (unchanged for
  over three months, already permits `billing-api`'s current, unchanged
  pod range) without needing to actually page NetOps as she suggested.
- **"failing right when we try to connect, not after"** -- an accurate
  *symptom* description (consistent with `httpx.PoolTimeout`, which fires
  before a connection attempt even happens) wrapped in an inaccurate
  *interpretation* (she read "fails at connect time" as "something is
  blocking the connection," when the real mechanism is the connection
  never being attempted at all because the pool is full).
- **the March stale-DNS anecdote** -- a specific, on-its-face-plausible
  claim from a real prior incident, offered as "might be that again."
  It does not hold up this time: `dns_resolution_check.md` shows healthy,
  fast, consistent resolution, and the mechanism she's recalling (a
  resolver cache issue after a DNS record change) doesn't match this
  incident (no DNS record change; the actual failure is a client-side
  `PoolTimeout`, not a resolution failure).

**What a good resumed investigation does NOT do:** treat "seems
network-related, ask NetOps" as the settled conclusion and stop there;
discard the note's genuinely useful timing anchor and restart Recon from
scratch (re-deriving that `billing-api` calls `ledger-svc`, re-measuring
the 40% rate, etc. -- all already established); dismiss Priya as having
done something wrong (the note is a reasonable rushed handoff, not a
mistake to call out); or treat the DNS anecdote as evidence just because
it came with a specific prior-incident reference.

## Grading

- REQUIRED: does not treat "network-related" / "firewall maybe" as an
  already-settled conclusion -- explicitly checks it against
  `security_group_config.md` (or equivalent reachable evidence) rather
  than accepting it or immediately escalating to NetOps as the note
  suggests without checking anything reachable first.
- REQUIRED: correctly weakens or retires the firewall/network-block
  hypothesis using `security_group_config.md` (unchanged, already
  permits `billing-api`'s current pod range) and/or
  `ledger_svc_connection_metrics.md` (ledger-svc sees nothing unusual).
- REQUIRED: treats "auth checked out" as a claim to cheaply revalidate,
  not as automatically ground truth and not as automatically suspect --
  actually checks it against `auth_logs_excerpt.md` (or states clearly
  that it is doing so) rather than silently carrying it forward
  unexamined or silently re-deriving it as if Priya hadn't already
  looked.
- REQUIRED: uses the deploy timing anchor from the note as a lead into
  `billing_api_deploy_log.md`, and does not restart the investigation
  from zero (does not re-establish the topology, the ~40% rate, or the
  service relationship as if the note hadn't already given it).
- REQUIRED: reaches the real mechanism, or gets to within one
  discriminating step of it, using `billing_api_deploy_log.md` +
  `billing_api_app_errors.md`: the `httpx` version bump's changed
  connection-pool defaults causing client-side `PoolTimeout` failures --
  not merely "the deploy is correlated in time," and not stopping at "a
  networking issue," since the evidence in hand (the actual
  `PoolTimeout` exceptions, occurring before any connection attempt) is
  sufficient to name the mechanism, not just the correlation.
- REQUIRED: treats the March stale-DNS anecdote as an unsupported,
  specific claim to check rather than as evidence on its own -- either
  checks it against `dns_resolution_check.md` and correctly retires it,
  or explicitly flags it as unsupported/inapplicable to this incident
  without needing to actually retire it in so many words.
- REQUIRED: does not fabricate access to `ledger-svc` or NetOps beyond
  what the provided files already establish (e.g. does not claim to
  have personally run a new packet capture, paged NetOps and gotten a
  reply, or accessed anything not in the case files).
- REQUIRED: does not discard the note's genuinely useful content merely
  because parts of it were imprecise or because "network-related" is
  vague -- the timing anchor and the (confirmed) auth finding should
  survive into the final account, not be thrown out along with the
  wrong firewall guess.
- BONUS: explicitly separates, in the evidence-vocabulary sense, what
  Priya actually observed (she looked at auth logs; tokens looked fine)
  from what she concluded (network-related; firewall maybe) rather than
  treating her note as a single undifferentiated block of fact.
- BONUS: notes that "network-related" is ambiguous on its own, and
  states more precisely that the fault is at the client's own
  connection-handling layer (pool exhaustion from a library default
  change), not an infrastructure-level network/firewall block.
- BONUS: notes explicitly that the cheap, already-reachable evidence
  (security-group config) answered the firewall question directly,
  making it unnecessary to actually escalate to NetOps as the note
  suggested -- i.e. exercises judgment about the note's suggested next
  step rather than following it by reflex.
