/**
 * Thin fetch wrapper the SPA uses for every call to the Orders API. This
 * is the only place in the frontend that attaches the access token to an
 * outbound request.
 */
import { getOrdersApiToken } from "./auth0-client";

const ORDERS_API_BASE = "https://api.example.com/orders";

async function ordersApiFetch(path, options = {}) {
  const token = await getOrdersApiToken();

  const resp = await fetch(`${ORDERS_API_BASE}${path}`, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!resp.ok) {
    throw new Error(`Orders API request failed: ${resp.status}`);
  }
  return resp.json();
}

export function listMyOrders() {
  return ordersApiFetch("/orders?mine=true", { method: "GET" });
}

export function getOrder(orderId) {
  return ordersApiFetch(`/orders/${orderId}`, { method: "GET" });
}

export function updateOrder(orderId, patch) {
  // The Orders-API-scoped token above is attached here exactly as it was
  // acquired -- this wrapper never widens, substitutes, or forwards it
  // anywhere other than https://api.example.com/orders.
  return ordersApiFetch(`/orders/${orderId}`, {
    method: "PATCH",
    body: JSON.stringify(patch),
  });
}
