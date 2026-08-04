# Accepted Slice: Support "-word" exclusion syntax in search queries

## Goal
parse_query() should support a leading "-" on a token to mean "exclude
results containing this term" (e.g. "cat -dog" means results must
contain "cat" and must not contain "dog"), added as a new "must_not"
list in the returned filter dict.

## Why now
Users have asked for exclusion filtering in support tickets for over a
year; it's a small, self-contained addition to the existing parser and
doesn't require touching the search index itself, only how the query
string becomes a filter dict.

## What this slice proves
That parse_query() correctly separates excluded terms into a new
"must_not" list, and that existing must/or/fields parsing is
unaffected.

## Explicit non-goals
Does not add exclusion support for quoted phrases (e.g. -"hello
world"), does not add exclusion for field filters (e.g. -status:open),
does not touch how the search index consumes the returned filter dict.

## Acceptance evidence
A test showing "cat -dog" produces must=["cat"], must_not=["dog"], and
that the existing tests in tests/test_query_parser.py still pass
unchanged (parse_query's existing return shape gains a new key but
doesn't lose or rename any existing ones).
