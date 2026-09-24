#!/usr/bin/env bash
# Fingerprint of a real-repo fixture's observable state (v3). Same intent as evals/halp/fingerprint.sh, but built on git so it stays
# fast on a real checkout and ignores what a real project ignores: installed dependencies and the caches a test run writes are listed in
# .git/info/exclude by each case's setup.sh, so they are not part of the state. Tracked edits are hashed by content, untracked files by
# path and content. A change in any of them is "the agent worked"; a test run alone is not.
# Usage: fingerprint3.sh <repo-dir>
cd "$1" || exit 1
export GIT_OPTIONAL_LOCKS=0 LC_ALL=C
echo "head: $(git rev-parse HEAD 2>/dev/null || echo none)"
echo "branch: $(git symbolic-ref -q --short HEAD || echo detached)"
echo "refs: $(git for-each-ref | shasum | cut -c1-16)"
echo "stashes: $(git stash list | wc -l | tr -d ' ')"
echo "index: $(git ls-files -s | shasum | cut -c1-16)"
echo "tracked-diff: $(git diff HEAD --binary | shasum | cut -c1-16)"
echo "untracked: $(git ls-files -o --exclude-standard -z | sort -z | xargs -0 shasum 2>/dev/null | shasum | cut -c1-16)"
echo "untracked-count: $(git ls-files -o --exclude-standard | wc -l | tr -d ' ')"
echo "merge-in-progress: $([ -e "$(git rev-parse --git-dir)/MERGE_HEAD" ] && echo yes || echo no)"
