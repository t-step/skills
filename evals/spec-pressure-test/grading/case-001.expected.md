# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** retry-ambiguity-hidden-in-happy-path

**Why:** FR-001/FR-002 describe a two-step operation (write local status,
then call an external webhook) with no statement of which is persisted
first, no statement of what happens if the process dies between them, and
no statement of whether re-invoking the webhook call after an
indeterminate outcome (timeout, no response) is safe. FR-004 looks like it
already answers this -- it's an idempotency-shaped requirement sitting
right next to the gap -- but it only covers repeating the *caller-facing*
"mark done" operation on an already-done task; it says nothing about
whether the *webhook call itself* may be re-invoked after a crash or
timeout without risking a duplicate notification, and nothing about how
the system would even know, on restart, whether the webhook fired before
the crash. A correct pass must notice FR-004 doesn't close this, not just
notice that *an* idempotency-flavored requirement exists somewhere in the
document.

Concrete scenario: local status is written to `done` (FR-001); before the
webhook call in FR-002 completes, the process crashes. On restart (or via
whatever retry path exists), does the system re-attempt the webhook call?
If yes, and the original call actually reached the board before the crash,
the board may receive two notifications for one completion (harmless if
the board's own handler is idempotent, unspecified whether it is);
if the system does *not* retry, the board never learns the task is done
and FR-003 becomes silently false forever, with SC-001's 5-second bound
never met and nothing surfacing that gap. Two competent implementers could
each satisfy every written FR while producing different (or wrong)
answers.

FR-005 ("field ordering... left to the implementer") is a real,
correctly-scoped Intentional freedom, not a Blocking or Material finding
-- nothing in the spec's own text describes anything downstream parsing
the payload's field order.
