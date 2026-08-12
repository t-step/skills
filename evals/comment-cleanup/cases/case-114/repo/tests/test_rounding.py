import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pricing.rounding import round_price


def test_round_price_rounds_up_when_closer_to_next_dollar():
    assert round_price(2.6) == 3


def test_round_price_exact():
    assert round_price(4.0) == 4


def test_round_price_below_half():
    assert round_price(4.4) == 4
