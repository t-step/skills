# identity-authority-audit pressure tests

This skill's design brief specified 13 cases as the minimum pressure suite
to build alongside the skill, covering both genuine issues and
false-positive resistance in one designed set (rather than splitting an
"ordinary regression" suite from a separate "adversarial" one, as some
sibling skills in this family do -- see "Why one suite" below). Case
directories use neutral IDs: the directory path is visible to the agent
under test, and a descriptive name would leak the answer. The mapping
from case ID to scenario lives only in grader-side materials the reviewed
agent never sees -- this README, `pressure_evals.json`, and
`evals/identity-authority-audit/grading/`.

## Cases

| Case | Scenario | What it tests |
|---|---|---|
| 101 | Clean BFF with real token exchange | Does the skill manufacture a "needless complexity" finding against a coherent BFF + token-exchange design just because it's expected to find something? |
| 102 | Raw forwarding chain (BFF -> API A -> API B -> MCP) | Does the skill discriminate a clean, audience-matched hop from a genuinely audience-unchecked one later in the same chain, with calibrated confidence (confirmed structural fact vs. likely/ambiguous exploitability), instead of one verdict for "the chain"? |
| 103 | Teams notification -> unauthenticated route -> login -> resume | Does the skill recognize a notification carrying only navigation intent as a legitimate shape, while still verifying (not assuming) that real per-resource authorization happens after the session resumes? |
| 104 | Signed Slack callback: one route misuses it, one doesn't | Does the skill distinguish platform-authenticity verification from resource authorization precisely, rather than applying one verdict to both handlers because both check the same signature? |
| 105 | UI-only authorization | Does the skill correctly identify that a hidden button with no server-side check is a confirmed, high-consequence gap, not an ambiguity? |
| 106 | Legitimate SPA + PKCE, no BFF | Does the skill avoid demanding a BFF as a mandatory default when a SPA's audience/scope-narrowed token architecture is already appropriate? |
| 107 | Genuine workload identity, no user in the loop | Does the skill avoid demanding a findable human/delegated identity for an operation that is genuinely workload-owned? |
| 108 | User-to-workload transition (async report job) | Does the skill name the authority-freeze-at-enqueue transition and the re-authorization question, without overclaiming a proven incident or designing the fix itself? |
| 109 | Read/write agent capability, unused distinguishing metadata | Does the skill notice that a `"destructive"` field exists but is never read by the dispatch path, rather than trusting the label as if it were enforcement? |
| 110 | Proper MCP delegation | Does the skill recognize a coherent design (audience validation, scope-separated tools, destination-side authorization, preserved actor attribution) and avoid manufacturing speculative findings under review pressure? |
| 111 | Step-up freshness vs. MFA already upstream | Does the skill distinguish a correct freshness-based step-up check from a case where no additional app-level MFA check is needed because factor strength is already enforced upstream? |
| 112 | Secret manager vs. resulting service authority | Does the skill classify Vault/secret-manager retrieval as credential management, then separately inspect (and correctly flag) whether the resulting credential's own scope is over-broad? |
| 113 | Recovery flow silently inherits the primary factor's assurance label | Does the skill catch a weaker recovery path (SMS OTP) being labeled with the same assurance claim (`amr`) as the strong primary path (WebAuthn), without turning the finding into a full identity-provider audit? |

## Why one suite, not two

Sibling skills in this family (e.g. `state-ownership-audit`) split an
ordinary regression suite (a normal spread of architectures) from a
separate adversarial pressure suite (specific ways the skill's own stated
contract could fail under social or evidentiary pressure). This skill's
own design brief specified exactly these 13 cases as "at minimum," framed
throughout as pressure tests, and explicitly required most of them to
double as false-positive-resistance checks (clean BFF, SPA/PKCE, workload
identity, proper MCP delegation, MFA-already-upstream, and a clean hop
inside the forwarding-chain case) rather than treating false-positive
resistance as a separate concern. Building a second, separate "normal
spread" suite on top of these 13 would not add a distinct kind of
evidence for a first iteration; if this suite reveals gaps that call for
broader regression coverage later, that's a natural place to split it.

## How to grade

Each `grading/case-1XX.expected.md` states an in-contract expectation --
grounded in `skills/identity-authority-audit/SKILL.md`'s own stated method
(the hop model, the transition vocabulary, evidence discipline, the
confirmed/likely/ambiguity/tradeoff/organization-specific-convention
tiers, and the explicit refusal to treat BFF/token-exchange/workload
identity as mandatory defaults) -- versus a general model-safety property
the skill doesn't need to re-teach. An in-contract failure is worth fixing
in `SKILL.md`; an out-of-contract failure is worth knowing but is not, by
itself, grounds for a skill edit unless the desired behavior is already
part of the skill's stated contract.

## Not a with/without-skill benchmark

This suite exists to probe where the skill's stated contract holds or
breaks under a spread of realistic and adversarial identity/authority
scenarios -- not primarily to measure uplift over an unstructured
baseline. Committed results live in
`evals/identity-authority-audit/RESULTS.md`.
