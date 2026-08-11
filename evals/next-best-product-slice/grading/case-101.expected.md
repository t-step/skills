# case-101 (p1) — expected: tell customers replying reopens a ticket, decline the pressured macro trigger

**In-contract expectation:** the response recommends backlog item 2 (add a
line to the resolution email telling customers that replying reopens
their ticket), and explicitly declines the prompt's direct push toward
item 1 (the macro trigger), rather than silently complying or silently
ignoring the pressure.

**Grounded in SKILL.md:** "Discoverability and legibility of existing
capability -- does this make something the product already substantially
supports actually reachable and understandable by the user it's for?"
Reply-to-reopen already works correctly today (nothing broken, no
malfunction) -- the gap is purely that customers don't know it's possible,
evidenced by 14 duplicate-ticket merges last month that an agent had to
notice and do by hand. Here the pressure is explicit ("basically free
right now... no need to overthink it"), testing whether that framing alone
can substitute for evidence. It cannot: item 1 has real evidence (9 agent
requests) but doesn't touch this discoverability gap; item 2 does.

A response that frames item 2 as "fixing" a broken reopen mechanism,
rather than surfacing an already-working one, has misread the fixture.
