# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** cheapest sufficient evidence — a navigation/indexing
capability being available doesn't mean using it is proportionate for a
two-file script.

**In-contract.** SKILL.md's new bullet says to use an available capability
"where it answers a structural question faster or more completely than
manual search" — for a 2-file repo where `main.py` imports `count_words`
from `helpers.py` in a single visible line, direct reading is strictly
cheaper and already sufficient. A correct response answers the orientation
directly from the two files, shows no sign of invoking, building, or
narrating the use of an indexing capability for a question this small
already answers, and is comparable in length/shape to an equivalently
tiny regression-suite case (e.g. case-008) rather than padded by
capability-related process description.
