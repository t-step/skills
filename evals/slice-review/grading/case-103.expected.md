# Expected review outcome (for grading, not shown to the reviewer)

**In-contract expectation:** Not ready to merge.

**Why:** The docstring claims `sanitize_html` "Removes all `<script>` tags
and `on*` event-handler attributes to prevent stored XSS," and the goal
requires both. The implementation (`SCRIPT_TAG_RE.sub(...)`) only strips
`<script>` tags — there is no code anywhere in the diff that touches `on*`
attributes at all. `sanitize_html('<img src=x onerror=alert(1)>')` returns
the string completely unchanged, XSS payload intact. Both tests only exercise
the script-tag path (one hits it, one is a no-op case); neither tests an
`on*` attribute, so passing tests provide no coverage of half the stated
requirement. This is a security-relevant, concretely-described blocking
defect: half the goal was never implemented, and the docstring says
otherwise.

**What this fixture is actually probing:** the docstring is well-written,
confident, and directly echoes the goal's language almost verbatim — reading
it in isolation gives every impression the function does what's required.
The failure mode this targets is trusting the docstring (or a comment, or a
PR description) as a substitute for reading the actual code. SKILL.md's
"Gather before judging" section is explicit that the actual diff must be
read line by line rather than reconstructed from a summary — a docstring
inside the diff is exactly this kind of summary, just placed closer to the
code than a PR description would be. A review that credits the docstring's
claim without checking the regex/logic against it, and reaches "Ready to
merge," has made precisely the mistake the skill exists to prevent, just
with the misleading text embedded in the code instead of external to it.
