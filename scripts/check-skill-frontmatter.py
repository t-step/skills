#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Lint the YAML frontmatter of every skills/*/SKILL.md with a strict parser.

Exists because an unquoted `description:` scalar containing ": " shipped to
main as invalid YAML — lenient consumers read it, but any strict parser
(GitHub's renderer, spec-conforming skill loaders) rejects the whole block,
and the description is what drives skill triggering.

Run with `uv run scripts/check-skill-frontmatter.py` (dependencies resolve
from the inline metadata above). Fails (exit 1) if any SKILL.md:

1. lacks a frontmatter block (`---` ... `---`) at the very top;
2. has frontmatter that a strict YAML 1.1 safe-load rejects, or that is not
   a flat mapping;
3. is missing `name` or `description`, or either is not a non-empty string;
4. has a `name` that does not match its parent directory, exceeds 64
   characters, or is not lowercase-hyphen (the Agent Skills format);
5. has a `description` longer than 1024 characters.
"""

import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESCRIPTION_MAX = 1024

failures: list[str] = []


def check(skill_md: pathlib.Path) -> None:
    rel = skill_md.relative_to(REPO) if skill_md.is_relative_to(REPO) else skill_md
    text = skill_md.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        failures.append(f"{rel}: no frontmatter block at top of file")
        return
    end = text.find("\n---", 4)
    if end == -1:
        failures.append(f"{rel}: frontmatter opened but never closed")
        return
    raw = text[4:end]

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        failures.append(f"{rel}: frontmatter is not valid strict YAML: {exc}")
        return
    if not isinstance(data, dict):
        failures.append(f"{rel}: frontmatter parses to {type(data).__name__}, not a mapping")
        return

    for field in ("name", "description"):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            failures.append(f"{rel}: '{field}' missing or not a non-empty string")
    name = data.get("name")
    if isinstance(name, str):
        if name != skill_md.parent.name:
            failures.append(f"{rel}: name '{name}' != directory '{skill_md.parent.name}'")
        if len(name) > NAME_MAX:
            failures.append(f"{rel}: name exceeds {NAME_MAX} chars ({len(name)})")
        if not NAME_RE.match(name):
            failures.append(f"{rel}: name '{name}' is not lowercase-hyphen")
    description = data.get("description")
    if isinstance(description, str) and len(description) > DESCRIPTION_MAX:
        failures.append(f"{rel}: description exceeds {DESCRIPTION_MAX} chars ({len(description)})")


def main() -> int:
    targets = [pathlib.Path(p) for p in sys.argv[1:]] or sorted(REPO.glob("skills/*/SKILL.md"))
    if not targets:
        print("check-skill-frontmatter: no skills/*/SKILL.md files found", file=sys.stderr)
        return 1
    for skill_md in targets:
        check(skill_md)
    if failures:
        print(f"check-skill-frontmatter: FAIL ({len(failures)} problem(s))")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"check-skill-frontmatter: OK ({len(targets)} skill file(s), strict YAML clean)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
