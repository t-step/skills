# Repo instructions (excerpt, checkout/)

- New functions need a test.
- Changes to `receipt.py` need a test asserting the printed/returned receipt
  text, since it has no other consumer that would catch a formatting
  regression.
