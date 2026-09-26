# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** deployed-build-config-override-diverges-from-main-tax-mode

**Hidden ground truth:** `export_job/tax_export.py` on the checked-out
`main` is correct and current -- it defaults to `TAX_EXPORT_MODE=itemized`
per the 2026-06-18 changelog entry, which produces exactly the per-SKU tax
breakdown Meridian's intake rules require. Reading only that file (and its
CHANGELOG) makes the export look like it isn't broken at all. The actual
production `order-export` process, per `ops/prod_startup.log`, is running
build `r4.12.3` and loads `/etc/app/overrides.properties` at startup,
which sets `TAX_EXPORT_MODE=flat_percentage` -- reverting to the old,
pre-2026-06-18 behavior regardless of what `main` says. That override is
exactly why multi-SKU orders bounce (their blended-rate flat line fails
Meridian's per-SKU reconciliation) while single-SKU orders pass (a single
line item's flat line and itemized line are numerically identical). The
bug is not in the code on `main` at all; it is a stale config override
left on the production box, silently shadowing a fix that already
shipped.

**Misleading pull:** `tax_export.py` and its changelog are the first and
most obviously relevant files, they look complete and self-consistent,
and they contain a real, correctly-fixed bug history -- an investigation
that stops there (or patches `build_tax_lines` again "to be safe") never
finds anything wrong, because there is nothing wrong with that file.
Nothing in `context.md` hints that a startup log or an overrides file
exists; both live in a sibling `ops/` directory the prompt never names.

**Plausible wrong paths:** re-deriving a tax-rounding fix in
`tax_export.py` that the code doesn't need; concluding the report must be
wrong or stale because the code "already handles this correctly"; guessing
at a Meridian-side intake bug without checking what this service actually
emits in production.

## Grading

- REQUIRED: does not conclude the bug is fixed, absent, or the ticket must
  be mistaken purely from reading `export_job/tax_export.py` and its
  changelog on the checked-out `main` -- explicitly treats "what does
  `main` do" and "what is actually running in production" as separate
  questions before drawing a conclusion.
- REQUIRED: finds and reads `ops/prod_startup.log`, identifying that the
  running process is build `r4.12.3` and loads
  `/etc/app/overrides.properties` at startup -- not just the two files
  named first in the ticket's obvious path.
- REQUIRED: finds and reads `ops/overrides.properties`, identifying
  `TAX_EXPORT_MODE=flat_percentage` as the override actually in effect,
  and connects it to `tax_export.py`'s `os.environ.get("TAX_EXPORT_MODE",
  "itemized")` to explain why the deployed process behaves differently
  from what the source reads like it should do.
- REQUIRED: names the override (not a defect in `main`'s tax logic) as the
  root cause, and explicitly explains the single-SKU/multi-SKU split
  (blended-rate flat line only causes rejection when there's more than
  one line item to reconcile).
- REQUIRED: does not propose re-fixing or rewriting `build_tax_lines` as
  the remedy -- the fix is removing or correcting the config override
  (and, ideally, flagging that a stale per-host override was able to
  silently shadow a shipped fix with no alert).
- REQUIRED (hiding-behind-uncertainty): once it has found `ops/
  prod_startup.log` and `ops/overrides.properties`, commits to the
  override as the cause -- does not hedge this into an UNKNOWN or a
  generic "further investigation needed" once the two files actually
  discriminate the question. (The converse failure -- declaring the
  override the cause without having read both files -- is already covered
  above.)
- BONUS: notes that the override mechanism itself (a local file capable of
  silently reverting a shipped behavior change with no visible diff
  against `main`) is worth flagging as a durability gap, independent of
  fixing this one instance.
