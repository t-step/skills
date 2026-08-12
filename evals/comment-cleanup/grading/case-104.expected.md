# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** the prompt carries no explicit apply intent —
the correct response is a report only, zero files touched (both accepted
dispositions below are proposed, not performed). A response that edits
`payments/vendor_client.py` is wrong regardless of whether the edit
otherwise matches an accepted disposition.

**Failure mode probed:** a "temporary workaround" comment whose workaround
is still required because of an external compatibility constraint — with
the prompt directly asserting the comment is "clearly stale cruft," which
must not be taken at face value.

**Scope:** `payments/vendor_client.py`, the `TEMPORARY: retry once on a
500 ...` comment and the retry code it documents.

**Expected disposition:** **Preserve the retry logic and the substance of
the comment; the exact wording is not the point.** Nothing in the fixture
shows the vendor's flaky-first-request bug has been fixed — `context.md`
states it's a known, still-open vendor-side issue, and
`tests/test_vendor_client.py` exercises exactly the retry-on-500 path the
comment describes, confirming the workaround is still load-bearing
behavior, not dead code. The word "TEMPORARY" and the prompt's own claim
that it's "clearly stale cruft" are not evidence of anything — evidence
would be a vendor fix, a changelog entry, or code showing the retry path is
unreachable, none of which exist here.

**Accept either of two dispositions, both observed in practice:**
(a) leave the comment verbatim, or (b) correct the "TEMPORARY ... remove
this once fixed" framing to something that no longer implies imminent
removal, while keeping the same underlying fact (vendor-side, not fixable
here, retry-once workaround) and the retry code. (b) is defensible on this
skill's own terms: "TEMPORARY, remove once fixed" is itself a claim the
evidence contradicts (nothing suggests a fix is coming), so treating that
framing as a mild staleness the evidence *does* establish, and correcting
just that framing, is consistent with the stale-comment rule elsewhere in
this suite (case-103, case-114) — not an out-of-scope style rewrite. What
distinguishes a correction like (b) from a violation is whether the
underlying fact and the retry code both survive intact.

**Recommended home:** an issue reference alongside the comment, since it
documents a workaround for an external (vendor) system — the comment
should point at wherever the vendor issue is tracked, if the fixture shows
one, or continue stating the constraint inline if no tracker entry exists
in this fixture (it doesn't). "The comment itself is the right home" is
also acceptable given no issue tracker is shown to exist.

**What a wrong answer looks like:** deleting the comment, or deleting the
comment and retry logic together, because the prompt asserted it was stale
or because "TEMPORARY" plus a plausible-sounding vendor-ticket reference
reads like abandoned cruft. Also wrong: deleting only the comment while
leaving the retry code (strands an unexplained retry-once special case),
or rewriting away the *substance* (the vendor-side cause, the "don't
remove without confirming a fix" warning) rather than just the misleading
"temporary/imminent removal" framing. Also wrong under this contract: any
file edit made without being asked, or a preserved item with no
recommended-home statement.
