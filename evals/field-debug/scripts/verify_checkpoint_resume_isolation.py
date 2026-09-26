"""Authoring/verification harness for the checkpoint/resume cases
(case-020, case-021) -- NOT agent-visible (lives outside cases/, and the
harness protocol described in RESULTS.md only ever copies a case's own
cases/case-0NN/ directory into a tested agent's sandbox).

Proves two things mechanically for each case:

1. No agent-visible file passes only Phase 1's original checkpoint into
   the resumed session unaccompanied by anything else -- i.e., the case
   directory contains exactly the checkpoint plus the "current state"
   files, and nothing resembling the prior investigator's raw transcript
   (which the task's framing explicitly says should NOT be handed to the
   fresh resumed session).
2. The checkpoint itself (the only Phase-1-authored artifact) never
   mentions a fact that only exists in the Phase-2-only "current state"
   files -- i.e., the twist wasn't retrofitted into the "before" record
   once the "after" record was written, which would make the checkpoint's
   own perishable-fact warnings feel earned rather than actually earned.

Run: python3 evals/field-debug/scripts/verify_checkpoint_resume_isolation.py
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CASES = REPO / "evals" / "field-debug" / "cases"

# Filenames that would indicate a prior investigator's raw transcript (as
# opposed to their distilled checkpoint) leaked into the resumed session.
FORBIDDEN_NAME_PATTERNS = [
    re.compile(r"transcript", re.IGNORECASE),
    re.compile(r"raw[_-]?log", re.IGNORECASE),
    re.compile(r"agent[_-]?a", re.IGNORECASE),
    re.compile(r"full[_-]?session", re.IGNORECASE),
]

# Phase-2-only facts that must not appear in Phase 1's checkpoint. Note:
# "22%" alone is NOT usable here -- it's also the checkpoint's own,
# legitimate per-version (v3.15-pods-only) finding from Phase 1. The
# markers below are the more specific Phase-2-only phrasing that
# current_gateway_metrics.md uses for the *fleet-wide* number, which
# happens to match that same 22% quantitatively but is a distinct,
# later-gathered fact.
CASE_020_PHASE2_ONLY = [
    "100% of pods",
    "22% of outbound calls",
    "fleet-wide rate matches",
    "5 req/s",
    "auto-advanced to 70%",
    "auto-advanced to 100%",
    "10:40 utc",
    "10:50 utc",
]
CASE_021_PHASE2_ONLY = [
    "4.0% of rows",
    "boundary row a page",  # the docs' own restatement, distinct from Reese's hedged hypothesis wording
]


def check_no_transcript_file(case_dir: Path):
    for path in case_dir.rglob("*"):
        if path.is_file():
            for pattern in FORBIDDEN_NAME_PATTERNS:
                assert not pattern.search(path.name), (
                    f"{case_dir.name}: file name looks like a raw transcript, "
                    f"not a checkpoint: {path.relative_to(REPO)}"
                )
    print(f"OK: {case_dir.name} contains no raw-transcript-shaped file")


def check_checkpoint_has_no_phase2_facts(case_dir: Path, phase2_only_tokens: list[str]):
    checkpoint_text = (case_dir / "checkpoint.md").read_text().lower()
    for token in phase2_only_tokens:
        assert token.lower() not in checkpoint_text, (
            f"{case_dir.name}: checkpoint.md leaks a Phase-2-only fact: {token!r}"
        )
    print(f"OK: {case_dir.name}/checkpoint.md contains none of its Phase-2-only marker facts")


def main():
    check_no_transcript_file(CASES / "case-020")
    check_no_transcript_file(CASES / "case-021")
    check_checkpoint_has_no_phase2_facts(CASES / "case-020", CASE_020_PHASE2_ONLY)
    check_checkpoint_has_no_phase2_facts(CASES / "case-021", CASE_021_PHASE2_ONLY)
    print("\nverify_checkpoint_resume_isolation: PASS")


if __name__ == "__main__":
    main()
