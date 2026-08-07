#!/bin/sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repository_root"

if ! command -v docker >/dev/null 2>&1; then
  printf '%s\n' "Docker with Compose is required. See docs/development-setup.md." >&2
  exit 1
fi

if [ ! -f .env ]; then
  printf '%s\n' "Missing .env. Run 'make bootstrap' first." >&2
  exit 1
fi

exec docker compose -f docker/compose.yaml up --build
