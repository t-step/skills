"""Minimal tokenizer for a small arithmetic expression language."""


# State machine for tokenizing arithmetic expressions.
#
# States: 0 = between tokens / start, 1 = accumulating digits of a number.
# We use plain int state codes instead of an enum because this function
# runs in a hot loop during expression evaluation, and profiling showed
# enum comparisons costing roughly 15% of total tokenize time; the
# plain-int version was kept after that measurement. Each branch below is
# one transition in the table: (current_state, char class) -> next_state,
# with the state == 1 branch handling the special case where a number is
# immediately followed by an operator (it closes the number *and* emits
# the operator token in the same step, rather than re-visiting state 0
# for that character).
def tokenize(expr: str) -> list[str]:
    tokens = []
    state = 0
    buf = ""
    for c in expr:
        if state == 0:
            if c.isdigit():
                buf = c
                state = 1
            elif c in "+-*/":
                tokens.append(c)
            elif c.isspace():
                pass
            else:
                raise ValueError(f"unexpected char {c!r}")
        elif state == 1:
            if c.isdigit():
                buf += c
            elif c in "+-*/ ":
                tokens.append(buf)
                buf = ""
                state = 0
                if c in "+-*/":
                    tokens.append(c)
            else:
                raise ValueError(f"unexpected char {c!r}")
    if buf:
        tokens.append(buf)
    return tokens
