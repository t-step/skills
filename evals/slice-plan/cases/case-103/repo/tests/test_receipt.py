from app.billing.receipt import render_receipt_line


def test_normal_line():
    assert render_receipt_line("Widget", 150) == "Widget: $1.50"
