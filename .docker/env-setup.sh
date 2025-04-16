#!/bin/bash
set -e

ENV_FILE="/app/.env"

if [ -z "${HEURIST_API_KEY}" ] || [ -z "${PROTOCOL_V2_AUTH_TOKEN}" ]; then
    echo "Error: missing HEURIST_API_KEY or PROTOCOL_V2_AUTH_TOKEN"
    exit 1
fi

mkdir -p "$(dirname "$ENV_FILE")" 2>/dev/null
env | grep -v "^PYTHON_SHA256\|^HOSTNAME\|^PYTHON_VERSION\|^UV_COMPILE_BYTECODE\|^PWD\|^HOME\|^LANG\|^GPG_KEY\|^TERM\|^SHLVL\|^PATH\|^_\|^OLDPWD\|^SUPERVISOR_GROUP_NAME\|^GITHUB_SHA\|^UV_LINK_MODE\|^SUPERVISOR_ENABLED=" >"$ENV_FILE" && echo "✓ Environment saved to $ENV_FILE"
