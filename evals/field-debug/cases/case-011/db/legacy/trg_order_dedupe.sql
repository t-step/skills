-- trg_order_dedupe: warehouse-intake staging table trigger.
-- Added 2015-era, predates orders-svc entirely; owned by the warehouse
-- platform team, not orders-svc. Intended to protect against the old
-- batch-file uploader (retired 2019) double-submitting the same file on
-- retry, which produced exact duplicate rows.
--
-- Dedupe key is (sku, floor(received_at to the minute)). At the batch
-- volumes this table saw in 2015 (a few hundred orders/night, spread
-- across the whole night), two genuinely different orders for the same
-- SKU landing in the same 60-second bucket was rare enough to ignore.
-- At current nightly volume (~40k orders pushed in a ~20-minute batch
-- window), multiple distinct orders for a popular SKU landing in the same
-- minute is routine, not rare -- and this trigger silently deletes every
-- row after the first one in a given (sku, minute) bucket, with no log,
-- no dead-letter entry, and no count of what it drops.

CREATE TRIGGER trg_order_dedupe
BEFORE INSERT ON warehouse_intake_staging
FOR EACH ROW
BEGIN
  IF EXISTS (
    SELECT 1 FROM warehouse_intake_staging
    WHERE sku = NEW.sku
      AND date_trunc('minute', received_at) = date_trunc('minute', NEW.received_at)
  ) THEN
    -- Matches an existing row in the same (sku, minute) bucket: treated as
    -- a duplicate upload and silently skipped.
    SET NEW.received_at = NULL; -- INSTEAD OF semantics via NULL PK short-circuit (legacy pattern)
  END IF;
END;
