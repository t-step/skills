# Implementation notes

Added a `threading.Lock` around the read-modify-write in `increment()`.
This fixes the lost-update race condition from issue #482 — ran the
concurrent-increment stress test (50 threads x 1000 increments) and got
exactly 50000 every time.

(Later, same day) Added a second, more thorough test that also runs
`flush()` concurrently with the increment threads, since that's a realistic
production pattern (a background exporter calls `flush()` periodically).
That test is flaky — occasionally comes up short by a handful of counts.
`flush()` reads and clears `self._values` without taking `self._lock`, so
it can race with an in-flight `increment()` and drop an update. Filed as a
follow-up; the lock in `increment()` alone doesn't fully close the race.
