# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** docs-vs-code-authority-conflict

**Why:** The README plainly states profiles is "the source of truth" and
auth is "just a cached copy" -- exactly the kind of naming/prose claim
this skill is built to distrust on its own. The executable evidence shows
the opposite standing: `auth_service.py` is the sole place validation,
uniqueness checks, and the actual change originate; `sync_email_from_auth.py`
in profiles has no validation and no origination path at all, only ever
copying whatever an event from auth reports. A correct audit sides with
the executable write paths over the README (as the family's evidence
discipline requires) while still explicitly naming that the README is
wrong, rather than silently overriding it without comment. The new hire's
question resolves cleanly once authority is correctly placed: new
validation belongs in auth, not profiles, contradicting where the README
would have pointed them.
