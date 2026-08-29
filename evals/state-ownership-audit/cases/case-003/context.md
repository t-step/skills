# Context

Design proposal circulated by a platform architect, asking for feedback
before it's written up formally:

> Having `available_units` split across three separate regional databases
> makes the codebase harder to reason about, and `GlobalCatalog`'s
> `total_available` is already polling all three FCs anyway. What if we
> flip it around: `GlobalCatalog` becomes the single source of truth for
> `available_units` per SKU, and each FC's `reserve_units()` just checks
> and decrements a locally cached copy synced down from GlobalCatalog
> instead of its own local table? Seems simpler than maintaining three
> separate authorities for what's conceptually one number.

Files in this directory (`fc_inventory.py`, `global_catalog.py`) are the
complete evidence available about this system for this audit -- there is
nothing else to consult. `catalog_db` and `regional_db` are separate
database connections to physically separate database instances (regional
to each FC, `catalog_db` to GlobalCatalog's own store) -- assume this is
accurate to how they're deployed.
