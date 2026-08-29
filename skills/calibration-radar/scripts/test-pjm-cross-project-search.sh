#!/usr/bin/env bash
# Deterministic test for pjm-cross-project-search.sh — no real pjm install,
# no real ~/.projectmem/ registry. Builds a temp PROJECTMEM_HOME and a stub
# `pjm` executable on PATH per case, so this is safe to run anywhere,
# including CI. Wired into scripts/check.sh.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SCRIPT="${REPO_ROOT}/skills/calibration-radar/scripts/pjm-cross-project-search.sh"

FAILURES=0
PASSES=0

pass() { PASSES=$((PASSES + 1)); echo "OK: $1"; }
fail() { FAILURES=$((FAILURES + 1)); echo "FAIL: $1"; }

assert_contains() {
    local haystack="$1" needle="$2" label="$3"
    if [[ "${haystack}" == *"${needle}"* ]]; then
        pass "${label}"
    else
        fail "${label} — expected to find: ${needle}"
        echo "--- actual output ---"
        echo "${haystack}"
        echo "---------------------"
    fi
}

assert_not_contains() {
    local haystack="$1" needle="$2" label="$3"
    if [[ "${haystack}" != *"${needle}"* ]]; then
        pass "${label}"
    else
        fail "${label} — should not have found: ${needle}"
        echo "--- actual output ---"
        echo "${haystack}"
        echo "---------------------"
    fi
}

assert_exit() {
    local actual="$1" expected="$2" label="$3"
    if [[ "${actual}" -eq "${expected}" ]]; then
        pass "${label}"
    else
        fail "${label} — expected exit ${expected}, got ${actual}"
    fi
}

# Each case gets its own scratch dir: a fake PROJECTMEM_HOME plus one or
# more fake "project" directories (each needs a .projectmem/ subdir to
# look registered-and-alive), and a stub pjm on PATH ahead of any real
# one, so these tests never touch the real machine's projectmem state.
WORKDIR="$(mktemp -d)"
trap 'rm -rf "${WORKDIR}"' EXIT

mkdir -p "${WORKDIR}/bin"
export PATH="${WORKDIR}/bin:${PATH}"

make_project() {
    # make_project <name> — creates $WORKDIR/<name> with a .projectmem/
    # dir *and* a config.toml inside it (a real `pjm init` always writes
    # config.toml before registering a project — see projectmem's own
    # initialize()/register_project() — so a registered-but-uninitialized
    # project isn't a state real projectmem ever produces; the
    # current-project resolver keys off config.toml specifically to
    # match that). Returns the project's absolute path on stdout.
    local dir="${WORKDIR}/$1"
    mkdir -p "${dir}/.projectmem"
    touch "${dir}/.projectmem/config.toml"
    echo "${dir}"
}

write_stub_pjm() {
    # write_stub_pjm <body> — writes a stub `pjm` script; `search` calls run
    # the given shell body, which sees $PWD as the "current project".
    cat > "${WORKDIR}/bin/pjm" <<EOF
#!/usr/bin/env bash
if [[ "\$1" == "search" ]]; then
    shift
    ${1}
else
    echo "stub pjm: unsupported command \$*" >&2
    exit 1
fi
EOF
    chmod +x "${WORKDIR}/bin/pjm"
}

# --- Case 1: PROJECTMEM_HOME registry resolution ---------------------------
rm -rf "${WORKDIR}"/proj-a "${WORKDIR}"/home-alt
PROJ_A="$(make_project proj-a)"
mkdir -p "${WORKDIR}/home-alt"
printf '["%s"]\n' "${PROJ_A}" > "${WORKDIR}/home-alt/projects.json"
write_stub_pjm 'echo "MATCH from $(pwd)"'
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-alt" HOME="${WORKDIR}/home-should-be-ignored" "${SCRIPT}" "q" 2>&1)"
EXIT=$?
assert_contains "${OUT}" "${PROJ_A}" "PROJECTMEM_HOME registry is read instead of \$HOME/.projectmem"
assert_contains "${OUT}" "MATCH from ${PROJ_A}" "search actually ran inside the registered project"
assert_exit "${EXIT}" 0 "PROJECTMEM_HOME case exits 0"

# --- Case 2: multiple registered projects -----------------------------------
rm -rf "${WORKDIR}"/proj-b "${WORKDIR}"/proj-c "${WORKDIR}"/home-multi
PROJ_B="$(make_project proj-b)"
PROJ_C="$(make_project proj-c)"
mkdir -p "${WORKDIR}/home-multi"
printf '["%s", "%s"]\n' "${PROJ_B}" "${PROJ_C}" > "${WORKDIR}/home-multi/projects.json"
write_stub_pjm 'echo "hit in $(pwd)"'
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-multi" "${SCRIPT}" "q" 2>&1)"
assert_contains "${OUT}" "${PROJ_B}" "multi-project: first project searched"
assert_contains "${OUT}" "${PROJ_C}" "multi-project: second project searched"

# --- Case 3: current-project skipping ---------------------------------------
rm -rf "${WORKDIR}"/proj-self "${WORKDIR}"/proj-other "${WORKDIR}"/home-self
PROJ_SELF="$(make_project proj-self)"
PROJ_OTHER="$(make_project proj-other)"
mkdir -p "${WORKDIR}/home-self"
printf '["%s", "%s"]\n' "${PROJ_SELF}" "${PROJ_OTHER}" > "${WORKDIR}/home-self/projects.json"
write_stub_pjm 'echo "should not run for self"'
OUT="$(cd "${PROJ_SELF}" && PROJECTMEM_HOME="${WORKDIR}/home-self" "${SCRIPT}" "q" 2>&1)"
assert_contains "${OUT}" "skipped (current project" "current-project skip: self is skipped, not searched"
assert_contains "${OUT}" "${PROJ_OTHER}" "current-project skip: the other project is still searched"

# --- Case 4: stale registration (dir/.projectmem gone) ----------------------
rm -rf "${WORKDIR}"/home-stale
STALE_DIR="${WORKDIR}/proj-deleted"
mkdir -p "${WORKDIR}/home-stale"
printf '["%s"]\n' "${STALE_DIR}" > "${WORKDIR}/home-stale/projects.json"
write_stub_pjm 'echo "should not be reached"'
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-stale" "${SCRIPT}" "q" 2>&1)"
assert_contains "${OUT}" "skipped (.projectmem/ missing" "stale registration is skipped gracefully"
assert_not_contains "${OUT}" "should not be reached" "stale registration never invokes pjm search"

# --- Case 5: no-match result --------------------------------------------------
rm -rf "${WORKDIR}"/proj-d "${WORKDIR}"/home-nomatch
PROJ_D="$(make_project proj-d)"
mkdir -p "${WORKDIR}/home-nomatch"
printf '["%s"]\n' "${PROJ_D}" > "${WORKDIR}/home-nomatch/projects.json"
write_stub_pjm 'echo "No matching events"'
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-nomatch" "${SCRIPT}" "q" 2>&1)"
assert_contains "${OUT}" "(no matches)" "no-match result reported as no matches, not a hit"
assert_contains "${OUT}" "No matches for" "no-match summary line printed when nothing found anywhere"

# --- Case 6: actual command failure is not treated as a match, does not
# stop the loop, and makes the whole run exit nonzero -----------------------
# Two registered projects: proj-e (its pjm search fails) and proj-f (its
# pjm search succeeds with a real hit). This exercises all three
# requirements at once: the failure is reported and not counted as a
# match; the loop continues past it to search proj-f anyway; and proj-f's
# real match still shows up even though the overall run is a (nonzero-exit)
# partial failure.
rm -rf "${WORKDIR}"/proj-e "${WORKDIR}"/proj-f "${WORKDIR}"/home-fail
PROJ_E="$(make_project proj-e)"
PROJ_F="$(make_project proj-f)"
touch "${PROJ_E}/FAIL_MARKER"
mkdir -p "${WORKDIR}/home-fail"
printf '["%s", "%s"]\n' "${PROJ_E}" "${PROJ_F}" > "${WORKDIR}/home-fail/projects.json"
# Distinguish per-project behavior via a marker file in the failing
# project's own directory (checked with a plain relative -f test) rather
# than a live `pwd`/`$(...)` comparison embedded in the stub body — the
# stub body passes through write_stub_pjm's unquoted heredoc, which
# expands any `$(...)` in the body immediately (at stub-authoring time),
# not deferred to when the generated stub actually runs.
write_stub_pjm 'if [[ -f "FAIL_MARKER" ]]; then echo "corrupted events.jsonl at line 4" >&2; exit 1; else echo "REAL MATCH in proj-f"; fi'
set +e
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-fail" "${SCRIPT}" "q" 2>&1)"
EXIT=$?
set -e
assert_contains "${OUT}" "search failed" "a failing pjm search is reported as a failure"
assert_contains "${OUT}" "corrupted events.jsonl" "the failure's stderr is shown, not swallowed"
assert_not_contains "${OUT}" $'\n(no matches)\n' "a failed search is not silently reported as no matches"
assert_contains "${OUT}" "REAL MATCH in proj-f" "the loop continues past a failed project and still searches the next one"
assert_contains "${OUT}" "Matches were found above, but at least one project's search failed" "a run with both a real match and a failure reports itself as incomplete, not clean"
assert_exit "${EXIT}" 1 "a partial failure makes the whole run exit nonzero, even when some projects did produce real matches"

# --- Case 6b: a pure failure (no successful matches at all) also exits
# nonzero, distinctly worded from the mixed case above ----------------------
rm -rf "${WORKDIR}"/proj-g "${WORKDIR}"/home-fail-only
PROJ_G="$(make_project proj-g)"
mkdir -p "${WORKDIR}/home-fail-only"
printf '["%s"]\n' "${PROJ_G}" > "${WORKDIR}/home-fail-only/projects.json"
write_stub_pjm 'echo "db locked" >&2; exit 1'
set +e
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-fail-only" "${SCRIPT}" "q" 2>&1)"
EXIT=$?
set -e
assert_contains "${OUT}" "No confirmed matches" "a pure-failure run (no real matches at all) still reports itself distinctly from a clean zero-match result"
assert_exit "${EXIT}" 1 "a pure-failure run also exits nonzero"

# --- Case 7: malformed registry is distinguished from an empty one ---------
rm -rf "${WORKDIR}"/home-malformed
mkdir -p "${WORKDIR}/home-malformed"
echo "not valid json" > "${WORKDIR}/home-malformed/projects.json"
write_stub_pjm 'echo "should not be reached"'
set +e
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-malformed" "${SCRIPT}" "q" 2>&1)"
EXIT=$?
set -e
assert_contains "${OUT}" "not a valid JSON list" "malformed registry produces a distinct message from an empty registry"
assert_not_contains "${OUT}" "is empty —" "malformed registry is not described as merely empty"
assert_exit "${EXIT}" 1 "malformed registry exits nonzero, unlike a genuinely empty registry"

# --- Case 8: nested current-project detection -------------------------------
# The current project is registered at its root, but the helper is
# invoked from a subdirectory a few levels deep (e.g. repo/apps/web/) —
# it must still resolve up to the registered root and skip it, not treat
# cwd itself as the identity to compare against.
rm -rf "${WORKDIR}"/proj-nested-self "${WORKDIR}"/proj-nested-other "${WORKDIR}"/home-nested
PROJ_NESTED_SELF="$(make_project proj-nested-self)"
NESTED_SUBDIR="${PROJ_NESTED_SELF}/apps/web"
mkdir -p "${NESTED_SUBDIR}"
touch "${PROJ_NESTED_SELF}/SELF_MARKER"
PROJ_NESTED_OTHER="$(make_project proj-nested-other)"
mkdir -p "${WORKDIR}/home-nested"
printf '["%s", "%s"]\n' "${PROJ_NESTED_SELF}" "${PROJ_NESTED_OTHER}" > "${WORKDIR}/home-nested/projects.json"
write_stub_pjm 'if [[ -f "SELF_MARKER" ]]; then echo "SHOULD NOT RUN FOR SELF"; else echo "OTHER PROJECT MATCH"; fi'
OUT="$(cd "${NESTED_SUBDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-nested" "${SCRIPT}" "q" 2>&1)"
assert_not_contains "${OUT}" "SHOULD NOT RUN FOR SELF" "nested invocation: pjm search is never actually invoked inside the current project's root"
assert_contains "${OUT}" "skipped (current project" "nested invocation: current project is still resolved (by walking up to its .projectmem/config.toml) and skipped from a subdirectory"
assert_contains "${OUT}" "OTHER PROJECT MATCH" "nested invocation: the other project is still searched normally"

# --- Case 9: a registry path containing a quote character doesn't break
# the Python parsing step (registry path is passed via argv, never
# interpolated into Python source text) ---------------------------------
rm -rf "${WORKDIR}/home's-quote" "${WORKDIR}"/proj-quote
PROJ_QUOTE="$(make_project proj-quote)"
QUOTE_HOME="${WORKDIR}/home's-quote"
mkdir -p "${QUOTE_HOME}"
printf '["%s"]\n' "${PROJ_QUOTE}" > "${QUOTE_HOME}/projects.json"
write_stub_pjm 'echo "quote-path match"'
set +e
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${QUOTE_HOME}" "${SCRIPT}" "q" 2>&1)"
EXIT=$?
set -e
assert_contains "${OUT}" "quote-path match" "a PROJECTMEM_HOME path containing a single quote still parses the registry and searches correctly"
assert_exit "${EXIT}" 0 "a quoted registry path does not crash or otherwise break the script"

# --- Case 10: duplicate registry entries are deduped (mirrors projectmem's
# own registered_projects(), which dedupes the same way) --------------------
rm -rf "${WORKDIR}"/proj-dup "${WORKDIR}"/home-dup
PROJ_DUP="$(make_project proj-dup)"
mkdir -p "${WORKDIR}/home-dup"
printf '["%s", "%s"]\n' "${PROJ_DUP}" "${PROJ_DUP}" > "${WORKDIR}/home-dup/projects.json"
write_stub_pjm 'echo "dup match"'
OUT="$(cd "${WORKDIR}" && PROJECTMEM_HOME="${WORKDIR}/home-dup" "${SCRIPT}" "q" 2>&1)"
HEADER_COUNT="$(grep -c "^## ${PROJ_DUP}$" <<< "${OUT}")"
if [[ "${HEADER_COUNT}" -eq 1 ]]; then
    pass "duplicate registry entries are deduped (searched once, not once per duplicate)"
else
    fail "duplicate registry entries are deduped (searched once, not once per duplicate) — got ${HEADER_COUNT} occurrences"
fi

# --- Case 11: pjm not installed / not found on PATH at all ------------------
# Build a PATH with every directory that actually contains a `pjm`
# executable removed — including $WORKDIR/bin, where every prior case's
# stub lives — rather than relying on the test machine happening not to
# have pjm installed. This makes the case deterministic regardless of the
# host machine's actual state.
NO_PJM_PATH=""
IFS=':' read -ra PATH_DIRS <<< "${PATH}"
for d in "${PATH_DIRS[@]}"; do
    if [[ -n "${d}" && ! -x "${d}/pjm" ]]; then
        NO_PJM_PATH="${NO_PJM_PATH:+${NO_PJM_PATH}:}${d}"
    fi
done
set +e
OUT="$(PATH="${NO_PJM_PATH}" "${SCRIPT}" "q" 2>&1)"
EXIT=$?
set -e
assert_contains "${OUT}" "cross-project search unavailable" "no-pjm: message clearly states cross-project search is unavailable"
assert_exit "${EXIT}" 1 "no-pjm: pjm not found on PATH at all makes the run exit nonzero, not a clean success"

echo
if [[ ${FAILURES} -eq 0 ]]; then
    echo "test-pjm-cross-project-search: OK (${PASSES} checks passed)"
    exit 0
else
    echo "test-pjm-cross-project-search: FAIL (${FAILURES} failed, ${PASSES} passed)"
    exit 1
fi
