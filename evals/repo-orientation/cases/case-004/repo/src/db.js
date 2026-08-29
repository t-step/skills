const Database = require("better-sqlite3");

const db = new Database("orders.sqlite");

db.exec(`
  CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    total_cents INTEGER NOT NULL
  )
`);

module.exports = db;
