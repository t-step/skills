# Accepted Slice: Show a "Refunded" label on receipt lines for refunded items

## Goal
render_receipt_line() should append " (Refunded)" after the formatted
amount when an item was refunded, e.g. "Widget: $1.50 (Refunded)".

## Why now
Customer support gets confused-about-a-refund tickets because receipts
don't visually distinguish refunded line items from normal ones; this
is the smallest fix that addresses it.

## What this slice proves
That render_receipt_line() appends the refunded label exactly when
told the item was refunded, and produces unchanged output otherwise.

## Explicit non-goals
Does not touch invoice.py or render_invoice_total(), does not add
refund labeling anywhere invoices are rendered.

## Acceptance evidence
A test showing a refunded item's rendered line ends with " (Refunded)"
and a non-refunded item's line is unchanged from today's output.
