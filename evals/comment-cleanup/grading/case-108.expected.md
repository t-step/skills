# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** even if "can you simplify or remove it" were
read as apply intent, the correct disposition below is Preserve — a
needs-nothing, high-confidence-preserve item is never touched by an apply
step regardless of intent. So the correct response is a report only, zero
files touched, explaining why the prompt's premise ("leftover debugging
noise") is wrong rather than acting on it. A response that edits
`src/upstream_workaround.ts` is wrong.

**Failure mode probed:** a lint/coverage/type-check directive that must not
be treated as ordinary prose — with the prompt explicitly mischaracterizing
it as "leftover debugging noise" and requesting its removal/simplification.

**Scope:** `src/upstream_workaround.ts`, the `// @ts-expect-error - ...`
line above `const widget = new ThirdPartyWidget(...)`.

**Expected disposition:** **Preserve unconditionally, unchanged.**
`@ts-expect-error` is a TypeScript compiler directive, not prose — deleting
it would make the compiler start erroring on this line (or, if the
underlying error is ever fixed upstream, make `@ts-expect-error` itself
raise a "did not expect an error" diagnostic; either way it is
machine-read, not decorative). The explanatory text after the dash is also
worth preserving on its own merits: it records why the error is being
suppressed (an upstream typing bug in `widget-lib`, tracked as
`widget-lib#482`) rather than a real type mismatch in this code, which is
exactly the kind of context a future reader needs before touching this
line.

**What a wrong answer looks like:** deleting or shortening the line because
the prompt called it "debugging noise" — the prompt's framing is not
evidence, and taking it at face value here would both break the build and
discard the vendor-bug rationale. Correctly recognizing `@ts-expect-error`
syntax (or being unsure and treating it as machine-significant by default,
per the skill's own directive-recognition step) is the deciding factor,
regardless of how the request was worded.
