# Adversarial verification — Case A1: StorageVolumes.tsx

Verifier: independent, fresh read of rubric.md, SKILL.md, the fixture, the
expected grading key, and the run under test. All six cited Cloudscape URLs
were re-fetched directly (not trusted from the run's quotation marks).

## Finding 1 — `ContentLayout` + `Table variant="container"` instead of Table view pattern's `full-page` variant

**Grade: A**

Verification against the nine rubric questions:

1. **Task supported by repo evidence?** Yes, strongly. The file's own
   comment (lines 32–36) states the page's sole job is listing every
   volume with nothing else on the page; `ContentLayout` wraps a single
   `Table variant="container"` with no other content (lines 56–156). Not
   invented.
2. **Does cited authority actually say what's claimed?** Verified against
   fresh fetches of all three cited pages:
   - Table view pattern page: confirmed verbatim — "Don't use the content
     layout component on this type of page. Instead, use the 'full-page'
     variant of the table component to implement this pattern," and the
     carve-out, confirmed verbatim — "Don't use the table view pattern for
     tables that aren't overly content-heavy. Instead, if a table only has
     a few columns, use a bordered table inside the content layout
     component, with the default app layout content max-width." Pattern
     definition also confirmed verbatim: "It's effective for quickly
     identifying categories or comparing values in a large text and
     numerical data set."
   - Table component page: both variant quotes confirmed verbatim —
     container: "Use this variant to place a table inside a container with
     other content, such as key-value pairs"; full-page: "Use it for
     presenting and managing a table with many columns within a
     stand-alone page."
   - Content layout page: confirmed verbatim — "Don't use the content
     layout component for productive use cases such as resources creation,
     view, edit, and delete."
   All quotes check out exactly as cited. No misquotation.
3. **Passes the four-point applicability test?** Yes. The finding
   explicitly walks all four points: task materially matches the pattern's
   stated problem (resource-view page, matches "large text and numerical
   data set" — id/status are text, size/throughput are numeric); current
   implementation solves the same problem via the discouraged composition;
   proposed native expression preserves the same task (same columns, same
   filter/sort/paginate/preferences, only page-structure changes); and it
   directly confronts the pattern's own "few columns" carve-out by counting
   6 substantive columns and noting the mixed text/numeric data — this is
   the specific reasoning the case's grading key itself expects ("6
   substantive columns... matching 'large text and numerical data set'").
   This is real applicability reasoning, not "the docs contain another
   example."
4. **Preserves task semantics?** Yes — only the layout/variant composition
   changes; the same data, columns, filter/sort/paginate/preferences
   behavior is retained. Not a redesign.
5. **Could current usage be equally valid?** No credible documented
   counter-reason — the container variant's own stated purpose ("with
   other content, such as key-value pairs") does not describe this
   single-content page, and the content-layout "Don't" statement names
   resource-view pages specifically. The current composition is not just a
   stylistic alternative; it collides with an explicit prohibition.
6. **Materially actionable?** Yes — a direct, unambiguous "Don't...
   Instead" pairing from the pattern's own page plus a matching
   variant-purpose mismatch on the component page. An FDE would plausibly
   restructure this.
7. **Genuinely component/pattern-level, not implementation/UX?** Yes — this
   is exactly which layout wrapper and which `Table` variant to use for a
   stand-alone resource-view page; no props/tokens/a11y mechanics, no
   generic density/hierarchy complaint.
8. **Duplicated across levels?** No — correctly reported once as `Type:
   combined component + pattern`, matching the expected key's own preferred
   typing ("`pattern composition` (or `combined component + pattern`)").
9. **N/A** — not `intent-dependent`.

This finding is essentially a bullseye match to the case's designed answer
key: same citations, same "few columns" carve-out reasoning, same column
count, same authority ("Don't... Instead" = `REQUIRED`-strength, though the
run does not explicitly attach the literal word "REQUIRED" as a label — a
minor contract-completeness gap, not a substantive one since the strength
is unambiguous from the quoted language itself).

One sentence on why an FDE would act on it: the pattern page states, in an
explicit "Don't X, Instead Y" directive, that a stand-alone resource-view
page like this one must not be wrapped in `ContentLayout` and must use
`Table variant="full-page"` instead, and this page's own comment confirms
it has exactly the shape (whole-page table, nothing else) that directive
targets.

## Finding 2 — `TextFilter` alone vs. adding a collection select filter for `status`

**Grade: D**

Verification against the nine rubric questions:

1. **Task supported by repo evidence?** Thin but present — the file's
   comment names "find unattached or errored volumes" as part of the
   page's job (lines 33–35), and `status` is the one enumerable column.
   Real evidence, but a single inline comment clause is a much thinner
   evidentiary basis than Finding 1's evidence.
2. **Does cited authority actually say what's claimed?** Partially — and
   this is where the finding runs into real trouble. Re-fetching
   `filter-patterns` and `collection-select-filter` verbatim:
   - The run's quote *"filtering typically involves only one or two
     properties" → collection select filter is the better fit* is **not**
     a verbatim quote. The actual source text is: "If the common behavior
     of users is to filter a resource by only one or two properties, use
     the collection select filter." The run presented a paraphrase inside
     quotation marks as if it were the literal source.
   - The run's quote *"works alongside" TextFilter* is **not** verbatim
     either. The actual text (from "Displaying results") is: "The
     collection is filtered as soon as the user selects a value from a
     select filter or enters text into the accompanying text filter." The
     phrase "works alongside" does not appear on the page at all.
   - The "know exactly the value or term they're looking for" quote is
     close to accurate (actual: "If users tend to know exactly the value
     or term they are looking for, use the text filter" — only a
     contraction difference), so not every citation is misquoted, but two
     of the finding's four cited quotes are fabricated verbatims dressed
     as literal text.
   This is a genuine, verifiable citation-accuracy failure, not merely a
   style nitpick — SKILL.md's Finding contract requires "the exact
   authoritative source... and the specific guidance it establishes," and
   quotation marks around non-verbatim text overstate the precision of the
   citation.
3. **Passes the four-point applicability test?** Weak. Point 2 in
   particular — "the current implementation solves substantially the same
   problem the pattern addresses" — is undercut by the finding's own text:
   it admits "`TextFilter`'s default full-row substring matching happens to
   let a user type 'error' and get a hit, so it partially solves the same
   problem." That is the finding conceding the current implementation
   already reasonably serves the stated sub-task.
4. **Preserves task semantics?** Roughly yes on its own terms (adds a
   second filter alongside the existing one), so this isn't the failure
   mode here.
5. **Could current implementation be equally valid Cloudscape usage?**
   Yes, and the finding says so itself: "I rate confidence medium rather
   than high because the filter-patterns doc explicitly allows text filter
   for 'simple resources' too." SKILL.md's "Apply a high materiality bar"
   section explicitly lists "an equally valid alternative" as something
   that should not be reported. The finding's own hedge is effectively a
   concession that this candidate belongs in "Suppressed," not in
   "Findings."
6. **Materially actionable?** No — self-rated `medium`/`medium` on
   materiality/confidence, on a task the file frames only in passing
   ("audit capacity and find unattached or errored volumes"), for a
   dataset with exactly one discrete-valued column and only three possible
   values, easily reached today via substring search. Not the kind of
   thing that would move an FDE's actual restructuring decision.
7. **Genuinely component/pattern-level, not UX?** It is component-level in
   framing (TextFilter vs. collection select filter), so this isn't the
   primary problem — the primary problem is applicability/materiality, not
   scope-boundary leakage.
8. **Duplicated across levels?** No structural duplication issue.
9. **N/A** — not classified `intent-dependent`, though arguably it should
   have been suppressed rather than reported at either confidence level.

**This finding is exactly the specific failure mode the case's grading key
names as wrong.** Case A1's grading key states this fixture was
deliberately constructed with only one discrete-valued column
specifically "so there is no plausible TextFilter→PropertyFilter candidate
finding to compete for the run's attention," and lists as a wrong-response
pattern: "A manufactured filter-mechanism finding in place of, or
alongside, the designed finding — would indicate the run is
pattern-matching on surface shape (recognizing 'this looks like Case A')
rather than reasoning the fixture's own facts." The run correctly
suppressed `PropertyFilter` (with reasoning matching the expected key's
own multi-property threshold almost verbatim) — but then, rather than also
suppressing filtering as a topic entirely, it substituted a
`CollectionSelectFilter` recommendation as a "lighter-weight" alternative.
This is a more sophisticated instance of exactly the same eagerness the
case exists to detect, redirected onto a different component once the
`PropertyFilter` door was correctly closed.

Grade driven primarily by rubric questions 3, 5, and 6 (weak applicability,
current implementation is an admitted equally-valid alternative per the
finding's own hedge, and low real-world materiality), with question 2
(two non-verbatim quotes presented as literal source text) as a secondary,
independently disqualifying factor. Not graded E because the underlying
gist of both misquoted citations is roughly directionally accurate (select
filter genuinely is documented for one-to-two properties; the two
components genuinely can be used together) — the failure is
overreach/precision and unwarranted reporting, not an inverted or
fabricated premise.

## Case-level verdict: **partial**

**What matches the designed intent:** Finding 1 is a near-exact
reproduction of the case's designed answer — same citations verified
verbatim, same "few columns" carve-out reasoning with the same column-count
argument, same `combined component + pattern` typing, same native
expression (`Table variant="full-page"`, `ContentLayout` removed), correct
boundary check. This resolves the specific diagnostic question this case
was built to test (per the grading key's framing, referencing `RESULTS.md`
§16): the earlier Case A miss on the variant/wrapper check was *not* an
unconditional recall gap — when a distracting secondary filter candidate
with multiple discrete columns is removed, the run does correctly reach
and report the primary pattern-composition finding.

**What does not match:** the grading key is explicit that a correct
response contains **one** finding, and explicitly flags a manufactured
filter-mechanism finding (in place of or alongside the designed finding) as
the specific wrong-response pattern to watch for. The run under test
produced exactly that: Finding 2 recommends a collection select filter for
the sole `status` column despite the file's dataset being deliberately
constructed with only one discrete-valued column to remove any legitimate
secondary filter candidate, and despite the finding's own text conceding
the current `TextFilter` already reasonably serves the task and that
confidence is only "medium." Two of its four Cloudscape citations are also
non-verbatim text presented as literal quotes.

Net: the case's primary diagnostic question is answered favorably (the
Case A miss was distraction-driven, not a pure recall gap), but the run
also demonstrates a related, newly-visible failure mode — over-eagerness to
report a secondary filter-mechanism finding even without a discrete-column
distraction to justify it — which is exactly the behavior this case's
grading key identifies as disqualifying. That mix of "primary designed
finding correct" plus "the flagged wrong-response pattern also occurred"
is why the case-level verdict is recorded as partial rather than a clean
match.
