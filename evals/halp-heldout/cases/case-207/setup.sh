#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# default branch is `develop` (origin/HEAD points at it); there is no main or master
new_repo "$out" develop
put geotools/distance.py <<'J'
import math


def haversine(a, b):
    return math.dist(a, b)
J
put README.md <<'J'
# geotools
J
commit_all "Initial geotools" "2026-09-05T09:00:00"
put geotools/io.py <<'J'
def read_points(path):
    return [tuple(map(float, l.split(","))) for l in open(path)]
J
commit_all "add point reader" "2026-09-08T09:00:00"
make_origin "git@github.com:acme/geotools.git" develop
git remote set-head origin develop
git checkout -q -b feat/export-csv
put geotools/export.py <<'J'
def to_csv(points):
    return "\n".join(f"{x},{y}" for x, y in points)
J
commit_all "export: to_csv" "2026-09-15T09:00:00"
put geotools/export.py <<'J'
def to_csv(points, header=True):
    rows = [f"{x},{y}" for x, y in points]
    return "\n".join((["x,y"] if header else []) + rows)
J
commit_all "export: optional header row" "2026-09-15T13:00:00"
put geotools/cli.py <<'J'
from .export import to_csv
J
commit_all "cli: import export" "2026-09-16T09:30:00"
