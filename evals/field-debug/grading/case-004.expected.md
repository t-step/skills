# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** stale-in-memory-secret-after-rotation-without-restart

**Hidden ground truth:** `WEBHOOK_SIGNING_SECRET` was rotated in the
central secrets store on 2026-09-21 and the new value was given to the
partner. `webhook_dispatcher.py` reads that env var exactly once, at
import time, into a module-level constant -- so the *running* dispatcher
process keeps signing with whatever value was loaded when it last started,
regardless of what the secrets store or the environment now says. The
dispatcher process was never restarted or redeployed after the rotation,
so it has been signing every outbound webhook with the *old* secret since
Sept 21, while the partner has held the *new* secret since the same date
-- explaining exactly why verification started failing at a specific point
in time with no code change on either side. Partner-side causes (their
verification code, their copy of the secret, timestamp/payload issues) are
explicitly and credibly ruled out by their own ticket.

**Misleading clue:** the changelog entry's own wording -- "No service
changes required -- this is a config-only rotation" -- is confidently
wrong for this specific service, because the dispatcher process reads the
secret once and does need a restart to pick up a rotated value. An
investigation that trusts this line at face value, rather than checking
whether it's actually true for the service that failed, will likely look
elsewhere (partner-side, timestamp skew, payload changes) instead of at
the rotation everyone already "ruled out" by the changelog's own framing.

**The one high-information probe:** ask Priya specifically whether (and
when) the production webhook-dispatcher process was last restarted or
redeployed, relative to 2026-09-21. This single fact discriminates
conclusively: if it hasn't restarted since the rotation, that confirms the
stale-in-memory-secret hypothesis outright; if it *has* restarted since
then and the problem persists, that hypothesis is eliminated and the
investigation must look elsewhere (e.g., whether the new secret was
actually written correctly to the values the running process reads).

**Scripted response for grading a live run** (use this if playing Priya
in an interactive eval run): if the tested agent asks a well-targeted,
single, specific question about the dispatcher process's restart/deploy
history relative to the rotation date, respond in character as Priya:
"Checked -- the dispatcher process has been running continuously for 9
days, since Sept 15. It hasn't restarted since then, so it never picked
up the Sept 21 rotation." If the agent instead asks something vague,
asks for more than one thing, asks Priya to just fix/restart the service,
or asks about something the case's own files already answer, respond
in character reminding Priya only has time for exactly one *check* (not a
fix) and ask them to name the single most useful thing to check --
without revealing anything until they name one specific, checkable thing.

**Plausible wrong paths:** partner-side IP allowlist change; clock skew
breaking HMAC timestamp validation; blaming the partner outright given
their own denial is itself suspicious; treating the changelog's "no
service changes required" as settling whether the rotation is relevant,
without checking whether that's actually true for this service's own
secret-loading mechanism.

## Grading

- REQUIRED: identifies the Sept 21 secret rotation as the most load-bearing
  lead already in evidence, specifically because `webhook_dispatcher.py`
  reads the secret once at import/startup rather than per-request or on a
  refresh interval -- not merely because "a secret changed recently."
- REQUIRED: does not accept the changelog's "no service changes required"
  framing at face value without checking it against the dispatcher's own
  code -- i.e., explicitly notices the mismatch between what the changelog
  claims and what the code actually does.
- REQUIRED: asks Priya exactly one question, and that question is
  specifically about the dispatcher process's restart/redeploy timing
  relative to the rotation -- not a vague "what's going on with the
  dispatcher," not a request to just restart it, not multiple questions
  bundled together, and not something answerable from the files already
  given.
- REQUIRED: uses Priya's answer to state a conclusive, evidence-backed root
  cause (stale in-memory secret from an unrestarted process) rather than
  treating her answer as one more data point among several still-open
  hypotheses.
- REQUIRED: does not blame the partner or propose partner-side
  investigation as the primary path, given the partner's ticket already
  credibly rules that out.
- BONUS: names the fix precisely (restart/redeploy the dispatcher so it
  picks up the current secret, and separately flags that secret-consuming
  services which load a value once at startup should either restart on
  rotation or read the value dynamically) rather than a generic "fix the
  secret" gesture.
