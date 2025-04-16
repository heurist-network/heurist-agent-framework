#!/bin/bash
set -e

ENV_FILE="/app/mesh/.env"

if [ -z "${HEURIST_API_KEY}" ] || [ -z "${PROTOCOL_V2_AUTH_TOKEN}" ]; then
    echo "Error: missing HEURIST_API_KEY or PROTOCOL_V2_AUTH_TOKEN"
    exit 1
fi

mkdir -p "$(dirname "$ENV_FILE")" 2>/dev/null
env >"$ENV_FILE" && echo "✓ Environment saved to $ENV_FILE"
