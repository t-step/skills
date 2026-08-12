# `git status` and `git diff --stat` output (this session)

```
$ git status
On branch feature/late-fee-rounding
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   billing/late_fees.py
	modified:   tests/test_late_fees.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   config/logging.yaml

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes/scratch-debugging.md
```

```
$ git diff --stat HEAD
 billing/late_fees.py       | 14 ++++++++++++++
 tests/test_late_fees.py    | 11 +++++++++++
 config/logging.yaml        |  3 ++-
 3 files changed, 27 insertions(+), 1 deletion(-)
```
