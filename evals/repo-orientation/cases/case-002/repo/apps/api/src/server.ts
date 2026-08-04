import express from "express";
import { formatCurrency, type Order } from "@acme/core";

const app = express();

app.get("/orders/:id", (req, res) => {
  const order: Order = { id: req.params.id, total: 1999 };
  res.json({ ...order, formatted: formatCurrency(order.total) });
});

app.listen(3000);
