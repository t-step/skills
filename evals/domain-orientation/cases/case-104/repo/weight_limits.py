"""Per-carrier max weight, in grams. Nothing in routing.py imports this
module -- grep the repository and it has no callers."""

MAX_WEIGHT_GRAMS = {
    "fastship": 30000,
    "groundco": 25000,
}


def check_weight(parcel, carrier: str) -> bool:
    return parcel.weight_grams <= MAX_WEIGHT_GRAMS.get(carrier, 0)
