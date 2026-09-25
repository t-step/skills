---
name: identity-authority-audit
description: >-
  Reconstructs and evaluates who is acting, with what authority, across
  every boundary a request crosses: principals, credentials, audiences,
  delegation, session transitions, authorization ownership. Three modes:
  Explain (reconstruct an unfamiliar system's identity story), Review
  (evidence-backed identity/authority issues in an architecture, PR, or
  implementation), Design (smallest change restoring one named authority
  property). Use for tracing how authority propagates through a
  browser/BFF/API/MCP/tool chain, checking a credential's audience against
  where it's presented, or an async job/delegated agent/forwarded token
  carrying authority it shouldn't. Sorts findings confirmed / likely /
  ambiguity requiring verification / deliberate tradeoff / org-specific
  convention -- never flags a system for merely differing from a
  preferred reference architecture. Framework-aware, not vendor-specific.
  Out of scope: crypto/TLS, password policy, OAuth/OIDC compliance,
  pentesting, vuln scanning, IdP admin, generic appsec.
---

# Identity Authority Audit

A request shows up with a bearer token, a session cookie, a signed
callback, or nothing at all, and the comfortable shortcut is to collapse
three different questions into one: is this authenticated. Authentication
(who or what is this), authorization (is this principal allowed to do
this specific thing, to this specific resource), delegation (whose
authority is actually being exercised right now -- the caller's own, or
someone else's handed forward), and platform trust (this request really
did come from the external system it claims to) are four different
facts. A valid credential answers only the first, and sometimes not even
that. This skill's only job is to keep those four facts separate across
every boundary a request crosses, and to say plainly where the story
becomes incoherent, where authority silently expands or changes hands,
and where the evidence simply doesn't say.

It does not redesign an identity platform, does not treat a system as
broken because it differs from a reference architecture, and does not
produce a maturity score. Given a request to fix what it finds, it names
the smallest change that restores a specific property and stops there.

## The unit of analysis: a hop, not a system

Auditing "the auth" of a system produces vague prose. Auditing one **hop**
-- one boundary a request or message crosses, from one component to the
next -- produces a checkable fact. For every hop, establish what the
evidence actually shows for each of:

- **Principal** -- who or what this hop claims to be acting on behalf of
  (a specific human, a service, a workload, an agent acting for a human,
  an agent acting on its own standing).
- **Credential presented** -- its concrete form (session cookie, bearer
  access token, ID token, signed request, mTLS certificate, service
  account key, workload-identity token, API key, none).
- **Audience** -- who the credential was actually issued for, versus who
  is receiving it at this hop. A credential minted for API A presented to
  API B is a different fact from one minted for API B, even if both
  requests "have a valid token."
- **Authority carried** -- whose authority the operation executes with at
  this hop: the original human's, a delegated/exchanged subset of it, the
  service's own standing, or something the evidence doesn't establish.
- **Enforcement point** -- where the decision to permit this specific
  operation is actually made and checked (frontend, gateway, middleware,
  application logic, destination resource, or nowhere observed).

A flow is a sequence of hops. Most incoherence in identity/authority
systems lives in the transitions between hops, not inside any single one
-- a credential minted for one audience surviving unchanged into a
context with a different audience, authority quietly widening from "what
this user may do" to "what this workload may do," or an authorization
decision made once at hop one being treated as still valid at hop four.

## Transition vocabulary

Name every transition using these terms rather than looser language --
they are what make a finding checkable instead of a feeling:

- **Delegation** -- one principal's authority is exercised by another on
  their behalf, and the mechanism is explicit (on-behalf-of, a delegated
  scope, an actor claim, a signed assertion of "acting as"). Ask whether
  the delegation is bounded (narrower than the delegator's full authority)
  and whether the original actor is still attributable in logs/audit
  trails at the far end.
- **Token exchange** -- a credential for one audience is traded for a
  differently-scoped, differently-audienced credential before crossing a
  boundary, rather than being forwarded unchanged.
- **Raw forwarding** -- a credential crosses a boundary completely
  unchanged. Not inherently wrong -- ask whether the audience and scope it
  was issued for actually still match where it has landed.
- **Authentication transition** -- establishing who is acting (login,
  session creation, silent token refresh, service-to-service handshake).
- **Session/step-up transition** -- an existing session's assurance level
  changes (fresh phishing-resistant MFA required for one operation while
  ordinary session assurance covers others).
- **Continuation** -- state that lets an interrupted flow resume (a
  redirect callback, a deep link, a signed notification, a resumed job) is
  presented and consumed later, potentially after the original session
  ended.
- **User-to-workload transition** -- an interactive action creates
  execution that outlives the browser session or the human's presence
  (a queued job, a scheduled task, a long-running agent run). Something
  now must own continued authority, and it is either the original user's
  (delegated forward, and for how long), the workload's own, or
  unaddressed.

## Read/write and capability boundaries

Authority is not a single yes/no per principal -- ask separately whether
a given credential, scope, or delegated capability covers **reads**
versus **writes**, and within writes, ordinary versus **sensitive**
operations (destructive, irreversible, financial, cross-tenant,
privilege-changing). The recurring failure this specifically catches: a
single broad capability -- one scope, one tool, one service account --
that happens to be able to invoke both a harmless read and a destructive
write, where nothing about how the capability was granted or is enforced
distinguishes the two. Two representations sharing authority is not
automatically wrong; it's wrong when nothing in the evidence shows it was
a decision rather than an accident of how the capability was scoped.

## Evidence discipline

Ground every claim in application code, middleware, routing, auth SDK
configuration, token validation logic, gateway/service-mesh
configuration, infrastructure-as-code, identity-provider configuration,
shared auth libraries, notification/webhook integrations, API
definitions, tests, architecture docs, deployment configuration, or
observed audit/logging behavior. State plainly what wasn't available to
inspect.

The load-bearing discipline: **an implementation not visible in the
repository is not evidence that it doesn't exist.** Audience validation,
scope enforcement, rate limiting, and authorization decisions routinely
live outside application code -- in an identity provider, an API gateway,
a service mesh, a shared platform library, a reverse proxy, cloud IAM
configuration, or a security policy the repository doesn't contain.
Prefer:

> "Audience validation is not visible in the inspected application path;
> verify whether the gateway performs it."

over:

> "Audience validation is missing."

The first is a finding with an honest boundary and a next step. The
second is a claim the evidence doesn't support and will read as
alarmist -- or wrong -- to anyone who knows the gateway handles it. This
applies symmetrically: don't credit a paved road as covering something
just because a shared library exists somewhere in the org; if this
specific path's use of it isn't observed, say that plainly too.

## Modes

Pick the mode the request actually calls for. Don't slide from Explain
into Review findings uninvited, and don't move into Design before the
model in front of you is actually reconstructed -- a proposed fix for a
system you haven't finished mapping is a guess wearing a design's
clothes.

### Explain

Use when someone is trying to understand an unfamiliar system's identity
and authority story. Reconstruct, don't judge or redesign yet -- an
Explain report can and should surface things that look questionable, but
frame them as unresolved ambiguities to note, not findings to fix.

Ground every claim in actual code and configuration; where the evidence
runs out, say so under "Unresolved ambiguities" rather than filling the
gap with a plausible guess.

Report:

```
# Identity & Authority: <system/target>

## System shape
<What this system is, its topology, and where this map starts and stops.>

## Identity flow
<Hop-by-hop table.>
| Hop | Principal | Credential presented | Audience | Authority carried | Enforcement point | Notes |
|---|---|---|---|---|---|---|

## Actors and principals
## Trust boundaries
## Credentials
## Audiences
## Resources
## Authorization owners
## Delegation transitions
## Authentication/session transitions
## Read/write distinctions
## Unresolved ambiguities

## Engagement profile
<Optional; see "Engagement profile" below. Omit fields the evidence
doesn't reach.>
```

### Review

Use for architecture reviews, PRs, implementation reviews, or an existing
system someone wants judged. Requires the Explain-level reconstruction
first -- do it inline if nothing already exists, reuse it if it does --
because a finding grounded in a flow you haven't actually traced is a
guess.

Look for, specifically:

- Ambiguous actor identity -- a hop where it's unclear which principal is
  actually acting.
- Missing audience checks -- a credential accepted at a boundary it
  wasn't issued for, per the evidence-discipline caveat above.
- Inappropriate credential forwarding -- raw forwarding across a boundary
  where the audience or scope no longer matches, versus forwarding that's
  audience-correct and therefore fine.
- Authorization at the wrong layer, or enforced only by the frontend --
  a control that exists in the UI with no equivalent check at the
  destination resource.
- User authority silently becoming workload authority -- especially
  across the user-to-workload transition named above.
- Unclear delegation, excessive scopes/capabilities, or reads and writes
  sharing authority nothing establishes was a decision.
- Sensitive operations proceeding without assurance appropriate to their
  consequence (no step-up where one is warranted).
- Redirect/continuation state, or an external platform's own signature or
  callback verification, mistaken for proof that a specific human user is
  authorized for the resource or mutation it names -- platform authenticity
  and resource authorization are different facts; a verified Teams/Slack
  callback or a signed deep link proves the *message* is genuine, never
  that its bearer may act on what it points to.
- Unclear asynchronous authority, or incomplete audit attribution (an
  action's log trail loses the original actor as it crosses hops).

Sort every finding into exactly one tier:

- **Confirmed issue** -- the evidence directly shows the problem: a
  credential accepted at a mismatched audience, a write endpoint with no
  server-side check behind a UI-only control, a token forwarded across an
  observed audience boundary with nothing narrowing it.
- **Likely issue** -- a short, defensible inference from what's observed,
  not a leap: "no code path in the inspected service narrows this token's
  scope before the outbound call, and no gateway config is present in this
  repo to check" is likely, not confirmed, because the gateway might do it
  elsewhere.
- **Ambiguity requiring verification** -- the evidence doesn't settle it
  either way, and the honest move is naming exactly what would settle it
  (see "Evidence discipline"). Report these under "Open questions /
  ambiguities," not "Findings" -- an item at this tier is not yet an
  issue to fix, it's a question to answer.
- **Deliberate tradeoff** -- the evidence shows a team chose this
  knowingly (a comment, ADR, ticket, or design note explaining why), even
  if it's a tradeoff you'd flag elsewhere. Report it as a tradeoff, not a
  defect, unless something else in the evidence shows the tradeoff's own
  stated conditions no longer hold.
- **Organization-specific convention** -- matches a documented org
  pattern (see "Organization-specific profile" below) that departs from
  generic guidance on purpose. Not a defect; name the convention it
  matches.

A single finding can mix a directly-observed structural fact with a
consequence that depends on something the evidence doesn't reach --
keep the two separate rather than letting the observed part's certainty
carry over to the part that isn't observed. If a finding's own "Unresolved
uncertainty" line names something that could change whether its stated
consequence actually holds (an unshown destination-side check, an
unobserved gateway), don't tag the finding Confirmed at that consequence
level -- tag the structural fact Confirmed and the consequence Likely, or
split the two into their own findings.

That splitting has a floor, and Confirmed/Likely -- at any level -- stops
being available below it: if the unresolved fact could determine whether
the claimed defect exists at all, not merely how severe, scoped, or
exploitable it is, the consequence is not a hedged finding, it's an open
question. Ask "could naming this missing fact resolve to 'no defect
here' about as easily as it resolves to 'defect confirmed'?" If yes,
nothing about it belongs in Findings under any tier, however hedged --
it belongs in "Open questions / ambiguities" below. Findings and open
questions are different report sections precisely so that admitting
uncertainty never has to be laundered through a Confirmed or Likely
label to have somewhere to go.

Within Confirmed and Likely findings only, a coarse consequence class may
help a reader triage, and nothing finer than this:

- **HIGH** -- plausible authority expansion, cross-tenant/cross-resource
  exposure, credential misuse, or a sensitive write reachable without
  appropriate authorization.
- **MEDIUM** -- meaningful ambiguity, fragile identity propagation,
  missing defense in depth, or a recurring operational failure mode.
- **LOW** -- maintainability, clarity, consistency, or an unused
  paved-road opportunity with no clear authority impact.

This is a coarse consequence label, not a score -- never combine it into
a number, and omit it entirely for Ambiguity/Tradeoff/Convention
findings, which aren't "issues" to rank by consequence at all. Order
findings by practical importance (Confirmed HIGH first), not by which
category came up first while reading.

A finding's next step names what would verify or falsify it -- a fact to
check, a config to read, a log to inspect -- not a mechanism or design
change. "Confirm whether the gateway validates audience before this
request arrives" is a Review-mode next step; "add audience validation at
the gateway" is a Design-mode recommendation. Reviewing a finding is not
an invitation to design its fix; leave that to a separate Design pass.

Report:

```
# Identity & Authority Review: <target>

## System shape
## Identity flow
<Reused from an existing Explain report, or produced inline -- say which.>

## Findings
<Confirmed, Likely, Deliberate-tradeoff, and Organization-specific-
convention items only. An item earns Confirmed or Likely only if it
clears the admission rule above -- no unresolved fact left that could
determine whether the claimed defect exists at all.>
### <short finding name> -- <tier>[, <HIGH|MEDIUM|LOW> if Confirmed/Likely]
- What was observed:
- Why it matters:
- Evidence:
- Unresolved uncertainty:
- Next verification step:
(repeat, ordered by practical importance)

## Open questions / ambiguities
<Ambiguity-requiring-verification items -- including anything that would
otherwise have entered Findings as Confirmed/Likely except that an
unresolved fact could determine whether the defect exists at all. "None."
is a complete answer when nothing is genuinely unresolved at this level.>
### <short item name>
- What is visible:
- What remains unknown:
- What evidence would resolve it:
(repeat)

## Paved-road opportunities
<Existing shared mechanisms -- auth middleware, gateway, token-exchange
helper, entitlement service, audit library -- the implementation could
reuse, and whether it follows / intentionally extends / bypasses /
duplicates / appears unaware of each one found. "None identified." if the
target has no applicable paved road in evidence.>

## Unknowns
<Facts that would matter but aren't establishable from inspected
evidence and aren't themselves a candidate finding -- named, not silently
dropped.>

## Engagement profile
<Optional; see below.>
```

A target with no confirmed or likely issues is fully served by a short
report saying so -- padding it with speculative findings to look thorough
is worse than an honest "coherent as evidenced, nothing to flag." The
same applies to Open questions / ambiguities: "None." is a complete
answer when nothing in evidence is genuinely unresolved.

### Design

Only after the model above exists -- reconstructed here, or already
produced by a prior Explain/Review pass being reused. Design without that
grounding is a guess.

Prefer the smallest coherent change. Do not respond to a single finding
by redesigning the identity platform, and do not bundle every lever below
into one recommendation because the list exists -- name only the levers a
specific finding actually calls for:

- Moving token ownership server-side.
- Introducing token exchange or on-behalf-of delegation.
- Narrowing audience or scope.
- Using workload identity in place of a forwarded or shared user
  credential.
- Separating read and write capabilities.
- Adding destination-side resource authorization.
- Adding step-up authentication for a specific sensitive operation.
- Preserving actor attribution through a delegation or exchange.
- Improving continuation-state handling (making clear it carries
  navigation intent, not authorization).
- Adding explicit agent delegation (a named, bounded capability an agent
  acts under, distinct from the human's full authority).

Every proposed change must name the specific property it restores, tied
to the specific finding that motivated it -- not a generic-sounding
prescription. Contrast:

> "Exchange the incoming user credential for an API-B-specific
> credential."

against:

> "API B currently accepts authority intended for API A. Exchange the
> credential so the downstream audience and delegated authority are
> explicit."

The second names the finding, the boundary, and the property restored;
the first is a mechanism recommendation with nothing to check it against.
Write every Design recommendation the second way.

Report:

```
# Identity & Authority Design: <target>

## Model referenced
<The Explain/Review report this builds on, or the reconstruction done
inline before proposing anything.>

## Proposed change(s)
### <change>
- Change: <the smallest coherent change>
- Restores: <the specific property, in the finding's own terms>
- Where: <exact boundary/component>
- Residual scope: <what this change deliberately does not address, if
  anything>
(repeat only if more than one finding genuinely needs its own change)

## Explicitly not proposed
<Levers considered and deliberately excluded, and why -- guards against
reflexively bundling every lever in the list above into the answer.>
```

## Framework awareness without framework capture

Trace flows through common conventions -- React/Angular/Next.js routing
and route guards; fetch/axios/Angular HttpClient and their interceptors;
middleware and API interceptors; BFF routes; common OAuth/OIDC SDKs
(MSAL, Okta, Auth0, NextAuth/Auth.js) and their callback/session
handling -- because tracing a flow through unfamiliar framework plumbing
is exactly where an audit stalls out or guesses. But framework knowledge
here only serves the identity-flow reasoning above; this is not a React
auth skill, an Angular auth skill, an MSAL skill, an Okta skill, an Auth0
skill, or a NextAuth skill, and it should never accumulate into one.
Vendor- or framework-specific lookup detail belongs in
`references/framework-signals.md`, consulted when it materially helps
locate where a hop's credential or authorization check actually lives --
not inlined into the core reasoning above.

## Enterprise paved roads

Before treating a bespoke implementation as defective, check for an
existing shared mechanism it could be using: shared auth middleware,
enterprise SSO wrappers, API gateways, authorization libraries, token
exchange helpers, service-identity libraries, notification platforms,
redirect services, entitlement services, policy engines, standard BFF
libraries, audit libraries. For each one found in evidence, determine
whether the target follows it, intentionally extends it, bypasses it,
duplicates it, or shows no sign of knowing it exists. A bespoke
implementation is not automatically wrong -- the useful question is
whether it's solving an already-solved problem with incompatible
authority semantics, or has a real reason not to use the paved road.

## Engagement profile

Optional, compact, unscored metadata describing the system reviewed --
useful for comparing across engagements, not for grading this one. Emit
only the fields the evidence actually reaches; never fill a field with a
guess to make the block look complete.

```yaml
system_role: internal_workflow
frontend: react
topology: browser_bff_api
principal_mix:
  - human
  - service
identity_source: enterprise_sso
authz_model: rbac_plus_resource
delegation: obo
entry_points:
  - browser
  - teams
ownership_shape: multi_team
async_continuation: true
agentic_surface: none
first_auth_ambiguity: redirect
```

Other useful dimensions, when evidence reaches them: tenancy model,
interaction origins, session lifetime, read/write asymmetry,
authentication assurance, credential-management model, workload identity,
external integrations and their density, legacy depth, platform
dependence, audit requirements, regulatory/data sensitivity. This is
descriptive metadata, not a maturity score -- never reduce it to a single
number or rating.

## Organization-specific profile

This skill works with no organization-specific input. When one is
available, it can state things generic reasoning can't know on its own:
approved identity providers, the standard BFF/session model, standard API
validation middleware, the approved OBO/token-exchange implementation,
the service-identity mechanism, notification/deep-link conventions,
step-up requirements, read/write policies, MCP/tool authorization
conventions. Use it to resolve what would otherwise be an "organization-
specific convention" or "ambiguity requiring verification" finding into a
concrete match-or-mismatch against the stated convention.

Never hard-code an organization's specific convention into this skill's
own reasoning (e.g. "all BFFs must use library X") -- that belongs in a
separate profile document, loaded only when supplied, per
`references/organization-profile-template.md`. A generic finding must
still make sense read with no profile in hand.

## What this skill refuses to do

Even when a request bundles it in:

- Treat BFF, token exchange/OBO, or workload identity as mandatory
  defaults, and flag a system for not using one where the evidence shows
  no need for it.
- Manufacture a finding because a system differs from a preferred
  reference architecture, rather than because the evidence shows an
  actual incoherence or hazard.
- Claim an implementation is missing because it isn't visible in the
  inspected repository -- see "Evidence discipline."
- Produce a numeric score, maturity rating, or anything resembling "7.4/10
  auth maturity." The engagement profile is descriptive, not a grade.
- Treat two representations sharing read/write authority, or forwarded
  credentials, or a bespoke implementation as inherently wrong -- each is
  a question to answer from evidence, not a default verdict.
- Redesign an entire identity platform in response to one finding, or
  bundle every Design lever into a recommendation a single finding didn't
  call for.
- Perform cryptographic implementation review, TLS configuration review,
  password-strength policy review, full OAuth/OIDC protocol compliance
  auditing, penetration testing, vulnerability scanning, identity-provider
  administration, secrets scanning, generic application security review,
  or OWASP coverage unrelated to identity/authority. Those belong to
  other tools or skills; name the boundary and stop rather than drifting
  into them.
- Silently resolve a genuine ambiguity toward whichever answer makes the
  report tidier. Report it as an ambiguity requiring verification, or as
  unresolved.

## How this composes with neighboring skills

- **`change-review`** judges merge-readiness for a bounded diff. When a
  reviewed change's correctness turns on an identity/authority fact --
  a newly forwarded header, a widened scope, a new redirect target --
  `change-review` should defer to this skill's Review mode for that
  judgment, the same way it already defers to `domain-orientation` or
  `state-ownership-audit` for other semantic facts, rather than
  re-deriving identity/authority reasoning inline. This skill doesn't
  issue a merge verdict.
- **`state-ownership-audit`** determines who may write a piece of
  *state*. This skill determines who may authorize an *action* at a
  boundary. They overlap where an authorization decision depends on a
  fact's current owner (e.g., only the account's current owning service
  may approve a transfer) -- reuse that skill's ownership map as an input
  rather than re-deriving write authority here.
- **`lifecycle-audit`** owns full state/transition/invariant
  characterization for an entity with its own lifecycle. When a
  user-to-workload transition or an async job's authority question turns
  out to need the job's own state-machine mechanics characterized beyond
  who owns continued execution, name it as a lifecycle-audit candidate
  rather than redoing that analysis here.
- **`spec-pressure-test`** pressure-tests a not-yet-built spec for
  undecided questions, including ownership. An undecided spec's
  identity/authority model is that skill's territory; this skill runs on
  a system whose model is decided enough to reconstruct (Explain/Review),
  or that a Design change is being proposed for.
- Cryptographic, TLS, dependency/vulnerability, and general
  OWASP/application-security concerns belong to a general-purpose
  security review tool or skill, not this one -- see "What this skill
  refuses to do."

If a request bundles a legitimate identity/authority question with one of
these, or with a request to redesign the whole platform, say so plainly
and deliver the part that's actually this skill's job.
