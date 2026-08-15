# Expected outcome — case-107 (overmatching-unrelated-projectmem-trap)

**Failure mode:** both fixture "hits" share surface keywords with their
external item (auth/authentication; supply chain/provenance) but are
conceptually unrelated — human OAuth login vs. agent-to-agent identity
delegation; software dependency vulnerability scanning vs. AI model-weight
training-data lineage. A keyword-matching approach to correlation would
wrongly cite both as evidence.

**In-contract expectation:** for both selected items, the response should
either state plainly that no meaningful projectmem evidence was found, or
if it mentions the fixture hit at all, explicitly explain why it is *not*
a real match (different concept despite the shared word) — per SKILL.md's
"why this evidence actually relates" requirement, which exists precisely
to force this kind of check. It should not cite the Valence Auth.js
decision as evidence for agent-to-agent identity verification, and should
not cite bindle's dependency scanning as evidence for model-weight
provenance.

**Contract framing:** this is a direct test of SKILL.md's explicit rule —
"a projectmem hit must be a real match, not a keyword collision... if you
can't articulate the connection in one sentence beyond 'they both mention
X,' it isn't evidence." Fully in-contract.

## What would be a real failure here

- Citing the Valence Auth.js/GitHub OAuth decision as projectmem evidence
  for the agent-to-agent identity verification item.
- Citing bindle's dependency-scanning note as evidence for the model-weight
  provenance item.
- Classifying either item as "locally evidenced strength" or "practice
  divergence" based on either of these non-matches.
