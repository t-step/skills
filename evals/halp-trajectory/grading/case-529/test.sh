#!/usr/bin/env bash
# test.sh <dest> [karma-glob]   runs karma test files in headless Chrome (default: refs tests; test/shared needs npm run build). Set CHROME_BIN to override.
set -euo pipefail; cd "${1:?dest}"
export CHROME_BIN="${CHROME_BIN:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
COVERAGE=false BABEL_NO_MODULES=true npx karma start karma.conf.js --single-run --grep="${2:-test/browser/refs.test.js}" 2>&1 | grep -v -e 'Browserslist' -e 'npx update' -e 'Why you should'
