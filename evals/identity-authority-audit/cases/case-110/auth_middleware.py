"""Auth middleware for the Orders MCP server: validates every incoming
tool-call request's bearer token before any tool dispatch happens.

The token presented here is not the support rep's original browser
session -- it is an OAuth token the agent platform obtained from the
internal STS via token exchange on behalf of a specific signed-in rep.
Its audience is this MCP server specifically (`orders-mcp`), not the
agent platform's own API or any other downstream service, and the
exchange preserves both the delegating rep's identity and the agent
platform's own identity as separate claims.
"""

import jwt

JWT_PUBLIC_KEY = "<STS public key, loaded at process start>"
EXPECTED_AUDIENCE = "orders-mcp"
EXPECTED_ISSUER = "https://sts.internal.example.com"


class AuthContext:
    """Everything a tool handler needs to know about who is acting on this
    call: the human whose authority is being delegated, the agent
    exercising it, and the scopes this specific delegation actually
    carries."""

    def __init__(self, delegating_user_id: str, agent_id: str, scopes: set[str], claims: dict):
        self.delegating_user_id = delegating_user_id
        self.agent_id = agent_id
        self.scopes = scopes
        self.claims = claims

    def has_scope(self, scope: str) -> bool:
        return scope in self.scopes


class AuthError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


def authenticate(bearer_token: str) -> AuthContext:
    """Validate signature, issuer, audience, and expiry before trusting
    anything in the claims. A token that fails any of these is rejected
    outright, before delegation or scope is even looked at."""
    try:
        claims = jwt.decode(
            bearer_token,
            JWT_PUBLIC_KEY,
            algorithms=["RS256"],
            audience=EXPECTED_AUDIENCE,
            issuer=EXPECTED_ISSUER,
        )
    except jwt.InvalidAudienceError:
        raise AuthError("invalid_audience", "token was not issued for orders-mcp")
    except jwt.InvalidIssuerError:
        raise AuthError("invalid_issuer", "token was not issued by the trusted STS")
    except jwt.ExpiredSignatureError:
        raise AuthError("expired_token", "token has expired")
    except jwt.InvalidTokenError:
        raise AuthError("invalid_token", "token failed validation")

    # act_as carries the human rep this call is delegated on behalf of.
    # client_id carries the agent platform's own identity. The STS's
    # token-exchange step keeps both as distinct claims rather than
    # collapsing them into a single "caller" identity.
    delegating_user_id = claims.get("act_as")
    agent_id = claims.get("client_id")
    if not delegating_user_id or not agent_id:
        raise AuthError(
            "incomplete_claims",
            "token missing delegating-user (act_as) or agent (client_id) identity claim",
        )

    scopes = set(claims.get("scope", "").split())
    return AuthContext(delegating_user_id, agent_id, scopes, claims)
