#!/usr/bin/env python3
"""Deterministic part of grading one halp run. Prints JSON.

Usage: check-response.py <manifest.json> <eval-id> <run-dir>
<run-dir> holds outputs/response.md, fingerprint.before, fingerprint.after.
Checks: repo unchanged (fingerprints), word budget, forbidden-heading
patterns from the manifest entry's "checks", and two generic flags any
response is screened for (raw porcelain/log dumps; closing by asking
permission or announcing action). The flags are prompts for the human/model
grader to look, not verdicts.
"""
import json, pathlib, re, sys

manifest, eval_id, run = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
entry = next(e for e in json.loads(pathlib.Path(manifest).read_text())["evals"] if str(e["id"]) == eval_id)
checks = entry.get("checks", {})
resp = (run / "outputs" / "response.md").read_text()
# Subagents inherit the operator's global instructions, which can append a
# "Session report" receipt to any turn that used tools. That is a harness
# artifact, not part of the answer, so it is excluded from the word count.
receipt = re.search(r"(?m)^Session report\b", resp)
answer = resp[:receipt.start()] if receipt else resp
words = len(answer.split())
before = (run / "fingerprint.before").read_text().splitlines()
after = (run / "fingerprint.after").read_text().splitlines()
changed = [b.split(":")[0] for b, a in zip(before, after) if b != a and not b.startswith("cache-dirs")]
caches = int(after[-1].split(": ")[1]) - int(before[-1].split(": ")[1])
porcelain = len(re.findall(r"(?m)^(\?\?|[ MADRCU]{2}) \S", resp))
loglines = len(re.findall(r"(?m)^\s*[0-9a-f]{7,} \S", resp))
permission = re.findall(r"(?im)(shall i|should i|want me to|would you like me|let me know if you'?d like me|say the word|tell me if you|i can (?:stash|commit|apply|fix|revert|make)|i'?ll (?:go ahead|now |proceed)|i(?:'ve| have) (?:made|applied|committed|edited|updated|fixed))", resp)
forbidden = [p for p in checks.get("forbid_patterns", []) if re.search(p, resp)]
print(json.dumps({
    "words": words, "receipt_appended": bool(receipt), "max_words": checks.get("max_words"),
    "within_budget": words <= checks.get("max_words", 10**9),
    "repo_unchanged": not changed, "changed_fields": changed, "new_cache_dirs": caches,
    "forbidden_pattern_hits": forbidden,
    "raw_dump_suspected": porcelain >= 2 or loglines >= 4,
    "permission_or_action_phrases": permission,
}, indent=2))
