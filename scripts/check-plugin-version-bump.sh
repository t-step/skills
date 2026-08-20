#!/usr/bin/env bash
# Enforces: if plugins/software-engineering/ runtime contents changed vs the
# PR base, plugin.json's version must be strictly greater than the base's.
#
# Plain bash/jq comparison (no third-party action) because the only thing
# being compared is a plain X.Y.Z semver string in one manifest field --
# pulling in a semver library or GitHub Action for that would be more
# machinery than the check warrants. Pre-release/build-metadata suffixes
# (e.g. "1.0.0-rc.1") are not supported; this repo's manifests use plain
# X.Y.Z versions only.
set -euo pipefail

PLUGIN_DIR="plugins/software-engineering"
MANIFEST="$PLUGIN_DIR/.claude-plugin/plugin.json"
BASE_REF="${1:?usage: check-plugin-version-bump.sh <base-ref>}"

changed=$(git diff --name-only "$BASE_REF"...HEAD -- "$PLUGIN_DIR")
if [ -z "$changed" ]; then
  echo "No changes under $PLUGIN_DIR; version bump not required."
  exit 0
fi

echo "Changed files under $PLUGIN_DIR:"
echo "$changed"

if ! git cat-file -e "$BASE_REF:$MANIFEST" 2>/dev/null; then
  echo "$MANIFEST does not exist at $BASE_REF (plugin is new in this PR); no prior version to bump from."
  exit 0
fi

base_version=$(git show "$BASE_REF:$MANIFEST" | jq -r .version)
head_version=$(jq -r .version "$MANIFEST")

version_gt() {
  local IFS=.
  local -a a=($1) b=($2)
  for i in 0 1 2; do
    local x=${a[$i]:-0}
    local y=${b[$i]:-0}
    if ((10#$x > 10#$y)); then return 0; fi
    if ((10#$x < 10#$y)); then return 1; fi
  done
  return 1
}

if version_gt "$head_version" "$base_version"; then
  echo "Version bump OK: $base_version -> $head_version"
else
  echo "::error::$PLUGIN_DIR changed but plugin.json version was not bumped above base ($base_version -> $head_version)."
  exit 1
fi
