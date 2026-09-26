# Context

The fulfillment platform on-call engineer messages you:

> Since Monday night's batch, `warehouse-svc`'s sync to Fulfillco (our 3PL
> fulfillment partner) has been failing completely -- every single order
> in every batch since Monday comes back `401 Unauthorized`. Fulfillco
> published a migration notice a couple weeks ago about retiring their
> old API-key auth in favor of request signing, effective the same night
> this started -- that's probably related, but I haven't confirmed it.
> Nothing else changed on our side this week. Can you get this sync
> working again?

You have `warehouse-svc`'s current `fulfillco_client.py` (the integration
code), `fulfillco_sandbox.py` (a local sandbox harness the fulfillment
platform team maintains to test against Fulfillco's documented contract
offline, without hitting their real endpoint), `run_sync.py` (runs a
batch through the client against the sandbox and reports results),
Fulfillco's migration notice, and the production sync log since Monday.
There is no ticket queue, chat transcript, or person to ask beyond this
message -- work from what you can find, and feel free to run the scripts
and edit the client code as your investigation requires.
