#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Resolve declared vs. locked versions of named packages for one frontend root.

Design-system-agnostic: takes the package names to resolve as arguments,
not a hardcoded list. Reads package.json (dependencies + devDependencies)
for the declared semver range, and an npm package-lock.json (lockfileVersion
2 or 3, "packages" map) if one is found, for the actually-resolved version.

Emits FACTS only:
  - declared range (or null if the package isn't a direct dependency)
  - locked version (or null if no lockfile, or the package isn't resolved
    in it)
  - "resolved": true only when a locked version was found -- callers must
    not assume "declared range" alone pins a version; a range like
    "^3.0.693" with no lockfile is genuinely unresolved, not approximately
    known.

Usage:
  uv run resolve_versions.py --root FRONTEND_ROOT --package NAME [--package NAME ...] [--lockfile PATH]

If --lockfile is omitted, looks for package-lock.json at FRONTEND_ROOT and
then each parent directory up to 3 levels up (monorepo-style lockfile
placement), first match wins.
"""

import argparse
import json
import sys
from pathlib import Path


def find_lockfile(root: Path) -> Path | None:
    candidates = [root] + list(root.parents)[:3]
    for d in candidates:
        candidate = d / "package-lock.json"
        if candidate.exists():
            return candidate
    return None


def declared_range(package_json: dict, name: str) -> str | None:
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        deps = package_json.get(key) or {}
        if name in deps:
            return deps[name]
    return None


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
    lock = json.loads(lockfile_path.read_text()) if lockfile_path else None

    results = []
    for name in args.packages:
        declared = declared_range(package_json, name)
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
