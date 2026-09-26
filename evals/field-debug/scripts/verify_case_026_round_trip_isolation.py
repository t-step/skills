#!/usr/bin/env python3
"""Structural isolation check for case-026's producer/consumer round trip.

case-026 splits evidence across phase_a/ (given only to the producing
agent) and phase_b/ (given only to the consuming agent). The only
channel meant to carry information from A to B is
phase_b/handoff_artifact.md -- everything else in phase_a/ must stay
out of phase_b/. This never touches a live agent; it's a pre-run and
post-capture structural check, run the same way
verify_checkpoint_resume_isolation.py is for case-020/case-021.

Two things fail this script:
1. phase_b/ contains a file it shouldn't (anything beyond the fixed set
   below, or anything shaped like a transcript/scratch dump).
2. Any file in phase_b/ other than handoff_artifact.md contains a
   substring copied verbatim from a phase_a/ file (a sign that raw
   Phase A evidence leaked into Phase B by mistake).

It does NOT try to judge whether handoff_artifact.md is a *good*
handoff -- that's grading/case-026.expected.md's job, done by a human or
model reading actual output. This script only checks the isolation
boundary is intact, before and after the placeholder is replaced with
Agent A's real output.
"""

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent.parent.parent
CASE_DIR = REPO / "evals" / "field-debug" / "cases" / "case-026"
PHASE_A = CASE_DIR / "phase_a"
PHASE_B = CASE_DIR / "phase_b"

EXPECTED_PHASE_B_FILES = {"context.md", "handoff_artifact.md", "vendor_response.md"}
TRANSCRIPT_NAME_PATTERN = re.compile(
    r"transcript|scratch|raw[_-]?log|full[_-]?session|agent[_-]?a\b", re.IGNORECASE
)

# A line must be at least this long to count as a meaningful leak signal --
# short lines ("### Notes", "```") collide across unrelated files constantly
# and would produce false positives.
MIN_LEAK_LINE_LENGTH = 40


def phase_a_lines() -> set[str]:
    lines: set[str] = set()
    for path in sorted(PHASE_A.rglob("*")):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if len(stripped) >= MIN_LEAK_LINE_LENGTH:
                lines.add(stripped)
    return lines


def main() -> int:
    failures: list[str] = []

    if not PHASE_A.is_dir() or not PHASE_B.is_dir():
        print("verify_case_026_round_trip_isolation: FAIL -- phase_a/ or phase_b/ missing")
        return 1

    actual_phase_b_files = {p.name for p in PHASE_B.iterdir() if p.is_file()}
    unexpected = actual_phase_b_files - EXPECTED_PHASE_B_FILES
    if unexpected:
        failures.append(f"unexpected file(s) in phase_b/: {sorted(unexpected)}")

    for name in actual_phase_b_files:
        if TRANSCRIPT_NAME_PATTERN.search(name):
            failures.append(f"transcript-shaped filename in phase_b/: {name}")

    leaked_lines = phase_a_lines()
    for path in sorted(PHASE_B.iterdir()):
        if not path.is_file() or path.name == "handoff_artifact.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped in leaked_lines:
                failures.append(
                    f"{path.relative_to(REPO)} contains a line copied verbatim "
                    f"from a phase_a/ file: {stripped[:80]!r}"
                )

    artifact_path = PHASE_B / "handoff_artifact.md"
    artifact_text = artifact_path.read_text(encoding="utf-8", errors="replace")
    if "PLACEHOLDER -- not agent-visible content" in artifact_text:
        print(
            "verify_case_026_round_trip_isolation: NOTE -- handoff_artifact.md "
            "is still the unfilled placeholder; the verbatim-copy check below "
            "only applies once Agent A's real output replaces it."
        )
    else:
        for phase_a_path in sorted(PHASE_A.rglob("*")):
            if not phase_a_path.is_file():
                continue
            phase_a_text = phase_a_path.read_text(encoding="utf-8", errors="replace")
            if phase_a_text.strip() and phase_a_text.strip() == artifact_text.strip():
                failures.append(
                    f"handoff_artifact.md is byte-identical to {phase_a_path.relative_to(REPO)} "
                    "-- looks like raw Phase A evidence was copied in place of an actual handoff"
                )

    if failures:
        print(f"verify_case_026_round_trip_isolation: FAIL ({len(failures)} problem(s))")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        f"verify_case_026_round_trip_isolation: OK "
        f"(phase_b/ has only {sorted(actual_phase_b_files)}, no phase_a/ leakage detected)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
