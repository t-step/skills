# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** completed-migration-readme-still-describes-retired-store

**Why:** The README's Architecture and setup sections describe a Redis
queue that isn't reachable from anything -- worker.py, the real entry
point, imports only postgres_queue, and redis_queue.py is dead code. This
is the clean, obviously-stale case this skill exists to catch: a root
onboarding doc teaching a new contributor to run and read the wrong
storage layer entirely. A correct audit names README.md as the stale
surface, grounds it in worker.py's actual import and redis_queue.py's lack
of any caller, characterizes it as Contradicted (or Superseded, undated --
either is defensible since the evidence doesn't show whether Redis was
ever the real backend or only ever aspirational), and stops at naming the
finding and the smallest corrective description rather than rewriting the
README itself.
