const express = require("express");
const db = require("./db");

const app = express();
app.use(express.json());

app.get("/orders/:id", (req, res) => {
  const row = db.prepare("SELECT * FROM orders WHERE id = ?").get(req.params.id);
  res.json(row ?? {});
});

app.listen(3000);
