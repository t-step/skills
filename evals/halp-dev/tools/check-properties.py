#!/usr/bin/env python3
"""Evaluates the regex-proxy properties of one development case against a saved reply.

Usage: check-properties.py <manifest.json> <case-id> <run-dir>
Reads <run-dir>/outputs/response.md (turn 1) and response-t2.md / response-t3.md when present.
For each property: MUST with a pattern passes if it matches; MUST_NOT with a pattern passes if it does not;
"scope_words" limits matching to the reply's first N words. Properties without a pattern are reported as
"judged" (a reader decides). A trailing 'Session report' receipt (an operator-instruction artifact) is stripped.
The regexes are proxies for behavior, not wording requirements: a proxy miss is a prompt to read the reply, not a verdict.
"""
import json, pathlib, re, sys
manifest, cid, run = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
entry = next(e for e in json.loads(pathlib.Path(manifest).read_text())["evals"] if str(e["id"]) == cid)
def load(name):
    f = run / "outputs" / name
    if not f.exists(): return None
    t = f.read_text(); m = re.search(r"(?m)^Session report\b", t)
    return t[:m.start()] if m else t
replies = {1: load("response.md"), 2: load("response-t2.md"), 3: load("response-t3.md")}
out = []
for p in entry["properties"]:
    text = replies.get(p.get("turn", 1))
    r = {"id": p["id"], "kind": p["kind"], "text": p["text"]}
    if text is None: r["result"] = "no-reply"
    elif "pattern" not in p: r["result"] = "judged"
    else:
        scoped = " ".join(text.split()[:p["scope_words"]]) if p.get("scope_words") else text
        hit = bool(re.search(p["pattern"], scoped))
        r["result"] = ("pass" if hit else "FAIL") if p["kind"] == "MUST" else ("FAIL" if hit else "pass")
        if hit and p["kind"] == "MUST_NOT": r["match"] = re.search(p["pattern"], scoped).group(0)[:80]
    out.append(r)
print(json.dumps(out, indent=1))
