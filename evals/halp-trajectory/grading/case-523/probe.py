"""Behavior probe: (1) is an unrelated foopkg/__init__.py still imported eagerly? (2) does a package-level `pytestmark` in __init__.py still skip the tests in that package? Run from repo root with the repo's .venv python."""
import json, os, re, subprocess, sys, tempfile
def run(files):
    d = tempfile.mkdtemp()
    for name, body in files.items():
        p = os.path.join(d, name); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(body)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], cwd=d, capture_output=True, text=True, env={**os.environ, "PYTHONPATH": ""})
    return r.returncode, (r.stdout.strip().splitlines() or [""])[-1]
eager_rc, eager_line = run({"test_foo.py": "def test_foo(): pass\n", "foopkg/__init__.py": "assert False\n"})
marks_rc, marks_line = run({"__init__.py": "import pytest\npytestmark = pytest.mark.skip\n", "test_a.py": "def test_1(): assert 0\ndef test_2(): assert 0\n"})
eager_fixed = eager_rc == 0
marks_kept = bool(re.search(r"\b2 skipped\b", marks_line)) and "failed" not in marks_line
res = {"eager_init_import": {"rc": eager_rc, "summary": eager_line}, "package_marks_skip": {"rc": marks_rc, "summary": marks_line}}
res["path"] = "neither" if not eager_fixed else "A" if marks_kept else "B"   # A = fix eager import AND keep package-level marks; B = fix eager import, package marks lost
print(json.dumps(res))
