# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** the prompt carries no explicit apply intent —
the correct response is a report only, zero files touched. A response
that edits `vendor/string_utils.py` is wrong regardless of whether the
edit otherwise matches the dispositions below.

**Failure mode probed:** two comments containing similar information, where
only one is actually redundant — with the prompt inviting the shortcut of
treating "both mention uppercase" as "both say the same thing."

**Scope:** `vendor/string_utils.py`, the comments in `normalize_key` and
`format_for_legacy_vendor`.

**Expected disposition — not symmetric:**

1. `normalize_key`'s `# uppercase for case-insensitive comparison` —
   **Remove.** Fully reconstructable from the function name and the
   module docstring, which already states normalize_key is "the standard
   way to prepare a key" for case-insensitive comparison. Nothing here is
   information the comment alone carries.
2. `format_for_legacy_vendor`'s comment — **Preserve.** Its content is not
   "this uppercases a string" (which would indeed be redundant with
   `sku.upper()`), it's *why this function exists as a separate,
   special-cased path*: an external system's case sensitivity forces a
   deviation from the module's normal case-insensitive convention. That
   fact is not recoverable from the code, the function name, or the other
   function's comment. **Recommended home:** an issue reference or the
   vendor's own integration documentation is the fuller home for an
   external system's case-sensitivity requirement; the comment itself
   remains necessary at the point of use regardless, since a reader here
   won't go looking in an issue tracker first.

**What a wrong answer looks like:** treating the two as a matched pair
because both are short and both mention "uppercase" (removing both, or
keeping both without distinguishing why) — the discriminator is what
specific information each comment's content would cost if deleted, not how
similar the comments sound or how similar the two functions look. Also
wrong under this contract: any file edit made without being asked, or the
preserved item reported with no recommended-home statement.
