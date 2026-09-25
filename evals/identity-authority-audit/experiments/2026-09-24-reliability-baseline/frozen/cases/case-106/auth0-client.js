/**
 * Auth0 SPA client setup for the order-management frontend.
 *
 * This app is registered in Auth0 as a Single Page Application (public
 * client): no client secret is issued to it, and none is embedded here.
 * Login uses the Authorization Code flow with PKCE, which is the standard
 * Auth0 SPA SDK behavior -- the SDK generates the code_verifier/challenge
 * pair itself.
 */
import { Auth0Client } from "@auth0/auth0-spa-js";

export const auth0 = new Auth0Client({
  domain: "example.us.auth0.com",
  clientId: "spa-orders-frontend-8h2j",
  authorizationParams: {
    redirect_uri: window.location.origin + "/callback",
    // Single audience: the Orders API, and nothing else. This app never
    // requests a token for any other API.
    audience: "https://api.example.com/orders",
    // Narrow, resource-scoped permissions only -- no admin/global scopes.
    scope: "openid profile orders:read orders:write:own",
  },
  // Tokens and the Auth0 session are kept in memory only. Explicitly not
  // "localstorage" -- an in-memory cache does not survive a page reload
  // (the SDK silently re-authenticates via an iframe on load instead) and
  // is not reachable by other tabs or by a persisted-storage read after
  // the tab closes.
  cacheLocation: "memory",
  useRefreshTokens: false,
});

/**
 * Returns a valid access token for the Orders API, silently renewing via
 * the Auth0 session (iframe-based, since useRefreshTokens is false) when
 * the in-memory token has expired.
 *
 * Note: this tenant's API (https://api.example.com/orders) is configured
 * in the Auth0 dashboard with an 8-hour access token lifetime, and this
 * app does not use refresh token rotation. In exchange for one fewer
 * moving part (no refresh token to store or rotate at all), a token that
 * leaks during its lifetime -- e.g. via an XSS bug elsewhere in the app --
 * stays valid for up to 8 hours rather than a shorter window.
 */
export async function getOrdersApiToken() {
  return auth0.getTokenSilently({
    authorizationParams: {
      audience: "https://api.example.com/orders",
      scope: "orders:read orders:write:own",
    },
  });
}
