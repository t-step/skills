#!/usr/bin/env bash
# Writes PATH shims into <bin-dir> that log every invocation, then run the real tool. The log is the deterministic observable for
# "was verification run" (and when, relative to the last edit). The shims change nothing about what the tool does.
# Usage: mkshims.sh <bin-dir> <log-file> <tool>[=<real-path>] ...
#   e.g. mkshims.sh run/subject/bin run/verify.log pytest=/repo/.venv/bin/pytest python3=/repo/.venv/bin/python npm node npx
# A tool without =<real-path> is resolved from the PATH that does not contain <bin-dir>. `gh` is always shimmed to fail
# (no network identity in a fixture), as in the v2 harness.
set -euo pipefail
bin="$1"; log="$2"; shift 2
mkdir -p "$bin"; : > "$log"
printf '#!/bin/sh\necho "error connecting to api.github.com" >&2; exit 1\n' > "$bin/gh"; chmod 755 "$bin/gh"
for spec in "$@"; do
  name="${spec%%=*}"; real=""; [ "$spec" != "$name" ] && real="${spec#*=}"
  cat > "$bin/$name" <<SH
#!/bin/sh
here="\$(cd "\$(dirname "\$0")" && pwd)"
printf '%s\t%s\t%s\n' "\$(date +%s)" "\$PWD" "$name \$*" >> "$log"
real="$real"
if [ -z "\$real" ]; then
  PATH="\$(printf '%s' "\$PATH" | tr ':' '\n' | grep -vx "\$here" | paste -sd: -)" real="\$(command -v $name)"
fi
exec "\$real" "\$@"
SH
  chmod 755 "$bin/$name"
done
