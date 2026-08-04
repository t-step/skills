# Implementation notes

Straightforward retry loop, 3 attempts, 1s delay, re-raises the last
`ConnectionError` if all attempts fail. Both tests pass.
