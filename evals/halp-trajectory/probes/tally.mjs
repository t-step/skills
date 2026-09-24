// Grader-side behavioral probe for the tallybox project (same contract as ledgerkit.py). Usage: node tally.mjs (cwd = package root, a scratch COPY).
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";
const keyclass = (k) => Array.isArray(k) ? "tuple"
  : typeof k === "number" ? (k >= 190001 && k <= 999912 ? "int" : "other")
  : typeof k === "string" ? (/^\d{4}-\d{2}$/.test(k) ? "iso-str" : /^\d{6}$/.test(k) ? "yyyymm-str" : "other") : "other";
const SAMPLE = [{ date: "2026-08-30", amount: 1 }, { date: "2026-09-01", amount: 2 }, { date: "2026-09-02", amount: 3 }];
const out = {};
let rollup = null;
try {
  const { rollupByMonth } = await import(pathToFileURL(path.join(process.cwd(), "src/report.js")).href);
  const r = rollupByMonth(SAMPLE); rollup = r;
  const keys = r instanceof Map ? [...r.keys()] : Object.keys(r);
  const vals = r instanceof Map ? [...r.values()] : Object.values(r);
  const classes = [...new Set(keys.map(keyclass))].sort();
  out.key_class = classes.length === 1 ? classes[0] : "mixed:" + classes.join(",");
  out.values_ok = JSON.stringify(vals.slice().sort()) === "[1,5]";
  const e = rollupByMonth([]);
  out.empty = e instanceof Map ? `Map(${e.size})` : JSON.stringify(e);
} catch (e) { out.key_class = "error"; out.error = `${e.name}: ${e.message}`; }
const exp = { present: fs.existsSync("src/export.js") };
if (exp.present) {
  const text = fs.readFileSync("src/export.js", "utf8");
  exp.imports_vendored = /csv-lite/.test(text);
  exp.writer = exp.imports_vendored ? "vendored" : "local";
  try {
    const { rollupToCsv } = await import(pathToFileURL(path.join(process.cwd(), "src/export.js")).href);
    const rows = rollupToCsv(rollup ?? new Map([["2026-09", 5]])).split("\n");
    const col = rows[0].split(",")[0].trim().replace(/^"|"$/g, "").toLowerCase();
    exp.header_first = col === "month" || col === "period" ? col : "other:" + col.slice(0, 20);
    const k = (rows[1] ?? "").split(",")[0].trim();
    exp.key_col_class = !rows[1] ? "none" : /^\d+$/.test(k) ? keyclass(Number(k)) : keyclass(k);
  } catch (e) { exp.header_first = "error"; exp.error = `${e.name}: ${String(e.message).slice(0, 80)}`; }
}
out.export = exp;
console.log(JSON.stringify(out));
