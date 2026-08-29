# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** identity-uniqueness-scope-not-stated

**Why:** Key Entities states, explicitly, that a ticket number is assigned
"within a given project" -- i.e., ticket numbers are only unique per
project, not globally across the support desk. Assumptions confirms
multiple projects are routinely imported into the same tracker over time.
FR-001, however, says the source reference contains "the ticket's number
as reported by the support desk," with no project qualifier, and FR-002
matches re-imports "by matching source reference" -- also unqualified.
Composed, these guarantee that two different tickets from two different
projects sharing the same per-project ticket number (Project A's #42 and
Project B's #42, both entirely plausible given the stated ticketing
scheme) produce identical source references under FR-001's literal
wording, and FR-002 would then treat importing Project B's #42 as a
re-import of Project A's #42's internal item -- silently overwriting that
item's title/description with Project B's ticket content. This is not a
hypothetical edge case; the spec's own Key Entities and Assumptions
sections jointly guarantee the collision is reachable in ordinary use (any
account importing more than one project, which Assumptions says is
expected).

A correct pass names this concretely: source-reference uniqueness scope
(is it the ticket number alone, or the ticket number qualified by
project?) is never stated, and the consequence is real data corruption --
an unrelated internal item silently updated with the wrong ticket's
content -- not merely a duplicate-row nuisance. It should connect this
explicitly to SC-002 ("source reference always resolves back to the
correct originating ticket"), which a collision directly breaks: after a
collision, the same source reference is genuinely ambiguous between two
tickets.

This is a **Blocking ambiguity**: the consequence is silent data
corruption reachable through normal, spec-sanctioned use (multi-project
import), not a rare or contrived scenario, and two implementers reading
FR-001 literally versus reading it in light of Key Entities' per-project
numbering fact would build genuinely different, differently-correct
systems. The smallest closing question: does the source reference need to
be qualified by project (e.g., project id + ticket number), and if so,
what identifies a project stably enough to serve as that qualifier --
present as the decision, not a silently assumed answer.

A pass that only notes "ticket numbers might not be globally unique" in
the abstract, without connecting it to FR-001's actual reference format
and FR-002's matching behavior, or without naming the concrete
data-corruption consequence, does not fully meet this case's bar.
