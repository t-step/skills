# Context

Message from a security-conscious engineer on the Orders frontend team,
ahead of a wider platform security review:

> Our order-management SPA authenticates the user directly in the browser
> with Auth0 (Authorization Code + PKCE, it's a public client, no client
> secret anywhere in the frontend). The access token it gets back is only
> good for our own Orders API. That token gets attached to our fetch calls
> to the Orders API and nothing else. There's no backend-for-frontend in
> front of it -- the SPA talks to the API directly. Someone on the review
> raised an eyebrow at "the browser is holding a bearer token" and asked
> whether we need to put a BFF in front of this before it ships more
> broadly. Before I push back, I want an actual identity/authority review
> of what we have, not just a gut reaction to "token in the browser."

Files in this directory (`auth0-client.js`, `orders-client.js`,
`orders-api-server.js`) are the complete evidence available about this
system for this review -- there is nothing else to consult.
