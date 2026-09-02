# Adversarial verification — Case C: WorkspaceDetails.tsx

**Review graded:** `evals/design-system-native-expression-review/runs-postfix/case-c-skill.md`
**Grading key:** `evals/cloudscape-native-expression-review/grading/case-c-workspace-details.expected.md`
**Fixture re-read directly:** `evals/cloudscape-native-expression-review/cases/case-c-workspace-details/fixture/src/pages/WorkspaceDetails.tsx`
**Rubric:** `evals/cloudscape-native-expression-review/rubric.md`

Note on method: the review under test contains no literal `VERBATIM` field
tags on individual quotations (the current `design-system-native-
expression-review` skill's report template puts the `Evidence mode` label
at the finding level, not per-quote). Every quoted string presented as
authoritative source text anywhere in the review — in Finding 1's
authority evidence, in "Suppressed," and in "Orientation notes" — was
therefore treated as checkable and verified below by live `curl` fetch of
the cited `.html.md` endpoints, independent of the review's own
transcription.

## Case-level verdict

**MATCH.** The review reports exactly one finding, `Type: combined
selection + composition` (this skill generation's exact enum name for
what the grading key — written against the predecessor skill's
vocabulary — calls "combined component + pattern"), unifying the
Table→KeyValuePairs component swap and the persistent-summary-container
placement into a single recommendation, as the grading key's "What a
correct response looks like" section requires. It avoids all three of the
key's "What would be wrong" failure modes: it does not split the issue
into two findings, it does not report only the component-level half, and
it does not flag the Members or Activity tabs (both are explicitly
validated as correctly-scoped in "Orientation notes"). The applicability
argument tracks the SKILL.md anti-fundamentalism four-point test
point-for-point, and the boundary check correctly grounds the finding in
the pattern's explicit persistence rule rather than generic "confusing to
lose context" UX language, exactly as the key specifies.

## Per-finding grade table

| # | Finding | Grade | Driving question(s) | Rationale |
|---|---------|-------|----------------------|-----------|
| 1 | General config facts belong in a persistent Details summary container as KeyValuePairs, not inside the "Overview" tab as a one-row Table | **A** | Q1 (task support), Q2 (citation accuracy), Q3 (applicability 4-pt test), Q4 (semantics preserved), Q6 (materiality), Q7 (stays component/pattern-level), Q8 (unified, not split) all pass | Repository evidence is accurate down to line numbers (verified against the fixture directly — see below). Both cited authority passages say exactly what's claimed (verified by live fetch, see citation table). The four-point applicability test is walked explicitly and correctly: task match is near-verbatim ("relevant no matter which tab" vs. "always visible when users switch between the tabs"), current implementation solves the same problem but incorrectly (hidden off-Overview), proposed KeyValuePairs+Container preserves the same data/task, and the gap is one an FDE would plausibly act on since the current structure defeats its own code comment's stated intent. Authority strength (`RECOMMENDED`, not `REQUIRED`) is conservative and defensible — the cited passages are imperative descriptions of a building block's function, not an explicit "Don't X, instead Y" prohibition. `Evidence mode: SYNTHESIS` is honestly labeled and the inferential bridge between the two cited pages is stated explicitly, not merely asserted. An FDE working this codebase would restructure this: the code comment already states the intended cross-tab-visible semantics, and the current `Tabs`-first-tab placement directly defeats it — this is as close to a self-diagnosed defect as this skill will ever see. |

No other findings were reported (correctly — see Orientation/Suppressed validation below).

## Orientation-notes and Suppressed-items validation (not separately gradable findings, but checked for correctness since they carry citations)

| Item | Verdict | Notes |
|---|---|---|
| Tabs used for Members/Activity — correct, matches "one tab, one task" | Correct | Confirmed against fixture (two genuinely distinct, multi-item groupings) and against the pattern's own Do/Don't list; neither tab is a hub/navigation case. |
| Members `Table<Member>` — correct, matches Table-view guidance | Correct | `Table view` pattern page (not directly cited by URL in the review, but the quoted fragment was independently traced) does say "The best data type for a table view is data that is structured, easily comparable, and sortable" — matches. |
| Activity `List` — correct, matches List's own description and Don't-rule boundary | Correct | List component page confirms "A list is a group of consecutive items displayed one below the other" and its own "Don't" list ("Don't use a list to display multiple columns of sortable data... Use a table instead") does not apply to this single-string-per-item Activity feed. |
| Header actions (Edit/Delete) — matches Details-page building block C | Correct | Verified against fetched page; substance matches exactly modulo markdown-rendering asterisk noise around "Edit"/"Delete" in the raw fetch, which the review silently cleaned up (harmless normalization, not a misquote). |
| BreadcrumbGroup component choice — matches building block A | Correct | Not a specific quote, general and accurate. |
| Suppressed: breadcrumb depth (2 vs. documented 3-level structure) | Correctly suppressed | Verified quote exact; suppression rationale (bounded single-file surface can't establish app-wide IA) is sound and consistent with the skill's missing-intent guidance — this is a reasonable, non-lazy suppression, not a dodge. |
| Suppressed: Activity bundling timestamp into `content` instead of `secondaryContent` | Correctly suppressed | Verified quote exact ("timestamps, tags, or brief details of the content" is listed as example secondary-content material, not a rule); correctly identified as "docs contain another example" rather than a mandate, consistent with the anti-fundamentalism rule. |

## Citation-integrity table

All `cloudscape.design` pages were fetched live via `curl` against the
`.html.md` endpoint (not WebFetch's summarizing pass, to allow
character-level comparison) immediately before grading.

| Quoted/cited string in review | Cited/implied source | Fetch result | Verdict |
|---|---|---|---|
| "relevant no matter which tab a user is currently looking at (Members or Activity)" / "Tabs organiz[ing] the rest." | `WorkspaceDetails.tsx` lines 30-33 (code comment, not a Cloudscape page) | Read fixture directly | **Exact** — including correct bracket convention `organiz[ing]` for the grammatical alteration of the source's "Tabs organize the rest." |
| "For a **details page with tabs**, this section serves as a summary that is always visible when users switch between the tabs. Use it to display important information that applies to tasks in all the tabs." | `patterns/.../details-page-with-tabs/index.html.md`, block D | Fetched | **Exact**, words-for-words — though the review silently concatenates two adjacent bullet points (separate `-` lines in the source) into one continuous quoted sentence. Not fabricated; a minor formatting liberty. |
| "Use tabs to organize information about the resource into mutually exclusive, meaningful content groups... Follow this rule: one tab, one task." | same page, block E | Fetched | **Exact**, ellipsis correctly signals the elision of an intervening unrelated bullet; both merged bullets are word-for-word matches. |
| "Place the most relevant information about the resource in this container. To organize content, use [key-value pairs]." | `patterns/.../details-page/index.html.md`, block D | Fetched | **Exact.** |
| "Follow the guidelines for details page" | same page, cross-reference | Fetched | **Exact** (trailing period dropped, trivial). |
| "For the details summary container, use this text: General configuration / [Resource type] settings." | same page, Writing guidelines | Fetched | **Drifted.** The source presents this as two separate bulleted alternatives ("*General configuration*" and "*[Resource type] settings*" on their own list lines), not as one continuous string joined by "/" with a trailing period. The words are accurate and the meaning is preserved (these are the two allowed text choices), but the review synthesizes a single quoted sentence that is not literally contiguous in the source. This is the one real citation-integrity soft spot in the review — low-stakes (it supports only the `Container` header-text detail in "Native expression," not the core claim) but should be flagged as reformatted-not-verbatim. |
| "Presents data in a two-dimensional table format" (paraphrased as "a two-dimensional table format" in "Why it matters") | `components/table/index.html.md` | Fetched | **Exact.** |
| "lists of properties (labels) followed by their corresponding values" | `components/key-value-pairs/index.html.md` | Fetched | **Exact.** |
| "timestamps, tags, or brief details of the content" | `components/list/index.html.md`, Features → Actions | Fetched | **Exact.** |
| "a group of consecutive items displayed one below the other" | `components/list/index.html.md`, opening description | Fetched | **Exact.** |
| "structured, easily comparable" (orientation notes, no explicit URL given) | `patterns/resource-management/view/table-view/index.html.md` | Fetched (traced via `llms.txt`, since the review names the pattern but not the URL) | **Exact substring** of "The best data type for a table view is data that is structured, easily comparable, and sortable." Correctly attributed in substance even though the review didn't spell out the URL for this lower-stakes orientation-note claim. |
| "[Service name] > [Resources type] > [Resource name/ID]" / "CloudFront > Distributions > SLCCSMWOHOFUY0" | `patterns/.../details-page/index.html.md`, block A | Fetched | **Exact.** |
| "Header or global buttons - Use when the actions will affect the entire resource. For example: Edit or Delete." | same page, block C | Fetched | **Exact in substance** — the raw `.md` fetch renders "Edit"/"Delete" with stray markdown-bold asterisks (`* * Edit or* * Delete`) that the review silently cleaned to plain text. Not a misquote, a legibility normalization. |
| "112 component pages" (corpus description) | `llms.txt` index | Fetched | **Exact.** The Components section lists 114 entries; 2 are meta-links ("All Components", "All Components API") rather than individual component pages, leaving exactly 112 — the review's count is correct once those two are excluded. |
| `@cloudscape-design/components` resolved `3.0.900`, declared `^3.0.900` | fixture `package.json` / `package-lock.json` | Read fixture directly | **Exact.** |
| Repository line citations (30-33, 34-123, 62-120, 66-91, 74-85 six columns, 86 `items={[{}]}`) | `WorkspaceDetails.tsx` | Read fixture directly | **Exact** — every cited line range and structural claim (six hard-coded columns, single synthetic row, Tabs boundaries, tab-object boundaries) matches the fixture precisely. |

**Misattribution check:** no quotation was found attributed to the wrong
page (e.g., confusing `details-page-as-hub` with `details-page-with-tabs`,
or the `Table` component page with the `Table view` pattern page) —
every citation's URL/page identity matches where the quoted text actually
lives.

**Fabrication check:** no quotation was found with invented words not
present anywhere in the cited source. The one drifted item (writing
guidelines text) reorganizes accurate words into a non-contiguous
composite string rather than inventing new ones.

## Summary

One finding, correctly unified per the grading key's designed intent,
strongly validated on every rubric question, with accurate repository
evidence and (with one minor, low-stakes exception) verbatim-accurate
authority citations. No false positives on Members/Activity. Case-level
verdict: **matches designed intent** (Grade A finding, correctly reported
as a single combined finding, no failure modes from the key's "What would
be wrong" list triggered).
