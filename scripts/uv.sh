#!/bin/sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
managed_uv="$repository_root/.tools/bin/uv"

if [ -x "$managed_uv" ]; then
  exec "$managed_uv" "$@"
fi

if command -v uv >/dev/null 2>&1; then
  exec uv "$@"
fi

printf '%s\n' "uv is not installed. Run 'make bootstrap' first." >&2
exit 1
