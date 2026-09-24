# Natural continuation (model45, immutable-js-2005) -- reference data only, not an oracle
k13 -> 36: agent notices repro3 still gives different hashes for differently-ordered sets, digs (debug*.js) and finds
`OrderedMap.__iterate` returns 4 while size is 3 (tombstone), patches OrderedMap.__iterate to count live entries (step 33), rebuilds, repro_final passes.
Step 37: `npm test` -> jest: 1 failing `OrderedSet > respects order for equality` (expected false, received true).
Steps 38-41: reads __tests__/OrderedSet.ts, re-reads the issue, concludes the bug is same-order-different-hash, `git checkout src/utils/deepEqual.js src/CollectionImpl.js`.
Steps 42-44: rebuild, `npm test` all green (jest + tstyche). Submits OrderedMap.js only (reference/agent-final.patch).
Upstream gold (reference/gold.patch): hashCollection uses `collection.size` instead of the iterate return value (+CHANGELOG), tests in reference/gold-test.patch.
