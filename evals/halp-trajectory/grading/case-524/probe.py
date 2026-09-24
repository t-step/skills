"""Behavior probe: how are comma-separated regex option values split? Run from repo root with the repo's .venv python."""
import json, subprocess, sys, warnings
warnings.filterwarnings("ignore")
from pylint.config.argument import _regexp_csv_transfomer as split
def run(s):
    try: return [p.pattern for p in split(s)]
    except BaseException as e: return "ERROR: " + str(e)[:90]
cases = ["(foo{1,3})", "foo,bar", "a{1,3}, b", "(a,b)", "[a,b],c", "(foo{1,}, foo{1,3}})"]
res = {"splits": {c: run(c) for c in cases}}
t = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/config/test_config.py::test_csv_regex_error"], capture_output=True, text=True)
res["tests"] = {"existing test_csv_regex_error": "pass" if t.returncode == 0 else "fail"}
s = res["splits"]
ok = s["(foo{1,3})"] == ["(foo{1,3})"] and s["a{1,3}, b"] == ["a{1,3}", "b"]
res["path"] = "neither" if not ok else "A" if s["(a,b)"] == ["(a,b)"] else "B"   # A = paren/bracket-aware tokenizer, B = brace-only splitting
print(json.dumps(res))
