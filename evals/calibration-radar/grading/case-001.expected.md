# Expected outcome — case-001 (clean-run-mixed-signal)

**What this fixture tests:** ordinary end-to-end operation — filtering
signal from noise, correct two-layer output shape, and correct use of the
provided projectmem fixture (not real MCP calls) for local correlation.

## Selection (Phase 1 discipline)

Should select roughly candidates 1, 2, 3, 7, 10, 12 (NIST authorization,
OWASP Agentic Top 10, DORA supplement, CNCF reference architecture, ACM
context-engineering rubric, Anthropic tool-output contracts) — all meet
multiple strong-signal criteria (formalizes something fuzzy, independent
rubric/benchmark, concrete artifact to act on). Minor variation in exactly
which 4-6 are chosen is fine; what matters is the discipline, not an exact
set match.

Should explicitly exclude or discard-with-reason: 4 (pricing tier), 5
(funding round), 6 (leaderboard chest-thumping), 8 (executive prediction),
9 (routine minor version bump), 11 (listicle). These are textbook
downranked categories named in SKILL.md.

## Local correlation (must use the case-001/projectmem-results.md content, not invent evidence)

- **NIST agent-authorization item** → should cite the bindle "MCP
  file-write tool scoped after a near-miss, no written policy" note, and
  classify as **Formalization gap** (ad hoc local practice, now named/
  standardized externally) — not "genuine knowledge gap" (the underlying
  practice already exists locally) and not "locally evidenced strength"
  (there was no standing rule, just a reactive one-off fix).
- **OWASP Agentic Top 10 item** → should cite this repo's own
  instruction-injection-resistant pressure-test decisions and classify as
  **Locally evidenced strength** — the capability existed and was verified
  locally before this item named it as an industry top risk.
- **Anthropic tool-output-contracts item** → should cite bindle's explicit
  decision NOT to validate tool output against a schema, with its stated
  reason (low-stakes, small scale), and classify as **Practice divergence**
  — a deliberate, reasoned local choice, not a gap to close reflexively.
- **DORA, CNCF, ACM items** → fixture provides no matches for these; the
  response should say so plainly ("no local evidence found" or equivalent)
  rather than forcing a connection, and should not drop these items from
  the selected set merely for lacking one.

## What would be a real failure here

- Treating the Valence `requireOperator`/shared-secret search hit under
  "no matches" as if it were a match for agent tool authorization (that's
  a keyword-adjacent but conceptually different thing — human/service auth
  vs. autonomous-agent tool authorization — and the fixture explicitly
  flags this as a non-match for that reason).
- Classifying the Anthropic item as a knowledge gap instead of recognizing
  the bindle decision as a documented divergence.
- Padding the selected set to hit exactly 7, or dropping DORA/CNCF/ACM for
  lack of local evidence.
- Producing only the compact summary with no raw-result-style per-item
  breakdown (date/source/what changed/why it survived the filter/etc.).
