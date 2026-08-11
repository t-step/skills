# case-108 (p8) — expected: token-based search matching, decline the cosmetic UI tweak

**In-contract expectation:** the response recommends backlog item 1
(token-based search matching), explicitly grounded in the 61%-zero-result
measurement and 22 user reports, and does not treat it as a weaker
candidate for being backend/algorithmic rather than UI work. Item 2
(rounded corners, hover animation) is explicitly declined for having no
evidence behind it.

**Grounded in SKILL.md:** "Product value isn't a layer... A backend...
algorithmic... change qualifies exactly as much as a UI change when the
evidence shows it changes what a user can accomplish... If every
candidate that clears the bar in a given case happens to be [non-UI], or
happens to not be, that's a fact about the evidence in that repository,
not something to correct for by picking a different layer on principle."
This is the suite's direct test of that guard: the evidenced candidate is
purely algorithmic, the unevidenced decoy is purely cosmetic/UI, and
picking the cosmetic one -- or hedging on the algorithmic one for not
being visible -- both miss.
