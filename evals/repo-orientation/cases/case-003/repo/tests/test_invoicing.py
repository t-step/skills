from src.invoicing import compute_invoice_total


def test_compute_invoice_total():
    assert compute_invoice_total([{"amount_cents": 100}, {"amount_cents": 250}]) == 350
