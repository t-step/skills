#!/usr/bin/env bash
# HALP evidence collector: read-only, deterministic, interprets nothing.
# Usage: collect-evidence.sh [dir]     (default: current directory)
# Prints a labeled plain-text evidence packet. Sources it cannot reach are
# reported as such, never guessed. Runs no tests, writes no files.
set -u
export GIT_OPTIONAL_LOCKS=0 LC_ALL=C

cd "${1:-.}" 2>/dev/null || { echo "cannot cd to ${1:-.}"; exit 0; }

section() { printf '\n== %s ==\n' "$1"; }
if stat -c %y . >/dev/null 2>&1; then
  mtime() { stat -c %y "$1" | cut -c1-16; }; epoch() { stat -c %Y "$1"; }
else
  mtime() { stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$1"; }; epoch() { stat -f %m "$1"; }
fi
with_timeout() {
  if command -v timeout >/dev/null 2>&1; then timeout 8 "$@"
  elif command -v gtimeout >/dev/null 2>&1; then gtimeout 8 "$@"
  else "$@"; fi
}

section "collected"
echo "at: $(date '+%Y-%m-%d %H:%M %Z') (all times below are local)"

in_git=0
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  in_git=1
  cd "$(git rev-parse --show-toplevel)" || exit 0
fi
echo "dir: $PWD"

if [ "$in_git" = 1 ]; then
  section "repo"
  branch=$(git symbolic-ref --short -q HEAD || echo "(detached)")
  echo "branch: $branch"
  head=$(git log -1 --format='%h %ad %s' --date=format:'%Y-%m-%d %H:%M' 2>/dev/null)
  echo "HEAD: ${head:-(no commits yet)}"
  gd=$(git rev-parse --git-dir); ops=""
  for m in MERGE_HEAD:merge CHERRY_PICK_HEAD:cherry-pick REVERT_HEAD:revert \
           rebase-merge:rebase rebase-apply:rebase BISECT_LOG:bisect; do
    [ -e "$gd/${m%%:*}" ] && ops="$ops ${m##*:}"
  done
  echo "in-progress operation:${ops:- none}"
  remotes=$(git remote -v | awk '{print $1" "$2}' | sort -u)
  if [ -n "$remotes" ]; then echo "remotes: $(echo "$remotes" | tr '\n' ';')"; else echo "remotes: none"; fi
  up=$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null)
  if [ -n "$up" ]; then
    echo "upstream: $up (ahead/behind: $(git rev-list --left-right --count HEAD...@{upstream} | tr '\t' '/'))"
  else echo "upstream: none configured"; fi
  base=""; how=""
  ohead=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null)
  if [ -n "$ohead" ] && git rev-parse --verify -q "$ohead" >/dev/null 2>&1; then base=$ohead; how="from origin/HEAD"; else
    for c in origin/main main origin/master master origin/develop develop origin/trunk trunk; do
      git rev-parse --verify -q "$c" >/dev/null 2>&1 && { base=$c; how="guessed by name"; break; }
    done
  fi
  if [ -z "$base" ]; then echo "base branch: none found (no origin/HEAD, and no main/master/develop/trunk)"
  elif [ "$branch" = "${base#origin/}" ]; then echo "base branch: $base ($how; this is it)"
  else echo "vs $base ($how): behind/ahead $(git rev-list --left-right --count "$base"...HEAD | tr '\t' '/')"; fi
  echo "stashes: $(git stash list | wc -l | tr -d ' ')"
  echo "other local branches, newest commit first:"
  git for-each-ref --sort=-committerdate --count=6 refs/heads \
    --format='  %(refname:short) | %(committerdate:format:%Y-%m-%d %H:%M) | %(subject)' \
    | grep -v "^  $branch |" | head -5

  section "working tree"
  status=$(git status --porcelain=v1 -unormal)
  if [ -z "$status" ]; then echo "clean"; else
    printf '%s\n' "$status" | awk '{x=substr($0,1,1); y=substr($0,2,1)
      if ($0 ~ /^\?\?/) u++; else if (x=="U"||y=="U"||$0 ~ /^(AA|DD)/) c++
      else { if (x!=" ") s++; if (y!=" ") m++ } }
      END{printf "files with staged changes: %d, unstaged: %d, untracked: %d, conflicted: %d\n", s,m,u,c}'
    echo "(XY path: X=staged, Y=unstaged, ??=untracked, U=conflict)"
    printf '%s\n' "$status" | head -25
    n=$(printf '%s\n' "$status" | wc -l | tr -d ' '); [ "$n" -gt 25 ] && echo "... +$((n-25)) more"
    echo "unstaged diff: $(git diff --shortstat | sed 's/^ //' | grep . || echo none)"
    echo "staged diff:   $(git diff --cached --shortstat | sed 's/^ //' | grep . || echo none)"
    newest=""; newest_t=0
    for f in $(git ls-files -m -o --exclude-standard | head -200); do
      [ -f "$f" ] || continue
      t=$(epoch "$f"); [ "$t" -gt "$newest_t" ] && { newest_t=$t; newest=$f; }
    done
    [ -n "$newest" ] && echo "most recently modified changed file: $newest ($(mtime "$newest"))"
  fi

  section "recent commits"
  if [ -n "$base" ] && [ "$branch" != "${base#origin/}" ]; then
    echo "on this branch, not on $base:"
    git log "$base"..HEAD -10 --format='  %h %ad %s' --date=format:'%Y-%m-%d %H:%M'
  else
    echo "last 8:"
    git log -8 --format='  %h %ad %s' --date=format:'%Y-%m-%d %H:%M' 2>/dev/null
  fi
else
  section "repo"
  echo "not a git repository: no branch, commit, or working-tree evidence"
fi

section "task / plan / spec artifacts"
found=$(find . -maxdepth 4 \( -name .git -o -name node_modules -o -name .venv -o -name vendor \) -prune -o \
  -type f \( -iname 'tasks.md' -o -iname 'todo.md' -o -iname 'plan.md' -o -iname 'spec.md' \
  -o -iname 'roadmap.md' -o -iname 'progress.md' -o -iname 'status.md' -o -iname 'handoff.md' \
  -o -iname 'decisions.md' \) -print | sort | head -20)
if [ -z "$found" ]; then echo "none found"; else
  printf '%s\n' "$found" | while read -r f; do
    st=""
    if [ "$in_git" = 1 ]; then
      if ! git ls-files --error-unmatch "$f" >/dev/null 2>&1; then st="untracked"
      elif [ -n "$(git status --porcelain -- "$f")" ]; then st="tracked, modified since last commit"
      else st="tracked, unchanged"; fi
    fi
    done_n=$(grep -cE '^[[:space:]]*[-*] \[[xX]\]' "$f"); open_n=$(grep -cE '^[[:space:]]*[-*] \[ \]' "$f")
    echo "$f | modified $(mtime "$f") | ${st:-not in git} | checkboxes: $done_n done, $open_n open"
    grep -E '^[[:space:]]*[-*] \[ \]' "$f" | head -3 | sed 's/^/    open: /'
  done
fi
for d in .projectmem .specify; do [ -d "$d" ] && echo "tool state dir present (not read here): $d/"; done
for f in AGENTS.md CLAUDE.md; do [ -f "$f" ] && echo "instructions present: $f"; done

section "verification artifacts (existing files only; nothing was run)"
ver=$(find . -maxdepth 3 \( -name .git -o -name node_modules -o -name .venv \) -prune -o -type f \
  \( -name '*.log' -o -name 'junit*.xml' -o -name lastfailed -o -path './test-results/*' \
     -o -path './logs/*' -o -name 'coverage*.xml' \) -print | head -8)
if [ -z "$ver" ]; then echo "none found"; else
  printf '%s\n' "$ver" | while read -r f; do echo "$f | modified $(mtime "$f")"; done
fi

section "pull request"
origin=""
[ "$in_git" = 1 ] && origin=$(git remote get-url origin 2>/dev/null)
case "$origin" in
  *github.com*)
    if command -v gh >/dev/null 2>&1; then
      out=$(GH_PROMPT_DISABLED=1 with_timeout gh pr view --json number,state,isDraft,reviewDecision,url \
        --jq '"#\(.number) \(.state)\(if .isDraft then " (draft)" else "" end) review=\(.reviewDecision // "none") \(.url)"' 2>&1)
      echo "${out:-no output}" | head -3
    else echo "not attempted (gh not installed)"; fi ;;
  *) echo "not attempted (no GitHub origin remote)" ;;
esac

section "not collected"
echo "test/lint/typecheck results (never run here), CI beyond the PR line, and the conversation"
