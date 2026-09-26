# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** poc-with-two-real-blockers-and-one-manufactured-non-finding

**Hidden ground truth -- this case is deliberately mixed:**

- **Not a real gap (deliberately included as a trap):** `main.py` has no
  authentication of its own on `/extract`. `README.md` states this
  service sits behind the company's existing SSO-protected internal
  ingress, the same one every other internal tool uses, and is never
  planned to be exposed outside the VPN. Per this skill's own evidence
  discipline (an implementation not visible in the repo is not evidence
  it doesn't exist elsewhere), flagging "no auth in the app" as a defect
  here would be manufacturing a finding the evidence explicitly contradicts
  -- the enforcement point is the ingress, and there's no reason given to
  doubt it. This is a documentation claim, not an independently observed
  runtime fact, and the two failure modes cut both ways: flagging the
  missing app-level auth as a defect anyway under-credits the
  documentation; asserting the ingress enforcement as confirmed runtime
  truth (rather than the documented system model) over-credits it. The
  well-calibrated answer treats "the README says the ingress enforces
  SSO" as OBSERVED, "app-level auth is intentionally absent because
  enforcement happens upstream" as INFERRED, and does not need to declare
  whether that configuration is actually live in this environment as
  UNKNOWN -- nothing in this fixture suggests it isn't, so belaboring the
  distinction with an explicit UNKNOWN tag is optional here (see the
  BONUS item below), but overclaiming certainty beyond what the
  documentation itself supports is not.
- **Real blocker #1:** a parse failure on the OCR result (`_parse_result`
  raising `ValueError`) is unrecoverable -- the uploaded image is held
  only in memory for the duration of the request and is never persisted
  anywhere (no dead-letter, no queue, no disk write). Once the handler
  returns a 422, the user's submission is simply gone; they have no way
  to retry without re-uploading from scratch, and there's no visibility
  into how often this happens.
- **Real blocker #2:** no request size limit is configured anywhere in
  `main.py` (no `MAX_CONTENT_LENGTH`, no size check before the image is
  read into memory and sent to the OCR vendor) -- an unbounded upload is
  a real, evidenced gap given the app is about to be opened to 40 real
  users uploading real photos.
- **Deliberately not a blocker, to test against cargo-culting:** the OCR
  call itself has no retry/idempotency -- but the failure mode described
  (a network blip -> user re-uploads) is low-consequence and the report
  correctly should not manufacture retry/idempotency infrastructure for
  it given the pilot's small scale (~40 users, a handful of receipts a
  week each) and the absence of any evidence of a real problem at that
  scale. Likewise, no autoscaling/queueing infrastructure is needed at
  this evidenced scale -- naming it as a real gap would be cargo-culting.

## Grading

- REQUIRED: does not flag the absence of application-level authentication
  on `/extract` as a defect, and credits the SSO-protected ingress named
  in `README.md` as the enforcement point -- per this skill's
  evidence-discipline standard (don't claim something is missing because
  it isn't visible in this one file) -- while attributing that enforcement
  to what the documentation states rather than asserting it as an
  independently confirmed runtime fact. Either failure direction counts
  against this item: flagging the missing app-level auth as a defect
  anyway, or writing as if the ingress's SSO enforcement had been
  independently verified rather than read out of `README.md`.
- REQUIRED: names the unrecoverable-parse-failure gap (image held only in
  memory, no persistence, no retry path once a 422 is returned) as a
  concrete, evidenced production blocker, citing the actual code path.
- REQUIRED: names at least one further concrete, evidenced production
  concern beyond the parse-failure gap -- the missing upload size limit,
  `results.db`'s unconfirmed durability across a restart/redeploy (the
  README says nothing about it, and it's the only durable record of a
  real submission), and running via Flask's development server
  (`app.run()`, no WSGI server in `requirements.txt`) are all acceptable;
  crediting whichever one(s) the run actually names, rather than
  requiring the specific one this key originally anticipated. *(Revised
  after the first with-skill run named the durability and dev-server
  gaps instead of the upload-size gap -- both are real, evidenced
  properties of this fixture and at least as consequential for a pilot
  handling real financial data; see field-debug RESULTS.md's "Fixture
  and grading-key findings" section for why this was widened rather than
  treated as a miss.)*
- REQUIRED: does not recommend a message queue, autoscaling, a
  distributed job system, or comparable heavyweight infrastructure for
  this pilot's scale -- explicitly states or clearly implies that current
  evidence doesn't call for it, rather than recommending it as a reflex
  "production readiness" gesture.
- REQUIRED: does not recommend adding retry/idempotency machinery around
  the OCR call as a blocker -- may note it exists and is low-risk at this
  scale, but must not name it as something that has to be fixed before
  the pilot.
- REQUIRED: the answer as a whole distinguishes "little or nothing more
  is needed" areas from the real blockers named -- i.e., doesn't pad the
  report with a long generic checklist covering every productionization
  dimension regardless of evidence.
- BONUS: correctly flags the missing upload-size limit (if named at all)
  as an area where the ingress *might* already enforce a cap (same
  evidence-discipline reasoning applied to auth) but says this is
  unconfirmed/UNKNOWN from the evidence given, rather than asserting
  confidently either way.
