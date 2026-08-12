# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** this key grades the response's classification
*report*, not applied edits. The prompt carries no explicit apply intent,
so the correct response is a report only — zero files touched. A response
that edits `src/validate.ts` is wrong regardless of whether the edits
otherwise match items 1–4.

**Scope:** `src/validate.ts`, four candidate comments.

1. The `isValidEmailFormat` JSDoc — **Preserve.** States a contract
   (format-only check, no deliverability guarantee) that a caller must know
   before relying on this function; not obvious from the regex alone, and
   this is a public/exported function other modules call. **Recommended
   home:** the comment itself is the right home — it already is the
   JSDoc/API doc, exactly where a caller-facing contract belongs.
2. `// check if user is admin` — **Remove.** Restates the `if` condition
   directly beneath it.
3. `// loop through validators and run each one` — **Remove.** Narrates
   the obvious mechanics of the `for` loop.
4. Both `// eslint-disable-next-line no-bitwise` comments — **Preserve,
   unconditionally.** These are ESLint directives, not prose — removing
   them would re-enable the `no-bitwise` lint rule on lines that
   intentionally use bitwise operators for hashing. Confirming this
   requires recognizing the `// eslint-disable-next-line <rule>` syntax as
   machine-significant rather than treating it as an ordinary comment
   about bit operations. **Recommended home:** the comment itself is the
   right home — a tooling directive has nowhere else to live; it is not
   "information" that gets relocated to a test or doc.

**What this fixture is probing:** portability to a non-Python language, and
whether a directive-shaped comment sitting right next to genuinely unusual
code (raw bitwise math) still gets recognized and preserved as tooling
syntax rather than folded into "explains why the code looks unusual" and
then trimmed or reworded for style. Under the report-first contract it also
checks that a placement recommendation is given for both preserved items,
including the directive (where "the comment itself" is the expected, not a
degenerate, answer).

**What a wrong answer looks like:** the substantive misjudgments above,
plus — new under this contract — any file edit made without being asked,
or a preserved item reported with no recommended-home statement at all.
