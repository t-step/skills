#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Resolve declared vs. locked versions of named packages for one frontend root.

Design-system-agnostic: takes the package names to resolve as arguments,
not a hardcoded list. Reads package.json (dependencies + devDependencies)
for the declared semver range, and a lockfile if one is found, for the
actually-resolved version. Supports npm's package-lock.json (lockfileVersion
2 or 3, "packages" map) and yarn's yarn.lock (v1 format: the declared range
must appear verbatim as one of a block's comma-separated "name@range" keys,
matching how yarn.lock itself records it).

Emits FACTS only:
  - declared range (or null if the package isn't a direct dependency)
  - locked version (or null if no lockfile, the package isn't resolved in
    it, or -- yarn.lock only -- no block's key matches the exact declared
    range verbatim)
  - "resolved": true only when a locked version was found -- callers must
    not assume "declared range" alone pins a version; a range like
    "^3.0.693" with no lockfile is genuinely unresolved, not approximately
    known.

Usage:
  uv run resolve_versions.py --root FRONTEND_ROOT --package NAME [--package NAME ...] [--lockfile PATH]

If --lockfile is omitted, looks for package-lock.json, then yarn.lock, at
FRONTEND_ROOT and then each parent directory up to 3 levels up (monorepo-
style lockfile placement), first match wins.
"""

import argparse
import json
import sys
from pathlib import Path


def find_lockfile(root: Path) -> Path | None:
    candidates = [root] + list(root.parents)[:3]
    for d in candidates:
        for name in ("package-lock.json", "yarn.lock"):
            candidate = d / name
            if candidate.exists():
                return candidate
    return None


def declared_range(package_json: dict, name: str) -> str | None:
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        deps = package_json.get(key) or {}
        if name in deps:
            return deps[name]
    return None


def parse_yarn_lock(text: str) -> dict[str, str]:
    """Map each verbatim 'name@range' block key to its resolved version.

    Yarn v1 lockfile blocks look like:
        "@mui/material@^5.15.11":
          version "5.15.11"
          ...
    or, when multiple requesters share a resolution:
        "foo@^1.0.0", "foo@^1.2.0":
          version "1.2.3"
          ...
    Only exact key matches are recorded -- no semver range reasoning, same
    "facts only" discipline as the npm path.
    """
    result: dict[str, str] = {}
    current_keys: list[str] = []
    for raw_line in text.splitlines():
        if not raw_line or raw_line.startswith("#"):
            continue
        if not raw_line[0].isspace():
            if not raw_line.rstrip().endswith(":"):
                current_keys = []
                continue
            header = raw_line.rstrip()[:-1]
            current_keys = [
                part.strip().strip('"')
                for part in header.split(", ")
                if "@" in part
            ]
        elif raw_line.strip().startswith("version "):
            _, _, rest = raw_line.strip().partition(" ")
            version = rest.strip().strip('"')
            for key in current_keys:
                result[key] = version
            current_keys = []
    return result


def locked_version_yarn(yarn_map: dict[str, str], name: str, declared_range: str | None) -> str | None:
    if declared_range is None:
        return None
    return yarn_map.get(f"{name}@{declared_range}")


def locked_version(lock: dict, name: str) -> str | None:
    packages = lock.get("packages")
    if isinstance(packages, dict):
        entry = packages.get(f"node_modules/{name}")
        if isinstance(entry, dict) and "version" in entry:
            return entry["version"]
        return None
    # lockfileVersion 1 shape: top-level "dependencies" map keyed by bare name.
    deps = lock.get("dependencies")
    if isinstance(deps, dict) and name in deps:
        return deps[name].get("version")
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True, type=Path, help="Frontend root containing package.json")
    ap.add_argument("--package", action="append", required=True, dest="packages")
    ap.add_argument("--lockfile", type=Path, default=None)
    args = ap.parse_args()

    pkg_json_path = args.root / "package.json"
    if not pkg_json_path.exists():
        print(f"resolve_versions: no package.json at {pkg_json_path}", file=sys.stderr)
        return 1
    package_json = json.loads(pkg_json_path.read_text())

    lockfile_path = args.lockfile or find_lockfile(args.root)
    is_yarn = lockfile_path is not None and lockfile_path.name == "yarn.lock"
    lock = None
    yarn_map = None
    if lockfile_path is not None:
        if is_yarn:
            yarn_map = parse_yarn_lock(lockfile_path.read_text())
        else:
            lock = json.loads(lockfile_path.read_text())

    results = []
    for name in args.packages:
        declared = declared_range(package_json, name)
        if is_yarn:
            locked = locked_version_yarn(yarn_map, name, declared)
        else:
            locked = locked_version(lock, name) if lock is not None else None
        results.append({
            "package": name,
            "declared_range": declared,
            "locked_version": locked,
            "resolved": locked is not None,
        })

    json.dump({
        "package_json": str(pkg_json_path),
        "lockfile": str(lockfile_path) if lockfile_path else None,
        "packages": results,
    }, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
