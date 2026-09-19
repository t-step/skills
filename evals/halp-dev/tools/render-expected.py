#!/usr/bin/env python3
"""Renders the human-readable expectations for dev cases from the manifest (the only source of truth).

Usage: render-expected.py <manifest.json> [case-id ...]      (no ids: every case, separated by ---)
Prints Markdown to stdout: what was varied, what should change, what must stay invariant, each property with
its kind and whether it has a regex proxy, and any later turns. Nothing is stored; edit evals.json instead.
"""
import json, pathlib, sys

def render(e):
    out = [f"# Case {e['id']} ({e['family']}, twin/control: {e['twin'] or 'none'})", "",
           f"Varies: {e['varies']}", "", f"Should change: {e['should_change']}", "",
           f"Should stay invariant: {e['invariant']}", "", "## Properties", ""]
    out += [f"- {p['kind']}: {p['text']}" + (" [regex proxy]" if p.get("pattern") else " [judged]") for p in e["properties"]]
    if e["turns"]:
        out += ["", "## Later turns (sent to the same conversation)", ""] + [f"- {t['mode']}: {t['message']}" for t in e["turns"]]
    return "\n".join(out) + "\n"

if __name__ == "__main__":
    evals = json.loads(pathlib.Path(sys.argv[1]).read_text())["evals"]
    want = sys.argv[2:]
    picked = [e for e in evals if not want or str(e["id"]) in want]
    missing = set(want) - {str(e["id"]) for e in picked}
    if missing: sys.exit(f"render-expected: no such case id: {', '.join(sorted(missing))}")
    print("\n---\n\n".join(render(e) for e in picked), end="")
