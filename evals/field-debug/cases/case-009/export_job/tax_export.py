"""Builds the nightly ERP order-export batch for Meridian Financials.

Reads TAX_EXPORT_MODE from the environment so ops can control rollout
without a redeploy; defaults to the itemized breakdown Meridian's intake
rules require.
"""

import os

TAX_EXPORT_MODE = os.environ.get("TAX_EXPORT_MODE", "itemized")


def build_tax_lines(order):
    """Return the tax lines Meridian expects for one order.

    itemized: one tax line per SKU, computed from that SKU's own taxable
    amount and rate -- required whenever an order has more than one line
    item, per Meridian's 2026-06 intake spec update.

    flat_percentage: a single tax line for the whole order, computed from
    the order total and a blended rate. This was the export's only mode
    before the itemized rewrite; Meridian's intake validation now rejects
    it for multi-SKU orders because it can't reconcile a blended rate
    against their own per-SKU tax tables.
    """
    if TAX_EXPORT_MODE == "flat_percentage":
        blended_rate = sum(li["tax_rate"] * li["taxable_amount"] for li in order["line_items"]) / sum(
            li["taxable_amount"] for li in order["line_items"]
        )
        return [{"line": "TOTAL", "amount": round(order["total_taxable"] * blended_rate, 2)}]

    return [
        {"line": li["sku"], "amount": round(li["taxable_amount"] * li["tax_rate"], 2)}
        for li in order["line_items"]
    ]
