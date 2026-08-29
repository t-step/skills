#!/usr/bin/env python3
"""Validate cross-skill dependency references declared in skills/*/SKILL.md.

A skill declares a dependency on another skill with a REQUIRED marker, per
the convention in superpowers' writing-skills skill:

    **REQUIRED SUB-SKILL:** Use <skill-name>
    **REQUIRED BACKGROUND:** You MUST understand <skill-name>

<skill-name> is either a bare name (a skill in this repo's skills/) or a
`namespace:skill-name` reference to an external plugin skill, which this
script cannot see into and does not validate further.

Fails (exit 1) if any of these holds:

1. A REQUIRED marker line doesn't parse to a `Use <name>` / `understand
   <name>` reference.
2. A bare (unqualified) reference names a skill that doesn't exist under
   skills/.
3. A skill declares a REQUIRED reference to itself.
4. A dependency chain among local skills is more than one hop deep (A
   requires B, and B itself requires anything locally) — mirrors the
   "keep references one level deep" rule for SKILL.md's own supporting
   files, applied to skill-to-skill references so an agent resolving one
   dependency doesn't have to chase a second to get the full picture.
"""

import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent

MARKER_RE = re.compile(r"\*\*REQUIRED (?:SUB-SKILL|BACKGROUND):\*\*.*")
REF_NAME_RE = re.compile(
    r"\b(?:Use|understand)\s+"
    r"(?P<name>[a-z0-9][a-z0-9-]*(?::[a-z0-9][a-z0-9-]*)?)",
    re.IGNORECASE,
)

failures: list[str] = []


def local_edges(rel: str, skill_name: str, text: str, local_skills: set[str]) -> list[str]:
    edges = []
    for line in text.splitlines():
        marker = MARKER_RE.search(line)
        if not marker:
            continue
        ref = REF_NAME_RE.search(marker.group(0))
        if not ref:
            failures.append(f"{rel}: unparseable dependency marker: {marker.group(0)!r}")
            continue
        name = ref.group("name")
        if ":" in name:
            continue  # external plugin skill — out of this repo, not our graph
        if name == skill_name:
            failures.append(f"{rel}: skill declares a REQUIRED dependency on itself ('{name}')")
            continue
        if name not in local_skills:
            failures.append(f"{rel}: REQUIRED dependency on '{name}', which has no skills/{name}/SKILL.md")
            continue
        edges.append(name)
    return edges


def main() -> int:
    skill_files = sorted(REPO.glob("skills/*/SKILL.md"))
    local_skills = {p.parent.name for p in skill_files}

    graph: dict[str, list[str]] = {}
    for skill_md in skill_files:
        rel = skill_md.relative_to(REPO)
        skill_name = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8")
        graph[skill_name] = local_edges(str(rel), skill_name, text, local_skills)

    rel_by_name = {p.parent.name: p.relative_to(REPO) for p in skill_files}
    total_edges = 0
    for skill_name, deps in graph.items():
        for dep in deps:
            total_edges += 1
            downstream = graph.get(dep, [])
            if downstream:
                chain = " -> ".join([skill_name, dep, downstream[0]])
                failures.append(
                    f"{rel_by_name[skill_name]}: dependency chain exceeds one hop ({chain}); "
                    f"keep cross-skill references one level deep"
                )

    if failures:
        print(f"check-skill-deps: FAIL ({len(failures)} problem(s))")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"check-skill-deps: OK ({len(skill_files)} skill file(s), {total_edges} local dependency edge(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
