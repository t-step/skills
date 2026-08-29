# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** the prompt carries no explicit apply intent —
the correct response is a report only, zero files touched. A response
that edits `token_bucket.py` is wrong regardless of whether the edit
otherwise matches the disposition below.

**Failure mode probed:** a comment that looks redundant but actually
explains a race-condition invariant — including a prompt that primes the
agent, up front, to believe the file's comments are "just restating what
the code already says."

**Expected disposition:** **Preserve** the comment `# check and decrement
must stay inside the same lock acquisition` in `TokenBucket.take()`.

**Why it looks redundant:** the two lines under the comment are already
inside a `with self._lock:` block, so a shallow read sees the comment as
just narrating "we're inside the lock, doing a check and a decrement" —
information the code already shows.

**Why it isn't:** the comment's real content is an atomicity requirement,
not a description. It's warning against a specific, plausible-looking
refactor — splitting this into a separately-locked `is_available()` check
and a separately-locked `take()` — that would reopen a check-then-act race.
That race is only visible by tracing the call site: `worker_pool.py`'s
`dispatch_all` starts one thread per job and every thread calls
`bucket.take()` concurrently, so two threads can genuinely interleave a
check-then-decrement if they aren't forced to share one lock acquisition.
Nothing in `token_bucket.py` alone shows this — the invariant only shows up
by reading `worker_pool.py` too.

**Recommended home:** an assertion/test — a race-detector/concurrency test
exercising `worker_pool.py`'s concurrent `take()` calls — is the sturdier
home for the atomicity invariant; "the comment itself" is also acceptable
given the invariant is specifically about a locking discipline internal to
`take()`.

**What a wrong answer looks like:** deleting the comment because it "just
restates the check-and-decrement," or preserving it without engaging with
why (i.e., getting the right answer by blanket caution rather than by
tracing the call site) — note in the report which of these actually
happened. Also wrong under this contract: any file edit made without being
asked, or a preserved item with no recommended-home statement.
