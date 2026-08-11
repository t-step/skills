# Backlog — Palette filters

1. **Let users save and reload a named filter view.** `docs/product-scope.md`
   describes saving a filter combination and returning to it later as
   part of the product's intended scope. Today, nothing in the product
   lets a
   user do this — filter state only persists implicitly, one item at a
   time, through the unrelated "recently viewed" sidebar. 7 users have
   asked about this directly in support chats over the last six weeks. A
   minimal first step: a "Save this view" button on the existing filter
   bar, using `ViewSerializer` (already verified) to persist it under a
   name the user chooses, and a way to reload it from a simple list.

2. **Shareable view links.** No usage signal on record.

3. **Filter usage analytics for admins.** No usage signal on record.
