/**
 * Orders API (Express). This is the only service that accepts the access
 * token minted for https://api.example.com/orders.
 */
const express = require("express");
const { auth, requiredScopes } = require("express-oauth2-jwt-bearer");
const db = require("./db");

const app = express();
app.use(express.json());

// Validates the token's signature against the tenant's JWKS, and rejects
// anything whose issuer or audience doesn't match this API. A token
// minted for a different Auth0 API (a different audience) is rejected
// here regardless of whether it's otherwise a valid, unexpired Auth0
// token.
const checkJwt = auth({
  issuerBaseURL: "https://example.us.auth0.com/",
  audience: "https://api.example.com/orders",
});

app.get(
  "/orders",
  checkJwt,
  requiredScopes("orders:read"),
  async (req, res) => {
    const userId = req.auth.payload.sub;
    const orders = await db.listOrdersForUser(userId);
    res.json(orders);
  }
);

app.get("/orders/:id", checkJwt, requiredScopes("orders:read"), async (req, res) => {
  const order = await db.getOrder(req.params.id);
  if (!order) return res.status(404).json({ error: "not found" });

  // Resource-level check: read is restricted to the order's own owner,
  // scope alone ("orders:read") doesn't grant access to every order.
  if (order.userId !== req.auth.payload.sub) {
    return res.status(403).json({ error: "not authorized for this order" });
  }
  res.json(order);
});

app.patch(
  "/orders/:id",
  checkJwt,
  requiredScopes("orders:write:own"),
  async (req, res) => {
    const order = await db.getOrder(req.params.id);
    if (!order) return res.status(404).json({ error: "not found" });

    // The scope name says "own", but the scope claim alone doesn't prove
    // *this* order belongs to the caller -- that's checked explicitly
    // here against the row itself before any write is applied.
    if (order.userId !== req.auth.payload.sub) {
      return res.status(403).json({ error: "not authorized for this order" });
    }

    const updated = await db.updateOrder(req.params.id, req.body);
    res.json(updated);
  }
);

module.exports = app;
