# Context

Excerpts from Auctions (`auction.py`) and Bidding (`bid.py`) -- two
separate services with separate databases. `auctions_client.py` and
`bidding_client.py` (the thin RPC clients each service uses to call the
other) are not included beyond the function signatures implied by the
call sites; treat anything not shown here as not available for this
review.

An incident note, forwarded for context:

> **Incident 2026-06-02:** Auction #9931 closed normally
> (`close_auction` ran, `status` -> `closed`, committed). The follow-up
> call to `reject_all_open_bids` timed out because Bidding's DB was
> under load at that moment. Nothing retried it. Three bids on auction
> #9931 stayed `submitted` for about six hours until an on-call engineer
> noticed and re-ran the RPC by hand. During that window, could any of
> those three bids have been `accept`-ed? Checked: no, `accept()` calls
> `get_auction_status` live and would have seen `closed` and refused --
> so the shared invariant (no bid accepted on a non-open auction) held
> throughout, even while the bids themselves sat in the "wrong" status
> for six hours. Raised in the retro but not resolved: should
> `reject_all_open_bids` have a retry/outbox mechanism, or is a human
> noticing and re-running it an acceptable failure mode given `accept()`
> already double-checks?
