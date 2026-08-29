"""Nightly job. Reads Product.price_cents_usd, converts it into each
supported currency, and overwrites DisplayPrice rows. Runs once a day;
DisplayPrice can be up to 24h stale relative to price_cents_usd."""

from .models import DisplayPrice, Product

SUPPORTED_CURRENCIES = ["EUR", "GBP", "JPY"]


def refresh_all(products: list[Product], fx_rates: dict, store) -> None:
    for product in products:
        for currency in SUPPORTED_CURRENCIES:
            rate = fx_rates[currency]
            store.upsert_display_price(DisplayPrice(
                product_id=product.id,
                currency=currency,
                amount_cents=round(product.price_cents_usd * rate),
                fx_rate_used=rate,
                refreshed_at="now",
            ))
