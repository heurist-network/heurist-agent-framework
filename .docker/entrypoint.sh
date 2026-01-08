#!/bin/bash
set -e

ENV_FILE="/app/.env"
REQUIRED_VARS=("HEURIST_API_KEY")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -ne 0 ]; then
    echo "[Entrypoint] Error: Missing required environment variables: ${MISSING_VARS[*]}" >&2
    exit 1
fi

# Variables to exclude from the .env file, which are system/build/runtime variables and not needed by the application
EXCLUDE_REGEX='^PYTHON_SHA256=|^HOSTNAME=|^PYTHON_VERSION=|^UV_COMPILE_BYTECODE=|^HOME=|^LANG=|^GPG_KEY=|^TERM=|^PATH=|^OLDPWD=|^UV_LINK_MODE='

echo "[Entrypoint] Preparing .env file at ${ENV_FILE}..."
mkdir -p "$(dirname "$ENV_FILE")" 2>/dev/null

if env | grep -v -E "${EXCLUDE_REGEX}" >"$ENV_FILE"; then
    echo "[Entrypoint] Successfully saved filtered environment to ${ENV_FILE}."
else
    echo "[Entrypoint] Error: Failed to save environment to ${ENV_FILE}." >&2
    exit 1
fi

# Execute the command passed into the container by docker-compose
echo "[Entrypoint] Handing over execution to command:" "$@"
exec "$@"

# This line should not be reached if exec is successful
echo "[Entrypoint] Error: exec command failed!" >&2
exit 1
