#!/usr/bin/env python3
"""Guard against answer leakage from slice-review eval grading into agent-visible inputs.

Fails (exit 1) if any of these holds:

1. An agent-visible case path (any file or directory under an evals/*/cases/
   tree) contains a scenario label or a verdict-derived slug.
2. An answer-key/grading file (expected*, grading*) exists inside an
   agent-visible case directory.
3. An eval prompt (manifest "prompt" field, or the file named by
   "prompt_file") or any agent-visible case file contains an expected-verdict
   phrase. The generic question "ready to merge" is allowed — every prompt
   asks it — but the decided verdict phrases ("not ready to merge", "ready
   after minor corrections", "unable to verify") never belong in inputs.

Scenario labels live only in grader-side materials: manifests' name/
failure_mode fields, grading/ files, and suite READMEs. This script never
scans those.
"""

import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
EVALS = REPO / "evals"

# Human-readable scenario labels that would identify the trap being tested.
SCENARIO_LABELS = [
    "clean-slice",
    "hidden-defect",
    "obsolete-path",
    "insufficient-evidence",
    "scope-creep",
    "false-positive",
    "minor-corrections",
    "goal-ambiguity",
    "approval-bias",
    "false-confidence",
    "misleading-docs",
    "incomplete-evidence",
    "zombie",
    "scope-confusion",
    "instruction-injection",
    "tempting-redesign",
]

# Verdict phrases that decide the answer. "ready to merge" alone is the
# question every prompt asks, so it is deliberately not on this list; the
# hyphenated slug forms are checked in paths, where no question appears.
VERDICT_PHRASES = [
    "not ready to merge",
    "ready after minor corrections",
    "unable to verify",
]
VERDICT_SLUGS = [
    "ready-to-merge",
    "not-ready",
    "minor-corrections",
    "unable-to-verify",
]

failures: list[str] = []


def check_path_component(path: pathlib.Path) -> None:
    rel = path.relative_to(REPO).as_posix().lower()
    for label in SCENARIO_LABELS + VERDICT_SLUGS:
        if label in rel:
            failures.append(f"path leaks '{label}': {path.relative_to(REPO)}")


def check_text(text: str, origin: str) -> None:
    lowered = text.lower()
    for label in SCENARIO_LABELS:
        if label in lowered:
            failures.append(f"content leaks scenario label '{label}': {origin}")
    for phrase in VERDICT_PHRASES:
        if phrase in lowered:
            failures.append(f"content leaks verdict phrase '{phrase}': {origin}")


def main() -> int:
    case_dirs = sorted(EVALS.glob("*/cases/case-*"))
    if not case_dirs:
        print("check-eval-isolation: no evals/*/cases/case-* directories found", file=sys.stderr)
        return 1

    for case_dir in case_dirs:
        check_path_component(case_dir)
        for path in sorted(case_dir.rglob("*")):
            check_path_component(path)
            if path.is_file():
                name = path.name.lower()
                if name.startswith("expected") or name.startswith("grading") or ".expected." in name:
                    failures.append(f"answer key inside agent-visible case dir: {path.relative_to(REPO)}")
                    continue
                check_text(path.read_text(encoding="utf-8", errors="replace"), str(path.relative_to(REPO)))

    for manifest_path in sorted(EVALS.glob("*/**/*.json")) + sorted(EVALS.glob("*/*.json")):
        try:
            manifest = json.loads(manifest_path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            failures.append(f"unparseable manifest: {manifest_path.relative_to(REPO)}")
            continue
        for entry in manifest.get("evals", []):
            origin = f"{manifest_path.relative_to(REPO)} eval id={entry.get('id')}"
            prompt = entry.get("prompt", "")
            if prompt:
                check_text(prompt, f"{origin} field=prompt")
            prompt_file = entry.get("prompt_file", "")
            if prompt_file and not (REPO / prompt_file).is_file():
                failures.append(f"prompt_file does not exist: {prompt_file} ({origin})")
            for f in entry.get("files", []):
                target = REPO / f.rstrip("/")
                if not target.exists():
                    failures.append(f"referenced files entry does not exist: {f} ({origin})")
                if re.search(r"expected|grading", f, re.IGNORECASE):
                    failures.append(f"agent-visible files entry points at grading material: {f} ({origin})")

    if failures:
        print(f"check-eval-isolation: FAIL ({len(failures)} problem(s))")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"check-eval-isolation: OK ({len(case_dirs)} case dirs, no leakage)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
