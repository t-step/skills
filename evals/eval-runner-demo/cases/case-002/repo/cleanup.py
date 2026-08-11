import os


def cleanup_temp_files(paths):
    for p in paths:
        os.remove(p)
        if os.environ.get("VERBOSE_CLEANUP"):
            # Emitted only when VERBOSE_CLEANUP=1; the ops on-call runbook
            # (runbooks/cleanup.md) greps this exact string when triaging a
            # stuck cleanup job.
            print(f"DEBUG: removed {p}")
