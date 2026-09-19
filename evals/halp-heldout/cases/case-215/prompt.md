You are the coding agent in a Claude Code session working in the repository at `repo/` (a sibling of this file).

**Session so far** (everything you remember of it):

- You wrote the provider client with a retry loop for plan task 4.
- You ran the test:

    $ go test ./internal/provider
    --- FAIL: TestRetryDoesNotDuplicate
        client_test.go:23: expected 1 transfer recorded by fake provider, got 3
    FAIL

The user now types:

    /halp
