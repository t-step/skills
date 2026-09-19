#!/usr/bin/env bash
# Shared deterministic builders for the halp held-out fixtures (sourced by each
# cases/case-NNN/setup.sh). Fixed dates and content. Each fixture is a small,
# differently-shaped repository; none reuses the development suite's project.
set -euo pipefail

put() { mkdir -p "$(dirname "$1")"; cat > "$1"; }                  # put <path> <<'EOF' ... EOF
new_repo() { # new_repo <abs-dir> [branch]
  rm -rf "$1"; mkdir -p "$1"; cd "$1"; git init -q -b "${2:-main}"
  git config commit.gpgsign false; git config user.name "Fixture Author"; git config user.email "fixture@example.invalid"
}
new_dir() { rm -rf "$1"; mkdir -p "$1"; cd "$1"; }
commit_all() { git add -A; GIT_AUTHOR_DATE="$2" GIT_COMMITTER_DATE="$2" git commit -q -m "$1"; }   # <msg> <iso>
commit_paths() { local m="$1" d="$2"; shift 2; git add -- "$@"; GIT_AUTHOR_DATE="$d" GIT_COMMITTER_DATE="$d" git commit -q -m "$m"; }
stamp() { local t="$1"; shift; touch -t "$t" "$@"; }             # stamp YYYYMMDDhhmm files...
sync_mtimes() { # give every tracked file the date of the last commit that touched it (repeatable mtimes)
  local f t
  git ls-files | while read -r f; do t=$(git log -1 --format=%cd --date=format:%Y%m%d%H%M -- "$f"); touch -t "$t" "$f"; done
}
# make_origin <fake-url> [branches...]: real local bare origin so remote-tracking refs exist, URL rewritten to a
# GitHub-looking address afterwards (nothing is ever fetched from it).
make_origin() {
  local url="$1"; shift; local bare; bare="$(pwd).origin"; rm -rf "$bare"; git init -q --bare "$bare"
  git remote add origin "$bare"; for b in "$@"; do git push -q origin "$b"; done
  git remote set-url origin "$url"
}
gh_shim() { # gh_shim <out-dir> <open|none|unauth>  -> ../bin/gh, a deterministic stand-in for `gh pr view`
  local d; d="$(dirname "$1")/bin"; mkdir -p "$d"
  case "$2" in
    open)   printf '#!/bin/sh\necho "#37 OPEN review=CHANGES_REQUESTED https://github.com/acme/notes-api/pull/37"\n' > "$d/gh";;
    none)   printf '#!/bin/sh\necho "no pull requests found for branch \\"fix/retry-jitter\\"" >&2; exit 1\n' > "$d/gh";;
    unauth) printf '#!/bin/sh\necho "gh: To use GitHub CLI, run: gh auth login" >&2; exit 4\n' > "$d/gh";;
  esac; chmod +x "$d/gh"
}
