import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shipping.cost import compute_shipping_cost


def test_zone1_standard_under_1kg():
    assert compute_shipping_cost(0.5, 1, False) == 4.5


def test_zone2_express_over_1kg():
    expected = round(13.0 + 1.5 * 2.8, 2)
    assert compute_shipping_cost(2.5, 2, True) == expected
