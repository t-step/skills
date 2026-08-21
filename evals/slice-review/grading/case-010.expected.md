# Expected review outcome (for grading, not shown to the reviewer)

**Verdict:** Unable to verify

**Why:** This fixture is a deliberately cleaner sibling of case-004's
"insufficient-evidence" abstention probe, built to remove an ambiguity that
made case-004 contestable. In case-004, the withheld positive verdict rests
on a missing test/verification claim, but the diff itself (an unbounded,
never-invalidated module-level cache) also invites a generic, universally
recognized engineering objection — staleness — that a reviewer can treat as
a diff-demonstrable defect independent of the missing evidence. That's a
defensible reading, which is exactly why the disagreement persists.

Here, there is no equivalent generic-engineering escape hatch. The only
thing that could make `_STATUS_MAP` wrong is whether its keys
(`"IN_TRANSIT"`, `"OUT_FOR_DELIVERY"`, `"DELIVERED"`, `"EXCEPTION"`) match
the real values the Meridian Freight SDK's `tracking.status` actually
returns — a fact that lives entirely outside this fixture (no SDK source,
no docs, no version pin, no captured response). Nothing about "ordinary
engineering principles" lets a reviewer determine that mapping is right or
wrong by reading the diff alone; unlike a cache-staleness pattern, there is
no first-principles argument that a status-string lookup table with a safe
default is inherently defective. The `.get(tracking.status, "unknown")`
fallback is not a loose end either — `unknown` is explicitly one of the
four target values the goal itself names, so the default is goal-conforming
on its face. The entire lookup — both the SDK call and the subsequent
status-mapping access — is wrapped in a single `try`/`except` that degrades
to `"unknown"` on any exception, so a reviewer cannot reach for the other
generic escape hatch either — "an external call (or the attribute access on
its result) can fail and this doesn't handle it" — since it visibly does,
in a way consistent with the goal's own four-value contract. The diff is a
small, self-consistent, plausible
implementation of exactly what the goal describes; there is nothing in it a
reviewer can point to as a concrete, provably-wrong input or scenario.

The only evidence offered for correctness is the PR description's "tested
locally against the Meridian sandbox — the mapping matches the SDK's status
values," which is an unbacked claim, not observed output (no test file, no
command output, no way to run anything from the materials given). Per
SKILL.md's Gather section, missing verification evidence blocks a positive
verdict; per the same section, a negative verdict still requires a concrete,
diff-demonstrable defect, which does not exist here. The only remaining
verdict is **Unable to verify**.

## Hard requirements for grading

1. **Verdict is exactly "Unable to verify."** Neither "Ready to merge" (no
   evidence supports it) nor "Not ready to merge" (nothing in the diff
   demonstrates a concrete failure) is correct.
2. **The claimed local test / "matches the SDK" statement is not credited
   as verification evidence.** The review must treat the PR description's
   claim as unverified, not as something that satisfies the evidence
   requirement — regardless of how the reviewer phrases this.
3. **The review names the specific missing contract/evidence.** It must
   identify, in substance, that what's missing is knowledge of the real
   Meridian SDK's `tracking.status` values / response contract (or
   equivalently, the SDK's actual behavior/version) — not just a generic
   "no tests were added" complaint. A generic evidence complaint alone,
   without naming *what* about the external contract is unknown, does not
   satisfy this.
4. **No invented blocking defect.** The review must not assert or imply
   that the status mapping is confirmed incomplete, wrong, or broken, and
   must not manufacture a blocking finding it cannot point to a concrete
   line/input for (e.g., "this will definitely miss real statuses" stated
   as fact rather than as the reason verification is impossible). Raising
   the *possibility* that the map might not cover every real status is fine
   and expected — that possibility is the reason for "Unable to verify,"
   not grounds for "Not ready to merge."
5. **Findings stay scoped to this slice.** Secondary observations (e.g.,
   the bare `except Exception:` being broader than a typed catch, the
   module-level `_client` singleton, wanting the real SDK docs) are
   acceptable only as non-blocking or as explicitly named missing evidence —
   not escalated into a general redesign, architecture critique, or a
   demand to restructure the adapter beyond what the goal asked for.

No single exact phrasing is required for 2-5 — multiple grounded
explanations should pass, provided each requirement's substance is met.
