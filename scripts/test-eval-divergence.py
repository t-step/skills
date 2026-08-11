#!/usr/bin/env python3
"""Focused verification for scripts/eval-divergence.py's resolve_case_repo.

Stdlib-only, no test framework, run directly:
`python3 scripts/test-eval-divergence.py`. Follows the same
runpy.run_path(..., run_name="test") pattern as test-skill-usage-report.py
-- calls the function directly without needing the hyphenated filename to
be importable.

Scoped narrowly to the files[] contract validation this script now enforces
(no files / empty files / more than one entry / non-directory entry), plus
one positive case. Does not test claude -p invocation, verify execution, or
diffing -- those require a live run, not a unit test.
"""

import pathlib
import runpy
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "eval-divergence.py"

failures = []


def check(name, condition):
    if condition:
        print(f"OK: {name}")
    else:
        print(f"FAIL: {name}")
        failures.append(name)


def load_module():
    return runpy.run_path(str(SCRIPT), run_name="test")


def test_rejects_missing_files():
    mod = load_module()
    try:
        mod["resolve_case_repo"]({"id": 1})
        check("rejects a case with no 'files' key", False)
    except mod["ManifestError"] as e:
        check("rejects a case with no 'files' key", "missing or empty" in str(e))


def test_rejects_empty_files():
    mod = load_module()
    try:
        mod["resolve_case_repo"]({"id": 2, "files": []})
        check("rejects a case with an empty 'files' list", False)
    except mod["ManifestError"] as e:
        check("rejects a case with an empty 'files' list", "missing or empty" in str(e))


def test_rejects_multiple_files():
    mod = load_module()
    try:
        mod["resolve_case_repo"]({
            "id": 3,
            "files": [
                "evals/eval-runner-demo/cases/case-001/repo/",
                "evals/eval-runner-demo/cases/case-002/repo/",
            ],
        })
        check("rejects a case with more than one 'files' entry", False)
    except mod["ManifestError"] as e:
        check("rejects a case with more than one 'files' entry", "exactly one is required" in str(e))


def test_rejects_non_directory_entry():
    mod = load_module()
    try:
        mod["resolve_case_repo"]({"id": 4, "files": ["evals/eval-runner-demo/divergence.json"]})
        check("rejects a 'files' entry that is not a directory", False)
    except mod["ManifestError"] as e:
        check("rejects a 'files' entry that is not a directory", "is not a directory" in str(e))


def test_accepts_single_directory_entry():
    mod = load_module()
    resolved = mod["resolve_case_repo"]({"id": 5, "files": ["evals/eval-runner-demo/cases/case-001/repo/"]})
    check("accepts a single valid directory 'files' entry", resolved.is_dir())


def main():
    test_rejects_missing_files()
    test_rejects_empty_files()
    test_rejects_multiple_files()
    test_rejects_non_directory_entry()
    test_accepts_single_directory_entry()

    if failures:
        print(f"\ntest-eval-divergence: FAIL ({len(failures)} problem(s))")
        for name in failures:
            print(f"  - {name}")
        return 1
    print("\ntest-eval-divergence: OK (all checks passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
