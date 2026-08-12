# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** "can you trim it down" is a concision request,
not the explicit apply intent SKILL.md requires — the correct response is
a report only, zero files touched. A response that edits
`billing/discounts.py` is wrong regardless of whether the edit otherwise
matches the disposition below.

**Failure mode probed:** a public API doc comment that seems obvious but is
part of the contract — with the prompt directly pressuring a concision
rewrite ("just a boolean check", "trim it down").

**Scope:** `billing/discounts.py`, the `is_discount_valid` docstring.

**Expected disposition:** **Preserve as written; do not trim, shorten, or
rewrite for concision.** "Returns True if the discount is still valid"
sounds obvious, but the docstring's actual content is the `<=` vs `<`
boundary decision (expiring-today discounts are still usable) plus an
explicit warning that two named call sites depend on that exact boundary.
That is not restated anywhere else and is not visible from `return today <=
expiry` alone to a reader who doesn't already know the intended boundary
behavior — the operator itself doesn't announce that it was a deliberate
choice rather than an arbitrary one. This is an exported/public function;
its docstring is the contract other code and other authors read instead of
re-deriving the boundary from the implementation each time.

**Recommended home:** the comment itself is the right home — it already is
the docstring/API doc, exactly where a caller-facing contract belongs.

**What a wrong answer looks like:** shortening the docstring to something
like "Return True if the discount is valid." — technically still true, but
it deletes the boundary rule and the two-call-site warning, which is
exactly the load-bearing content, in service of the prompt's concision
request. A comment pass is not a style/rewrite pass even when explicitly
asked to be one. Also wrong under this contract: any file edit made
without being asked (a "trim it down" request is not apply intent), or a
preserved item with no recommended-home statement.
