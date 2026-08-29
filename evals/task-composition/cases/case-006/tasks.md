# Tasks: Move Session Storage to a Shared Cache

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Introduce a `SessionStore` in `sessions/store.py`, backed by a
  distributed cache client, replacing the current in-process dict. The
  public interface (`get`, `set`, `delete`) stays the same, but the
  semantics change from process-local to shared and networked across
  worker processes, with a possible race window on concurrent
  read-modify-write to the same session key.
- T2: Migrate `api/login.py` to use T1's `SessionStore` instead of the
  old in-process store.
- T3: Migrate `api/cart.py` to use T1's `SessionStore` instead of the
  old in-process store.
- T4: Migrate `api/preferences.py` to use T1's `SessionStore` instead of
  the old in-process store.
- T5: Add a concurrency test, `tests/test_session_concurrency.py`, that
  drives T1's store from multiple concurrent workers and checks for lost
  updates on the same session key.

T2, T3, and T4 don't touch any of the same files as each other. No
priority is stated between them.
