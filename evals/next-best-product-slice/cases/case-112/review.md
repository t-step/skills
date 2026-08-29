# Slice Review: Resumable sync (fieldbook sync --resume)

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- The 4 MB chunk-size constant is duplicated in `sync/uploader.py` and
  `sync/test_uploader.py`; fine for now, worth a shared constant if
  either is touched again.

## Out of scope
None.

## Verification evidence
```
$ pytest sync/test_resume.py -v
test_resume_after_dropped_connection PASSED
test_resume_skips_committed_chunks PASSED
test_resume_reindexes_local_observations PASSED
test_full_sync_unchanged_when_no_interruption PASSED
4 passed in 0.31s
```

## Reasoning
`fieldbook sync --resume` picks up an interrupted upload at the last
committed chunk instead of restarting from zero. Sync bookkeeping,
including a local `obs.sqlite` file of synced observations, is rebuilt
on completion so a later resume knows what has already been committed.
