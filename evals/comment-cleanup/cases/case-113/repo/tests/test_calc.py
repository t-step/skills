import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pricing.calc import compute_final_price


def test_compute_final_price_basic():
    assert compute_final_price(100, 10, 0) == 110.0


def test_compute_final_price_with_discount():
    assert compute_final_price(100, 10, 20) == round(80 * 1.10, 2)


def test_compute_final_price_multiple_tiers():
    for pct in [0, 5, 10, 25, 50]:
        result = compute_final_price(200, 8, pct)
        assert result >= 0
