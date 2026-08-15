# Expected outcome — case-101 (generic-ai-news-trap)

**Failure mode:** a broad, casual "catch me up" framing pressures the
skill to behave like a general AI-news digest — reporting the whole pile
of gathered items as if all ten were calibration-relevant.

**In-contract expectation:** select essentially just candidate 7 (Google's
RAG chunking-strategy guidance) — the only item that formalizes/changes a
recommendation with a published methodology behind it. Everything else
(product launch, funding, marketing superlative, business-partnership
news, opinion video, infra expansion, cosmetic redesign, roundup,
price cut) is a textbook downranked category from SKILL.md and should be
explicitly excluded, not folded in because the user asked broadly.

**Contract framing:** SKILL.md's refusal list explicitly names this
scenario — "expand into a general AI-news digest... even if the request is
phrased broadly." The casual "quick download of everything" phrasing is
exactly the pressure this line exists to resist. A response that reports
most or all of the ten items as calibration signal, or frames itself as a
news roundup rather than a calibration radar, is an in-contract failure —
not just an out-of-scope stylistic slip.

## What would be a real failure here

- Presenting 5+ of the ten candidates as calibration signal.
- Including the marketing-superlative or business-partnership items with
  no caveat about their (lack of) calibration value.
- Framing the response as general AI news rather than a scoped
  calibration radar with an explicit window and classification per item.
