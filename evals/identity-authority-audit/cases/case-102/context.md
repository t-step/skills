# Context

A platform engineer is trying to understand a request chain before adding
a new tool to it:

> A user action in our app ends up calling API A, which calls API B, which
> calls our internal MCP server, which invokes a tool. Somewhere along the
> way I noticed the exact same bearer token shows up in the `Authorization`
> header at every hop -- API A forwards what it received, API B forwards
> what it received, and so does the MCP server. Is that a problem, or is
> that just how these things normally work? I don't want to block this on
> a vague "forwarding tokens is bad" instinct if it's actually fine.

Files in this directory are the complete evidence available about this
system -- there is nothing else to consult.
