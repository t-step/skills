#!/usr/bin/env python3
"""Guard against answer leakage from eval grading into agent-visible inputs.

Generalized across all skills under evals/ (not just one) — each skill's
own manifests (evals.json, pressure-tests/pressure_evals.json, etc.) supply
the scenario labels checked against that skill's own evals/<skill>/cases/
tree. Adding a new skill's eval suite does not require touching this
script; it only needs manifests shaped like the existing ones (an "evals"
list of entries with "name" and/or "failure_mode" fields).

Fails (exit 1) if any of these holds, scoped per skill:

1. An agent-visible case path (any file or directory under that skill's
   evals/<skill>/cases/ tree) contains a scenario label derived from that
   skill's own manifests, or a verdict-derived slug (see SKILL_VERDICTS).
2. An answer-key/grading file (expected*, grading*) exists inside an
   agent-visible case directory.
3. An eval prompt (manifest "prompt" field, or the file named by
   "prompt_file") or any agent-visible case file contains a scenario label
   or one of that skill's closed-vocabulary verdict phrases (see
   SKILL_VERDICTS). A skill's generic question phrasing (e.g. slice-review's
   "ready to merge") is allowed since every prompt asks it; only the
   *decided* verdict phrases are checked.

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

# Skills with a small, closed verdict vocabulary get extra phrase/slug
# checks (their generic question phrasing, e.g. "ready to merge", is
# deliberately excluded — every prompt asks it). Skills without a closed
# verdict vocabulary (most retrospective/report-style skills) get none;
# their scenario-label check below still applies.
SKILL_VERDICTS = {
    "slice-review": {
        "phrases": [
            "not ready to merge",
            "ready after minor corrections",
            "unable to verify",
        ],
        "slugs": [
            "ready-to-merge",
            "not-ready",
            "minor-corrections",
            "unable-to-verify",
        ],
    },
}

failures: list[str] = []


def derive_labels(text: str) -> set[str]:
    """The full string, lowercased, as a single label — a hyphenated slug
    like 'false-positive-zombie' or a full failure_mode sentence. Names are
    deliberately NOT split into individual words: a curated multi-word slug
    is a near-impossible accidental match in fixture prose, but generic
    single words pulled from it (e.g. 'notes' out of 'overstated-notes',
    'evidence' out of 'ambiguous-evidence') collide constantly with
    ordinary fixture content and produce false positives."""
    labels: set[str] = set()
    if not text:
        return labels
    slug = text.strip().lower()
    if slug:
        labels.add(slug)
    return labels


def load_manifest(path: pathlib.Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, UnicodeDecodeError):
        failures.append(f"unparseable manifest: {path.relative_to(REPO)}")
        return None


def scenario_labels_for_skill(skill_dir: pathlib.Path) -> set[str]:
    labels: set[str] = set()
    for manifest_path in sorted(skill_dir.rglob("*.json")):
        manifest = load_manifest(manifest_path)
        if manifest is None:
            continue
        for entry in manifest.get("evals", []):
            labels |= derive_labels(entry.get("name", ""))
            labels |= derive_labels(entry.get("failure_mode", ""))
    return labels


def check_path_component(path: pathlib.Path, labels: set[str], slugs: list[str]) -> None:
    rel = path.relative_to(REPO).as_posix().lower()
    for label in sorted(labels) + slugs:
        if label and label in rel:
            failures.append(f"path leaks '{label}': {path.relative_to(REPO)}")


def check_text(text: str, origin: str, labels: set[str], phrases: list[str]) -> None:
    lowered = text.lower()
    for label in labels:
        if label in lowered:
            failures.append(f"content leaks scenario label '{label}': {origin}")
    for phrase in phrases:
        if phrase in lowered:
            failures.append(f"content leaks verdict phrase '{phrase}': {origin}")


def check_manifest_entries(skill_dir: pathlib.Path, labels: set[str], phrases: list[str]) -> None:
    for manifest_path in sorted(skill_dir.rglob("*.json")):
        manifest = load_manifest(manifest_path)
        if manifest is None:
            continue
        for entry in manifest.get("evals", []):
            origin = f"{manifest_path.relative_to(REPO)} eval id={entry.get('id')}"
            prompt = entry.get("prompt", "")
            if prompt:
                check_text(prompt, f"{origin} field=prompt", labels, phrases)
            prompt_file = entry.get("prompt_file", "")
            if prompt_file and not (REPO / prompt_file).is_file():
                failures.append(f"prompt_file does not exist: {prompt_file} ({origin})")
            for f in entry.get("files", []):
                target = REPO / f.rstrip("/")
                if not target.exists():
                    failures.append(f"referenced files entry does not exist: {f} ({origin})")
                if re.search(r"expected|grading", f, re.IGNORECASE):
                    failures.append(f"agent-visible files entry points at grading material: {f} ({origin})")


def main() -> int:
    skill_dirs = sorted(d for d in EVALS.iterdir() if d.is_dir()) if EVALS.is_dir() else []
    total_case_dirs = 0

    if not skill_dirs:
        print("check-eval-isolation: no evals/<skill>/ directories found", file=sys.stderr)
        return 1

    for skill_dir in skill_dirs:
        case_dirs = sorted(skill_dir.glob("cases/case-*"))
        if not case_dirs:
            continue
        total_case_dirs += len(case_dirs)

        skill_name = skill_dir.name
        verdicts = SKILL_VERDICTS.get(skill_name, {"phrases": [], "slugs": []})
        labels = scenario_labels_for_skill(skill_dir)

        for case_dir in case_dirs:
            check_path_component(case_dir, labels, verdicts["slugs"])
            for path in sorted(case_dir.rglob("*")):
                check_path_component(path, labels, verdicts["slugs"])
                if path.is_file():
                    name = path.name.lower()
                    if name.startswith("expected") or name.startswith("grading") or ".expected." in name:
                        failures.append(f"answer key inside agent-visible case dir: {path.relative_to(REPO)}")
                        continue
                    check_text(
                        path.read_text(encoding="utf-8", errors="replace"),
                        str(path.relative_to(REPO)),
                        labels,
                        verdicts["phrases"],
                    )

        check_manifest_entries(skill_dir, labels, verdicts["phrases"])

    if total_case_dirs == 0:
        print("check-eval-isolation: no evals/*/cases/case-* directories found", file=sys.stderr)
        return 1

    if failures:
        print(f"check-eval-isolation: FAIL ({len(failures)} problem(s))")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"check-eval-isolation: OK ({total_case_dirs} case dirs across {len(skill_dirs)} skill(s), no leakage)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
