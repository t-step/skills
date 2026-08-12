#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Generate the skill inventory table in README.md from skills/*/SKILL.md.

Exists because README.md used to carry a hand-maintained skill table that
silently drifted from the skills that actually exist (two skills,
`next-best-product-slice` and `ship-slice`, were never added to it). The
single source of truth is each skill's own frontmatter; this script derives
the table from it, and `--check` guards against the table going stale again
without anyone noticing.

Run with `uv run scripts/generate-skill-inventory.py` (dependencies resolve
from the inline metadata above) to regenerate the managed region of
README.md in place, between the `<!-- skill-inventory:begin -->` and
`<!-- skill-inventory:end -->` markers. Text outside those markers is left
byte-identical.

Run with `--check` to verify the committed README.md matches what this
script would generate, without writing anything; exits nonzero and prints a
unified diff if it does not. `scripts/check.sh` runs this in `--check` mode.

Deterministic summary rule (one column, table cells must stay short even
though frontmatter descriptions run up to ~1000 chars): take the first
sentence of the frontmatter `description` (text up to and including the
first `. ` or the end of the string if no such break exists), collapse
internal whitespace, then hard-truncate to SUMMARY_MAX_CHARS characters,
replacing the tail with a single `…` if truncation happened. No
paraphrasing, no LLM involvement — the same description always produces the
same summary.

Validation-status rule (per skill, derived from evals/<name>/): count the
`evals/<name>/cases/case-*` directories. If there is no `evals/<name>/`
directory, or it has zero case directories, the status is "no evals". If
case directories exist but `evals/<name>/RESULTS.md` is missing, the status
is "authored, unrun" — fixtures exist but nothing recorded them being run.
If RESULTS.md exists, it counts as recording at least one actually-executed
run only if it contains a pass/fail fraction (a `<number>/<number>` token,
e.g. "12/12" or "2/3") anywhere in its text — the shape every RESULTS.md in
this repo uses to report real graded output. A RESULTS.md that only
describes fixtures as authored-but-not-yet-run (see evals/ship-slice/, which
says so explicitly and contains no such fraction) correctly falls through
to "authored, unrun" rather than being overstated. This is a deliberately
conservative, honest signal: no fraction found means unrun, even if prose
elsewhere hints at execution.
"""

import difflib
import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
README = REPO / "README.md"
BEGIN_MARKER = "<!-- skill-inventory:begin -->"
END_MARKER = "<!-- skill-inventory:end -->"
SUMMARY_MAX_CHARS = 160
FRACTION_RE = re.compile(r"\b\d+/\d+\b")


def load_frontmatter(skill_md: pathlib.Path) -> dict | None:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return data


def summarize(description: str) -> str:
    match = re.search(r"(.+?\.)(\s|$)", description, re.DOTALL)
    first = match.group(1) if match else description
    first = re.sub(r"\s+", " ", first).strip()
    if len(first) > SUMMARY_MAX_CHARS:
        return first[: SUMMARY_MAX_CHARS - 1].rstrip() + "…"
    return first


def validation_status(name: str) -> str:
    evals_dir = REPO / "evals" / name
    if not evals_dir.is_dir():
        return "no evals"
    case_dirs = sorted(evals_dir.glob("cases/case-*"))
    count = len(case_dirs)
    if count == 0:
        return "no evals"
    results = evals_dir / "RESULTS.md"
    if not results.is_file():
        return f"{count} cases · authored, unrun"
    text = results.read_text(encoding="utf-8", errors="replace")
    if FRACTION_RE.search(text):
        return f"{count} cases · validated (sample)"
    return f"{count} cases · authored, unrun"


def collect_rows() -> list[tuple[str, str, str]]:
    rows = []
    for skill_md in sorted(REPO.glob("skills/*/SKILL.md")):
        data = load_frontmatter(skill_md)
        if data is None:
            print(f"generate-skill-inventory: {skill_md}: unreadable frontmatter, skipping", file=sys.stderr)
            continue
        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not name:
            name = skill_md.parent.name
        if not isinstance(description, str) or not description:
            print(f"generate-skill-inventory: {skill_md}: no description, skipping", file=sys.stderr)
            continue
        rows.append((name, summarize(description), validation_status(name)))
    return rows


def render_block() -> str:
    rows = collect_rows()
    lines = [BEGIN_MARKER, "| Skill | What it does | Validation |", "|---|---|---|"]
    for name, summary, status in rows:
        lines.append(f"| [`{name}`](skills/{name}/) | {summary} | {status} |")
    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"


def splice_readme(readme_text: str, block: str) -> str | None:
    lines = readme_text.splitlines(keepends=True)
    begin_idx = next((i for i, line in enumerate(lines) if line.strip() == BEGIN_MARKER), None)
    end_idx = next((i for i, line in enumerate(lines) if line.strip() == END_MARKER), None)
    if begin_idx is None or end_idx is None or end_idx <= begin_idx:
        return None
    return "".join(lines[:begin_idx]) + block + "".join(lines[end_idx + 1 :])


def main() -> int:
    check = "--check" in sys.argv[1:]
    if not README.is_file():
        print("generate-skill-inventory: README.md not found", file=sys.stderr)
        return 1

    readme_text = README.read_text(encoding="utf-8")
    block = render_block()
    new_readme = splice_readme(readme_text, block)
    if new_readme is None:
        print(
            f"generate-skill-inventory: README.md is missing {BEGIN_MARKER} / {END_MARKER} markers",
            file=sys.stderr,
        )
        return 1

    if check:
        if new_readme == readme_text:
            print("generate-skill-inventory: OK (README.md skill inventory is current)")
            return 0
        diff = difflib.unified_diff(
            readme_text.splitlines(keepends=True),
            new_readme.splitlines(keepends=True),
            fromfile="README.md (committed)",
            tofile="README.md (generated)",
        )
        print("generate-skill-inventory: FAIL (README.md skill inventory is stale)")
        sys.stdout.writelines(diff)
        print("\nRun `uv run scripts/generate-skill-inventory.py` to refresh it.")
        return 1

    if new_readme != readme_text:
        README.write_text(new_readme, encoding="utf-8")
        print("generate-skill-inventory: README.md skill inventory updated")
    else:
        print("generate-skill-inventory: README.md skill inventory already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
