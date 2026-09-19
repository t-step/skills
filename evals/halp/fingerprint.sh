#!/usr/bin/env bash
# Prints a fingerprint of a fixture repo's observable state, so a run can be
# checked for mutation by diffing before/after. Caches a test run would create
# (__pycache__, .pytest_cache) are counted separately: they are side effects
# of running tests, not edits, and shouldn't mask or mimic one.
# Usage: fingerprint.sh <repo-dir>
cd "$1" || exit 1
if git rev-parse --git-dir >/dev/null 2>&1; then
  echo "head: $(git rev-parse HEAD 2>/dev/null || echo none)"
  echo "branch: $(git symbolic-ref -q --short HEAD || echo detached)"
  echo "refs: $(git for-each-ref | shasum | cut -c1-16)"
  echo "stashes: $(git stash list | wc -l | tr -d ' ')"
  echo "index: $(git ls-files -s | shasum | cut -c1-16)"
  echo "merge-in-progress: $([ -e "$(git rev-parse --git-dir)/MERGE_HEAD" ] && echo yes || echo no)"
else
  echo "head: not-a-repo"
fi
echo "files: $(find . -path ./.git -prune -o \( -name __pycache__ -o -name .pytest_cache \) -prune -o -type f -print0 | sort -z | xargs -0 shasum | shasum | cut -c1-16)"
echo "cache-dirs: $(find . -path ./.git -prune -o \( -name __pycache__ -o -name .pytest_cache \) -print | wc -l | tr -d ' ')"
