#!/usr/bin/env bash
# Shared deterministic builders for the halp eval fixtures. Sourced by each
# cases/case-NNN/setup.sh. Fixed dates and content, so a rebuild reproduces
# the same history. The fixture project is a tiny "cohort ranking" package
# with a spec, plan, and task list; each case leaves the repository in a
# different state.
set -euo pipefail

SPEC=specs/cohort-ranking

new_repo() { # new_repo <abs-dir>
  rm -rf "$1"; mkdir -p "$1"; cd "$1"
  git init -q -b main
  git config commit.gpgsign false
  git config user.name "Fixture Author"
  git config user.email "fixture@example.invalid"
}
new_dir() { rm -rf "$1"; mkdir -p "$1"; cd "$1"; }
commit_all() { # commit_all <message> <iso-date>
  git add -A
  GIT_AUTHOR_DATE="$2" GIT_COMMITTER_DATE="$2" git commit -q -m "$1"
}
commit_paths() { # commit_paths <message> <iso-date> <path>...
  local m="$1" d="$2"; shift 2
  git add -- "$@"
  GIT_AUTHOR_DATE="$d" GIT_COMMITTER_DATE="$d" git commit -q -m "$m"
}

# ---------------------------------------------------------------- docs
write_readme() { # write_readme [fixed]
  local word="recieve"; [ "${1:-}" = fixed ] && word="receive"
  cat > README.md <<EOF
# cohort

Small library that ranks learners in a cohort for the weekly review.
Learners $word a ranking based on their readiness score.
EOF
}
write_agents() {
  cat > AGENTS.md <<'EOF'
# AGENTS

- Run tests with `python3 -m unittest discover -s tests`.
- The task list is `specs/cohort-ranking/tasks.md`; requirements are in `spec.md` beside it.
EOF
}
write_spec() { # write_spec assumption|oq
  local tail
  if [ "$1" = oq ]; then
    tail='## Open questions

- OQ-1: How should learners with unknown readiness be ranked? Undecided; needs a product answer.'
  else
    tail='## Assumptions

- A1: Upstream always supplies readiness as a number in 0-100 for every learner.'
  fi
  cat > $SPEC/spec.md <<EOF
# Cohort ranking

Rank learners in a cohort for the weekly review.

## Requirements

- FR-1: Readiness is normalized from a 0-100 value to 0..1.
- FR-2: Learners are ranked by descending normalized readiness.
- FR-3: Learners with equal readiness are ordered by name, ascending.
- FR-4: Selectors are canonicalized (trimmed, lowercased, spaces to hyphens).

$tail
EOF
}
write_plan() { # write_plan assumption|oq
  local note='Normalization assumes A1; no null handling is planned.'
  [ "$1" = oq ] && note='Unknown-readiness handling waits on OQ-1.'
  cat > $SPEC/plan.md <<EOF
# Plan

1. Package scaffold, then normalization and selectors (independent).
2. Ranking builds on normalization.
3. Reporting builds on ranking.

$note
EOF
}
write_tasks() { # write_tasks assumption|oq <x|.>x6   (x = ticked)
  local variant="$1"; shift
  local i=1 mark t
  {
    echo "# Tasks: cohort ranking"; echo
    for s in "$@"; do
      mark=" "; [ "$s" = x ] && mark="x"
      case $i in
        1) t='Scaffold `cohort` package and test layout';;
        2) t='Score normalization (FR-1) in `cohort/normalize.py`';;
        3) t='Selector normalization (FR-4) in `cohort/selectors.py`';;
        4) t='Ranking with name tie-break (FR-2, FR-3) in `cohort/ranking.py`';;
        5) if [ "$variant" = oq ]; then t='Handle learners with unknown readiness (blocked on OQ-1)'
           else t='Ranking report output in `cohort/report.py`'; fi;;
        6) if [ "$variant" = oq ]; then t='Ranking report output in `cohort/report.py`'
           else t='CLI entry point in `cohort/cli.py`'; fi;;
      esac
      echo "- [$mark] T00$i $t"; i=$((i+1))
    done
  } > $SPEC/tasks.md
}
write_sample_data() {
  mkdir -p data
  cat > data/sample_cohort.json <<'EOF'
[
  {"name": "amy", "readiness": 82},
  {"name": "bo", "readiness": 64},
  {"name": "cy", "readiness": null},
  {"name": "dee", "readiness": 91},
  {"name": "eli", "readiness": "n/a"},
  {"name": "fay", "readiness": 64},
  {"name": "gus", "readiness": null},
  {"name": "hal", "readiness": 47}
]
EOF
}

# ---------------------------------------------------------------- code
write_package() {
  mkdir -p cohort tests
  echo '"""Cohort ranking."""' > cohort/__init__.py
  : > tests/__init__.py
}
write_normalize() {
  cat > cohort/normalize.py <<'EOF'
"""Score normalization (FR-1)."""


def normalize_score(value, lo=0, hi=100):
    """Clamp a numeric readiness value into [lo, hi] and scale it to 0..1."""
    v = max(lo, min(hi, value))
    return (v - lo) / (hi - lo)
EOF
  cat > tests/test_normalize.py <<'EOF'
import unittest

from cohort.normalize import normalize_score


class NormalizeTests(unittest.TestCase):
    def test_scales_to_unit_interval(self):
        self.assertEqual(normalize_score(50), 0.5)

    def test_clamps_out_of_range(self):
        self.assertEqual(normalize_score(140), 1.0)
        self.assertEqual(normalize_score(-5), 0.0)
EOF
}
write_selectors() {
  cat > cohort/selectors.py <<'EOF'
"""Selector normalization (FR-4)."""


def normalize_selector(raw):
    return raw.strip().lower().replace(" ", "-")
EOF
  cat > tests/test_selectors.py <<'EOF'
import unittest

from cohort.selectors import normalize_selector


class SelectorTests(unittest.TestCase):
    def test_canonical_form(self):
        self.assertEqual(normalize_selector("  Week 3 Cohort "), "week-3-cohort")
EOF
}

# T004 ranking variants (cohort/ranking.py) and the shared ranking tests.
write_ranking_final() {
  cat > cohort/ranking.py <<'EOF'
"""Ranking (FR-2, FR-3)."""
from .normalize import normalize_score


def rank(learners):
    """Descending readiness; ties broken by name ascending."""
    return sorted(learners, key=lambda l: (-normalize_score(l["readiness"]), l["name"]))
EOF
}
write_ranking_wip() {
  cat > cohort/ranking.py <<'EOF'
"""Ranking (FR-2, FR-3)."""
from .normalize import normalize_score


def _has_ties(ordered):
    scores = [normalize_score(l["readiness"]) for l in ordered]
    return len(scores) != len(set(scores))


def rank(learners):
    ordered = sorted(learners, key=lambda l: -normalize_score(l["readiness"]))
    if _has_ties(ordered):
        raise NotImplementedError("tie-break by name (FR-3)")
    return ordered
EOF
}
write_ranking_defect() {
  cat > cohort/ranking.py <<'EOF'
"""Ranking (FR-2, FR-3)."""
from .normalize import normalize_score


def rank(learners):
    """Descending readiness; ties broken by name ascending."""
    return sorted(
        learners,
        key=lambda l: (normalize_score(l["readiness"]), l["name"]),
        reverse=True,
    )
EOF
}
write_ranking_no_tiebreak() {
  cat > cohort/ranking.py <<'EOF'
"""Ranking (FR-2, FR-3)."""
from .normalize import normalize_score


def rank(learners):
    """Descending readiness (ties keep input order)."""
    return sorted(learners, key=lambda l: -normalize_score(l["readiness"]))
EOF
}
write_ranking_tests() {
  cat > tests/test_ranking.py <<'EOF'
import unittest

from cohort.ranking import rank


def L(name, readiness):
    return {"name": name, "readiness": readiness}


class RankTests(unittest.TestCase):
    def test_rank_by_readiness(self):
        got = [l["name"] for l in rank([L("amy", 40), L("bo", 90), L("cy", 65)])]
        self.assertEqual(got, ["bo", "cy", "amy"])

    def test_tie_break_by_name(self):
        got = [l["name"] for l in rank([L("zed", 70), L("amy", 70), L("bo", 55)])]
        self.assertEqual(got, ["amy", "zed", "bo"])
EOF
}
write_ranking_tests_weak() { # tie test whose input is already in name order
  cat > tests/test_ranking.py <<'EOF'
import unittest

from cohort.ranking import rank


def L(name, readiness):
    return {"name": name, "readiness": readiness}


class RankTests(unittest.TestCase):
    def test_rank_by_readiness(self):
        got = [l["name"] for l in rank([L("amy", 40), L("bo", 90), L("cy", 65)])]
        self.assertEqual(got, ["bo", "cy", "amy"])

    def test_tie_break_by_name(self):
        got = [l["name"] for l in rank([L("amy", 70), L("zed", 70), L("bo", 55)])]
        self.assertEqual(got, ["amy", "zed", "bo"])
EOF
}
write_sample_data_test() {
  cat > tests/test_sample_data.py <<'EOF'
import json
import pathlib
import unittest

from cohort.ranking import rank

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "sample_cohort.json"


class SampleDataTests(unittest.TestCase):
    def test_ranks_upstream_sample(self):
        learners = json.loads(DATA.read_text())
        self.assertEqual(len(rank(learners)), len(learners))
EOF
}

# ---------------------------------------------------------------- history
scaffold_main() { # scaffold_main assumption|oq   (WITH_SAMPLE_DATA=1 adds data/)
  write_readme; write_agents
  [ "${WITH_SAMPLE_DATA:-0}" = 1 ] && write_sample_data
  commit_all "Initial project scaffold" "2026-09-10T09:00:00"
  mkdir -p $SPEC; write_spec "$1"; write_plan "$1"; write_tasks "$1" . . . . . .
  commit_all "Add cohort ranking spec, plan, and task list" "2026-09-10T11:00:00"
}
through_t003() { # leaves the checkout on feat/cohort-ranking with T001-T003 committed
  scaffold_main "$1"
  git checkout -q -b feat/cohort-ranking
  write_package;    write_tasks "$1" x . . . . .
  commit_all "T001: scaffold cohort package and test layout" "2026-09-14T09:30:00"
  write_normalize;  write_tasks "$1" x x . . . .
  commit_all "T002: score normalization (FR-1)" "2026-09-14T14:00:00"
  write_selectors;  write_tasks "$1" x x x . . .
  commit_all "T003: selector normalization (FR-4)" "2026-09-15T10:15:00"
}
commit_t004() { # commit_t004 assumption|oq  -- final ranking + tests, task ticked
  write_ranking_final; write_ranking_tests; write_tasks "$1" x x x x . .
  commit_all "T004: rank learners with name tie-break (FR-2, FR-3)" "2026-09-16T16:20:00"
}
