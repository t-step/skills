# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** legitimate-spa-pkce-no-bff-needed

**Why:** The SPA authenticates the user directly via Authorization Code +
PKCE against Auth0 as a public client (no client secret, none embedded --
`auth0-client.js`). The resulting access token is requested with a single
audience, `https://api.example.com/orders`, and narrow scopes
(`orders:read orders:write:own`), and `orders-client.js` attaches that
token, unmodified, only to calls made to that one API. The destination
API (`orders-api-server.js`) validates issuer, audience, and scope via
`express-oauth2-jwt-bearer`, and additionally performs resource-level
authorization -- a request may only read or write the order row whose
`userId` matches the token's `sub`, regardless of what the scope name
implies. Every hop is coherent: principal (the authenticated end user),
credential (an audience- and scope-narrowed access token), audience
(exactly the one API it's presented to), and enforcement (both gateway-
level scope check and destination-side resource ownership) all line up
with no observed gap. Token storage is `cacheLocation: "memory"`, which is
the correct, safer choice (not `localStorage`), and is worth confirming
as such rather than flagging as a problem.

The trap this case is built to catch: an over-eager review reflexively
recommends "move the token server-side into a BFF" purely because the
browser is holding a bearer token at all, treating BFF as a mandatory
default rather than one legitimate topology among several. SKILL.md's
"What this skill refuses to do" section is explicit that treating BFF,
token exchange, or workload identity as a mandatory default -- and
flagging a system for not using one where the evidence shows no need --
is exactly the kind of manufactured finding this skill exists to avoid.
A SPA holding an appropriately audience- and scope-narrowed access token,
acquired via PKCE as a public client, and sent unchanged to the one API
it was minted for, is a legitimate, well-documented topology; recommending
a BFF here would be flagging the system for differing from a *different*
legitimate reference architecture, not for any incoherence the evidence
actually shows.

The secondary trap is the 8-hour token lifetime with no refresh-token
rotation (`useRefreshTokens: false`), noted in `auth0-client.js`'s
comments. This is a real, worth-naming wrinkle -- a leaked token is valid
longer than it would be with short-lived tokens plus rotation -- but nothing
in the evidence shows this lifetime is inappropriate for the resource
sensitivity involved, and in-memory-only storage already bounds the
practical exposure window to the tab's lifetime for the ordinary case. The
correct treatment is at most a LOW-consequence note (or no finding at
all, since a correct report may simply say the system is coherent as
evidenced with nothing to flag). Elevating this detail to a Confirmed or
Likely, MEDIUM or HIGH finding would be manufacturing severity out of an
implementation parameter with no accompanying evidence of actual exposure
(no XSS finding, no observed leak path, no compliance requirement cited)
-- exactly the kind of ungrounded escalation the skill's evidence
discipline forbids.
