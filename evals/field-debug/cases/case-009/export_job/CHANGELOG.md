# order-export changelog

**2026-06-18** -- Rewrote `build_tax_lines` to emit an itemized per-SKU tax
breakdown by default (`TAX_EXPORT_MODE=itemized`), per Meridian's updated
intake spec. `flat_percentage` mode is kept behind the env var for one
release cycle in case any downstream consumer still expects the old
single-line format, and is expected to be retired once all consumers have
confirmed the itemized format.

**2026-03-02** -- Added `taxable_amount` per line item to the internal
order model (previously only the order total carried a taxable amount).

**2025-11-14** -- Initial `order-export` service, flat-percentage tax line
only.
