# Framework and vendor signals

Where to look for a hop's credential, audience, and authorization check in
common frameworks and auth SDKs -- consulted only when tracing a flow
through unfamiliar plumbing, not as a substitute for reading the actual
code. This is lookup detail in service of `SKILL.md`'s identity-flow
reasoning, not a parallel checklist to work through independently of it.
None of this is a defect list -- a pattern named here is a place to look,
not a thing to flag by its mere presence.

## Frontend frameworks and routers

- **React** -- look for a `useAuth`/`useSession`-style hook or context
  provider, route guards (a wrapper component or a router loader/guard
  that redirects unauthenticated users), and where the credential the
  hook exposes actually gets attached to outbound requests (see HTTP
  clients below). A guard that only conditionally renders UI, with no
  corresponding server-side check, is the classic UI-only-authorization
  shape this skill's Review mode looks for.
- **Angular** -- `CanActivate`/`CanMatch` route guards, an `HttpInterceptor`
  attaching tokens to outbound `HttpClient` calls, and an `AuthService`
  wrapping session state. Same UI-only caveat as React: a guard blocks
  navigation, not the API call underneath it.
- **Next.js** -- `middleware.ts` (runs at the edge, before a route
  handler; check what it actually validates versus merely checking for
  cookie presence), API routes vs. App Router route handlers (different
  runtimes, sometimes different auth wiring), and server components vs.
  client components (a server component can hold a credential a client
  component never should).

## HTTP clients

- **fetch / axios / Angular HttpClient** -- interceptors or wrapper
  functions are where a credential gets attached to a request; this is
  the actual point to check for audience-correctness of an outbound call,
  not the call site that invokes the wrapper.

## OAuth/OIDC SDKs

- **MSAL** -- `acquireTokenSilent` vs. `acquireTokenRedirect/Popup`; the
  `scopes` array passed to an acquire call is the requested audience/scope
  for *that specific downstream call* -- a call site requesting a broader
  scope than the operation needs is a scope-excess signal. Cache
  behavior (`account` selection) is where actor confusion in a
  multi-account browser session tends to hide.
- **Okta / Auth0** -- SDK callback/redirect handlers (where a code is
  exchanged for tokens), the configured `audience` parameter (which API
  the resulting access token is actually valid for), and whether the SDK
  is used in a SPA-token pattern (tokens held client-side) or behind a
  server-side callback (BFF pattern) -- these imply different appropriate
  architectures; neither is wrong by default.
- **NextAuth / Auth.js** -- the `jwt` and `session` callbacks are where a
  provider's token gets mapped into the app's own session token/claims;
  check what they carry forward (a raw upstream access token surviving
  into the session cookie is a common raw-forwarding point) and where
  server-side code reads that session versus a client component reading
  it directly.

## Gateways, middleware, and service mesh

- API gateway configs (Kong, Envoy, AWS API Gateway, Azure APIM, and
  similar) often perform audience/JWT validation, rate limiting, and
  routing-level authorization entirely outside application code -- when
  one is referenced in infrastructure config but its rules aren't in this
  repository, that's an "ambiguity requiring verification," not a missing
  check (see `SKILL.md`'s "Evidence discipline").
- Service mesh sidecar configs (Istio, Linkerd) can enforce mTLS and
  service-identity policy at the network layer, independent of anything
  the application code does.

## MCP and tool-calling surfaces

- An MCP server's tool definitions are the capability boundary --
  read/write and destructive/non-destructive should be distinguishable
  per tool, not folded into one broad "access" grant. Check whether the
  server validates the audience of a delegated credential it receives, or
  simply trusts whatever it's handed.
