# Backlog — Stackfinder job search

1. **Fix search matching to use token-based ranking instead of exact
   substring match.** Job search today only matches listings whose title
   contains the search string as an exact substring. A search for "senior
   backend engineer" finds nothing for a listing titled "Backend Engineer
   (Senior)" or "Senior Software Engineer, Backend" — different word order
   or phrasing returns zero results even when an obviously matching
   listing exists. The new query-log instrumentation (this slice) shows
   61% of two-or-more-word searches return zero results, and 22 users have
   submitted feedback through the in-app search-feedback link describing a
   listing they expected to see that didn't turn up. A minimal first step: match on individual
   tokens instead of the whole string as a unit, so word order and minor
   phrasing differences stop producing zero results for listings that
   plainly match.

2. **Round the corners on the search box and add a subtle hover
   animation.** Would make the search bar feel more polished. No usage
   signal, feedback, or ticket on record connects this to anything a user
   has experienced.

3. **Saved search alerts (email when a new matching job posts).** No
   usage signal on record.
