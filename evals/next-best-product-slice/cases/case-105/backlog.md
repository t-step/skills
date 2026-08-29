# Backlog — Craftline shop floor

1. **Let a shop-floor operator mark a work order complete from a tablet.**
   `docs/roles.md` describes the "shop-floor operator" role directly: "an
   operator completes a work order at the machine where the work happens,"
   and the shop's tablets are already used for other floor tasks. Today,
   completing a work order can only be done through the desktop supervisor
   app, so an operator has to walk to the office and ask a supervisor to
   do it on their behalf — observed directly in three shop visits by the
   product team, logged in `docs/shop-visit-notes.md`, and confirmed by
   the fact that the average work order isn't marked complete until 40
   minutes after the operator says it actually finished. A minimal first
   step: a single "mark complete" button in the existing tablet floor app,
   calling the already-verified `complete_work_order()`.

2. **Barcode label redesign.** No usage signal on record.

3. **Multi-shift handoff notes.** No usage signal on record.
