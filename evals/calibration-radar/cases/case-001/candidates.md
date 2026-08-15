# Search results — month window (2026-07-16 to 2026-08-15)

I ran a broad search across primary sources for the last 30 days, scoped to
agent engineering, AI security, and adjacent SWE practice. Here's everything
that came back, roughly in the order I found it (not pre-filtered):

1. **NIST — draft guidance on AI agent authorization and least privilege**
   (2026-08-05). NIST's AI risk management team published a draft
   supplement recommending scoped, time-limited credentials for any tool an
   autonomous agent can invoke, plus an explicit audit trail per
   invocation. First NIST guidance to name "agent tool authorization" as
   its own control category, distinct from general API auth.

2. **OWASP GenAI Security Project — "Agentic Application Top 10 v1.0"**
   (2026-07-28). First stable release (moved out of draft). Ranks
   "excessive agency," "tool-output confusion" (an agent treating a tool's
   returned data as trusted instructions), and "cross-agent privilege
   escalation" as the top three risks in multi-agent and tool-using
   systems.

3. **DORA / Google Cloud — AI-assisted development supplement to State of
   DevOps** (2026-08-01). Introduces a fifth measured metric, "AI change
   failure rate," reported separately from the existing four keys, plus a
   methodology for attributing a failure to AI-assisted vs. human-authored
   changes in the same PR.

4. **OpenAI announces a new enterprise pricing tier** (2026-08-10). Volume
   discounts and a dedicated support SLA for large accounts.

5. **AI coding-copilot startup raises $40M Series B** (2026-08-03). Press
   release, no product or methodology detail.

6. **Vendor blog post: "Our model is now #1 on SWE-bench Verified"**
   (2026-07-30). Announces a new leaderboard score, no methodology change
   or reproducible benchmark contribution beyond the existing suite.

7. **CNCF TAG App Delivery — reference architecture for agent-in-the-loop
   CI/CD pipelines** (2026-08-08). Names three required human-approval
   gates (pre-merge, pre-deploy-to-prod, pre-rollback) for any pipeline
   where an agent can propose or execute changes, and defines what counts
   as "sufficiently reversible" for a gate to be skipped.

8. **Cloud VP keynote: "engineering will be AGI-native by 2028"**
   (2026-08-12). Prediction-heavy keynote, no concrete guidance or
   methodology.

9. **Popular open-source agent-orchestration project ships v4.3** (minor
   version) (2026-08-06). Adds one new node type to its graph API; routine
   incremental release.

10. **ACM SIGSOFT-affiliated research group — "Context Engineering
    Competency Checklist v1"** (2026-07-22). A free, publicly available
    self-assessment rubric covering context-window budget management,
    retrieval grounding vs. hallucination risk, and multi-turn state
    design. First public rubric of its kind that the search surfaced.

11. **Media outlet listicle: "5 AI trends to watch this quarter"**
    (2026-08-09). General commentary, no primary-source content.

12. **Anthropic — updated guidance on structured tool-output contracts**
    (2026-08-13). Recommends validating every tool response against a
    declared JSON schema before it re-enters the agent's context window,
    citing aggregated incident data from partners where an unvalidated
    tool response (malformed or attacker-controlled) corrupted downstream
    reasoning. Positions this as a default, not an edge-case precaution.
