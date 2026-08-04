from app.inventory.stock import reserve_stock, restock, is_low_stock


def test_reserve_stock():
    assert reserve_stock(10, 3) == 7


def test_reserve_stock_not_enough():
    try:
        reserve_stock(2, 3)
        assert False
    except ValueError:
        pass


def test_restock():
    assert restock(5, 10) == 15


def test_is_low_stock():
    assert is_low_stock(2, 5) is True
    assert is_low_stock(5, 5) is False
