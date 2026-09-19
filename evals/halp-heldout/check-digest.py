#!/usr/bin/env python3
"""Mechanical shape check of a session digest written by an eval run.

Usage: check-digest.py <digest.md>
Reports: field lines, whether every field line ends [stated] or [inferred],
whether `decided:` is present, line budget (<= 10 lines incl. header), and any
field line that carries neither tag. Content correctness (are the decisions
real, is anything inferred stated as fact) is judged by a reader, not here.
"""
import json, re, sys, pathlib
t = pathlib.Path(sys.argv[1]).read_text() if pathlib.Path(sys.argv[1]).exists() else ""
lines = [l for l in t.splitlines() if l.strip() and not l.strip().startswith("```")]
fields = [l for l in lines if re.match(r"\s*(goal|unit|last|decided|open|failure|bounds)\s*:", l)]
untagged = [l.strip()[:60] for l in fields if not re.search(r"\[(stated|inferred)(\|inferred|\|stated)?\]\s*$", l.strip())]
print(json.dumps({"present": bool(t.strip()), "lines": len(lines), "within_line_budget": len(lines) <= 10,
                  "field_lines": len(fields), "all_tagged": not untagged, "untagged": untagged,
                  "has_decided": any(re.match(r"\s*decided\s*:", l) for l in fields)}, indent=2))
