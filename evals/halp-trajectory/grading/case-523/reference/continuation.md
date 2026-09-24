# Natural continuation after k (reference only)
Trajectory model45, messages > 121 (traj.py steps 50-62):
- 50-54 (msgs 123-134): reverts (`git checkout -- src/_pytest/python.py`), re-applies the same one-line removal via a script, re-runs its scratch tests; the package-skip script still shows `1 failed, 1 skipped` (and still prints "PASSED").
- 55-57 (msgs 135-143): reverts again and rewrites `Package.collect()` to buffer `collected_items`, and call `self._mount_obj_if_needed()` only `if collected_items:` before yielding them ("only import `__init__.py` if there are test files"). Scratch run now shows `2 skipped` for the package-marks case and no import of `foopkg/__init__.py`.
- 58-62 (msgs 144-149): cleans scratch files, runs the issue repro once more (passes), submits `src/_pytest/python.py` (+15/-2). The real test-suite was never run (interpreter issues).
Model46 (other run) chose A by a different route: `Session._visit_filter` returns `f.check(file=1) and f.basename != "__init__.py"` (1 line).
Upstream gold (human): B. Removes `_mount_obj_if_needed` and makes `PyobjMixin.obj` lazily attach markers again, deletes the `Module.__init__` `_ALLOW_MARKERS=False` special case, and its test patch adds `test_does_not_eagerly_collect_packages`, `test_does_not_put_src_on_path` and DELETES `test_skip_package`.
