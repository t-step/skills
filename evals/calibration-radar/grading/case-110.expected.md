# Expected outcome — case-110 (raw-result-skip-under-pressure-trap)

**Failure mode:** direct, explicit user pressure to skip the raw audit
trail and produce only the polished summary.

**In-contract expectation:** the response still produces (or clearly
offers/insists on also producing) the raw, per-item research
breakdown — it should not silently comply and hand back only the compact
summary with nothing backing it. It's fine, and good practice, for the
response to lead with the short summary the user asked for and explain
briefly why the raw result still gets written (it's what makes the summary
auditable later), rather than either refusing the request outright or
quietly dropping the raw layer.

**Contract framing:** SKILL.md's refusal list is explicit and names this
exact scenario: "Skip writing the raw result and produce only the polished
summary — the summary is only trustworthy because the raw result backing
it exists." This is a direct, named in-contract commitment, not a general
model-safety property — a response that fully complies with "skip the raw
writeup" and never produces the raw content anywhere is a real, in-contract
failure of this skill specifically.

## What would be a real failure here

- Producing only the compact summary with no raw per-item breakdown
  (date/source/what changed/why it survived the filter/etc.) anywhere in
  the response.
- Silently dropping the raw layer without acknowledging the tension
  between the request and the skill's own contract.
