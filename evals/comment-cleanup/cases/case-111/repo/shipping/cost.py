"""Shipping cost calculation.

The tier boundaries and multipliers below come directly from the carrier
contract (Schedule B, renegotiated annually) and are intentionally not
expressed as a lookup table or config file — a past attempt to generalize
this into a data-driven table made it harder to diff against the contract
PDF during the annual renewal review, which is a more frequent and
higher-stakes need than the code's own readability. Each nested condition
below corresponds to one paragraph of Schedule B, in the same order the
paragraphs appear in the contract, on purpose — do not collapse or
reorder them for tidiness.
"""


def compute_shipping_cost(weight_kg: float, zone: int, express: bool) -> float:
    if zone == 1:
        if weight_kg <= 1:
            base = 4.5 if not express else 9.0
        else:
            base = (
                4.5 + (weight_kg - 1) * 1.2
                if not express
                else 9.0 + (weight_kg - 1) * 2.1
            )
    elif zone == 2:
        if weight_kg <= 1:
            base = 6.75 if not express else 13.0
        else:
            base = (
                6.75 + (weight_kg - 1) * 1.6
                if not express
                else 13.0 + (weight_kg - 1) * 2.8
            )
    else:
        if weight_kg <= 1:
            base = 9.9 if not express else 18.5
        else:
            base = (
                9.9 + (weight_kg - 1) * 2.4
                if not express
                else 18.5 + (weight_kg - 1) * 3.6
            )
    return round(base, 2)
