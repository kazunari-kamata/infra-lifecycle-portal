#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
FRONTEND_DIR="${REPO_ROOT}/app/frontend"

docker run --rm \
  --user "$(id -u):$(id -g)" \
  --env npm_config_cache=/tmp/.npm \
  --volume "${FRONTEND_DIR}:/workspace" \
  --workdir /workspace \
  node:22-slim \
  npm "$@"
