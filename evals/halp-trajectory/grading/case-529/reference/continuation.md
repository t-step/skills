# What model46 did after k=14 (reference data only, not an oracle)
- Step 15-17: grepped `refs.test.js` for cleanup tests (none); tried `karma --grep refs` (pattern matched nothing; the full suite ran instead, all green).
- Step 18-24: re-read the diff, looked at `mangle.json` to check `_refCleanup` gets mangled (regex `^_[^_]` covers it).
- Step 25-27: wrote `patch.txt`, re-ran the full suite (1173 passed), submitted. Tree never changed after step 11. No test for the feature was written; no stable-ref re-render was ever tried.
- Contrast, model45 (same issue, different trajectory): applyRef with `refVNode` + in `diffChildren` `else if (oldVNode._refCleanup) childVNode._refCleanup = oldVNode._refCleanup;` (the transfer that WIP lacks), 48 steps, several karma runs in Chrome.
- Upstream (human) fix: cleanup stored on the ref function as `ref._unmount`, in `src/diff/index.js` and a `RefCallback` type change; tests added to `test/browser/refs.test.js`.
