#!/usr/bin/env bash
# Read-only cross-project projectmem search.
#
# Enumerates every project pjm knows about (the registry `pjm dashboard`
# also reads: "${PROJECTMEM_HOME:-$HOME/.projectmem}/projects.json",
# populated by `pjm init` in each repo — projectmem's own storage layer
# honors $PROJECTMEM_HOME, defaulting to ~/.projectmem, so this script
# does too) and runs `pjm search` inside each one, labeling results by
# project directory. This is the existing supported mechanism for
# cross-project lookup in this environment — this script does not talk to
# any projectmem storage directly and never writes anything.
#
# Usage: pjm-cross-project-search.sh "<query>" [--regex]
#
# Exits 0 as a clean, complete "nothing to search" state (prints a note)
# only when there's genuinely no registered-project set to search: the
# registry file doesn't exist yet (no project has ever run `pjm init`),
# or it exists but parses to an empty list. Both are normal, expected
# states, not failures.
#
# Everything else that prevents a real, complete search from happening
# exits nonzero instead: `pjm` not being installed, a registry that
# exists but is unreadable/malformed, or (after the search is attempted)
# one or more individual projects' `pjm search` itself failing. This
# keeps "the search could not run, or did not finish" cleanly separate
# from "the search ran to completion and found nothing" — a caller
# checking only the exit code must not mistake one for the other.
#
# Exit codes: 0 means a real, complete cross-project search happened —
# every registered, still-alive project was searched successfully
# (whether or not anything matched) — or there was genuinely nothing to
# search (no registry file yet, or an empty one). Nonzero means the
# search did not fully complete: `pjm` isn't installed, the registry
# exists but is unreadable/malformed, or at least one individual
# project's `pjm search` failed. A per-project failure does not stop the
# loop — every remaining project is still searched, and any real matches
# from projects that did succeed are still printed — but the overall exit
# code still reflects that this run's cross-project coverage was not
# exhaustive, so a caller must not treat exit 0 as "confirmed complete"
# and must not treat a nonzero run's silence on a given topic as "no
# local evidence found."

set -euo pipefail

QUERY="${1:-}"
shift || true
EXTRA_ARGS=("$@")

if [[ -z "${QUERY}" ]]; then
    echo "usage: pjm-cross-project-search.sh \"<query>\" [--regex]" >&2
    exit 2
fi

REGISTRY_HOME="${PROJECTMEM_HOME:-${HOME}/.projectmem}"
REGISTRY="${REGISTRY_HOME}/projects.json"

if ! command -v pjm >/dev/null 2>&1; then
    echo "pjm CLI not found on PATH — cross-project search unavailable (could not run at all)." >&2
    exit 1
fi

if [[ ! -f "${REGISTRY}" ]]; then
    echo "No cross-project registry found at ${REGISTRY} — no other projectmem-tracked projects known on this machine."
    exit 0
fi

# Parse the registry once, emitting a status line first (OK / EMPTY /
# MALFORMED / READ_ERROR) so the caller can tell "honestly nothing
# registered" apart from "the file is there but broken" instead of both
# silently collapsing into an empty project list.
REGISTRY_LINES=()
while IFS= read -r line; do
    REGISTRY_LINES+=("${line}")
done < <(python3 -c "
import json, sys

# Registry path arrives via argv, never interpolated into this source
# text — a path containing a quote or other shell/Python-meaningful
# character must not be able to break parsing.
path = sys.argv[1]
try:
    with open(path, encoding='utf-8') as f:
        raw = f.read()
except OSError:
    print('READ_ERROR')
    sys.exit(0)

try:
    data = json.loads(raw)
except json.JSONDecodeError:
    print('MALFORMED')
    sys.exit(0)

if not isinstance(data, list):
    print('MALFORMED')
    sys.exit(0)

# Dedupe while preserving order, mirroring projectmem's own
# registered_projects() (storage.py), which does the same.
seen = set()
paths = []
for p in data:
    if isinstance(p, str) and p not in seen:
        seen.add(p)
        paths.append(p)

if not paths:
    print('EMPTY')
    sys.exit(0)

print('OK')
for p in paths:
    print(p)
" "${REGISTRY}")

STATUS="${REGISTRY_LINES[0]:-}"
case "${STATUS}" in
    READ_ERROR)
        echo "Registry file at ${REGISTRY} exists but could not be read — treating cross-project search as unavailable this run (not the same as an empty registry)." >&2
        exit 1
        ;;
    MALFORMED)
        echo "Registry file at ${REGISTRY} is not a valid JSON list of project paths — treating cross-project search as unavailable this run (not the same as an empty registry). Check the file directly." >&2
        exit 1
        ;;
    EMPTY)
        echo "Cross-project registry at ${REGISTRY} is empty — no other projectmem-tracked projects known on this machine."
        exit 0
        ;;
    OK)
        ;;
    *)
        echo "Unexpected registry read result from ${REGISTRY} — treating cross-project search as unavailable this run." >&2
        exit 1
        ;;
esac

PROJECT_DIRS=("${REGISTRY_LINES[@]:1}")

# Resolve the current *project's* root (not just cwd) so a registered
# project matching it can be skipped — Phase 2 of the calling skill
# already searches the current project directly, so searching it again
# here would just duplicate that work. This mirrors projectmem's own
# discovery semantics closely enough for this purpose (storage.py's
# discover_mem_dir/_is_project_mem_dir): walk upward from cwd looking for
# a `.projectmem/` that contains `config.toml` (only `pjm init` writes
# that file; a bare `.projectmem/` — e.g. the machine-wide global store —
# doesn't count). Without this walk-up, invoking the helper from a
# subdirectory like `repo/apps/web/` would fail to recognize `repo/` as
# the current project and search it again as if it were a different one.
resolve_current_project_root() {
    local dir
    dir="$(pwd -P 2>/dev/null)" || return 1
    while true; do
        if [[ -f "${dir}/.projectmem/config.toml" ]]; then
            printf '%s\n' "${dir}"
            return 0
        fi
        if [[ "${dir}" == "/" ]]; then
            return 1
        fi
        dir="$(dirname "${dir}")"
    done
}

CURRENT_RESOLVED="$(resolve_current_project_root)" || CURRENT_RESOLVED=""

FOUND_ANY=0
ANY_FAILURE=0

for dir in "${PROJECT_DIRS[@]}"; do
    if [[ ! -d "${dir}/.projectmem" ]]; then
        echo "## ${dir} — skipped (.projectmem/ missing or removed since registration)"
        echo
        continue
    fi

    DIR_RESOLVED=""
    DIR_RESOLVED="$(cd "${dir}" 2>/dev/null && pwd -P)" || DIR_RESOLVED=""
    if [[ -n "${CURRENT_RESOLVED}" && -n "${DIR_RESOLVED}" && "${DIR_RESOLVED}" == "${CURRENT_RESOLVED}" ]]; then
        echo "## ${dir} — skipped (current project; already covered by the current-project search)"
        echo
        continue
    fi

    echo "## ${dir}"

    SEARCH_EXIT=0
    if [[ ${#EXTRA_ARGS[@]} -gt 0 ]]; then
        OUTPUT="$(cd "${dir}" && pjm search "${QUERY}" "${EXTRA_ARGS[@]}" 2>&1)" || SEARCH_EXIT=$?
    else
        OUTPUT="$(cd "${dir}" && pjm search "${QUERY}" 2>&1)" || SEARCH_EXIT=$?
    fi

    if [[ ${SEARCH_EXIT} -ne 0 ]]; then
        echo "(search failed, exit code ${SEARCH_EXIT} — not treated as a match)"
        echo "${OUTPUT}"
        ANY_FAILURE=1
    elif [[ -z "${OUTPUT}" || "${OUTPUT}" == *"No matching events"* || "${OUTPUT}" == *"no matches"* ]]; then
        echo "(no matches)"
    else
        echo "${OUTPUT}"
        FOUND_ANY=1
    fi
    echo
done

# A partial failure (one or more project searches failed) must never
# exit success — this run's cross-project coverage is incomplete, and a
# caller that only checks the exit code needs to be able to tell that
# apart from a clean, complete "no matches anywhere" result.
if [[ ${ANY_FAILURE} -eq 1 ]]; then
    if [[ ${FOUND_ANY} -eq 1 ]]; then
        echo "Matches were found above, but at least one project's search failed — treat this run's cross-project coverage as incomplete, not exhaustive (see failures above)."
    else
        echo "No confirmed matches for \"${QUERY}\" — at least one project's search failed and this run's cross-project coverage is incomplete, not a clean zero-match result (see failures above)."
    fi
    exit 1
elif [[ ${FOUND_ANY} -eq 0 ]]; then
    echo "No matches for \"${QUERY}\" in any known project."
fi
