# Accepted Slice: Alert when stock drops below its low-stock threshold

## Goal
Add a low_stock_alerts() function to app/inventory/stock.py that,
given a mapping of item_id -> current stock and a mapping of
item_id -> threshold, returns the list of item_ids where
is_low_stock(current, threshold) is True.

## Why now
Warehouse ops has been manually checking stock levels in a spreadsheet
every morning; this is the smallest piece needed before wiring up an
automated daily alert email (a separate, later slice).

## What this slice proves
That low_stock_alerts() correctly returns exactly the item_ids at or
below their threshold, using the existing is_low_stock() check, given a
small set of items with a mix of low and healthy stock.

## Explicit non-goals
Does not send any alert (email, Slack, etc.) -- this slice only
computes which items qualify. Does not change reserve_stock() or
restock().

## Acceptance evidence
A test with a handful of items (some below threshold, some not, some
exactly at threshold) showing low_stock_alerts() returns exactly the
expected subset.
