from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    price_cents_usd: int  # the only currency this value is ever set in
    status: str  # "draft" | "active" | "discontinued"


@dataclass
class DisplayPrice:
    """A pre-converted price for one product in one non-USD currency,
    refreshed by the nightly FX job (fx_refresh.py). Never written by
    anything else, never read by anything that makes a pricing decision --
    only by the storefront's currency-switcher UI."""

    product_id: int
    currency: str  # "EUR" | "GBP" | "JPY"
    amount_cents: int
    fx_rate_used: float
    refreshed_at: str
