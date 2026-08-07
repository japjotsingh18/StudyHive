#!/bin/sh
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repository_root"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf '%s\n' "Missing required command: $1" >&2
    exit 1
  fi
}

require_command curl
require_command node
require_command corepack
require_command git

if [ ! -f .env ]; then
  cp .env.example .env
  printf '%s\n' "Created .env from safe local defaults."
fi

mkdir -p .tools/bin

if [ ! -x .tools/bin/uv ] && ! command -v uv >/dev/null 2>&1; then
  temporary_directory=$(mktemp -d "${TMPDIR:-/tmp}/studyhive-uv.XXXXXX")
  trap 'rm -rf "$temporary_directory"' EXIT HUP INT TERM
  installer="$temporary_directory/uv-installer.sh"
  curl --proto '=https' --tlsv1.2 -LsSf \
    https://releases.astral.sh/github/uv/releases/download/0.12.0/uv-installer.sh \
    -o "$installer"
  UV_INSTALL_DIR="$repository_root/.tools/bin" UV_NO_MODIFY_PATH=1 sh "$installer"
fi

corepack prepare pnpm@10.17.1 --activate
pnpm install --frozen-lockfile
./scripts/uv.sh sync --all-packages --group dev --frozen

printf '%s\n' "StudyHive bootstrap complete. Run 'make dev' to start the local stack."
