#!/bin/bash
set -e

ENV_FILE="/app/.env"

if [ -z "${HEURIST_API_KEY}" ] || [ -z "${PROTOCOL_V2_AUTH_TOKEN}" ]; then
    echo "Error: missing HEURIST_API_KEY or PROTOCOL_V2_AUTH_TOKEN"
    exit 1
fi

# This is needed because there are a lot of os.environ.clear() calls in the code,
# which would otherwise clear the environment variables set in the Dockerfile.
# This is a workaround to save the environment variables to a file that can be used by python-dotenv.
mkdir -p "$(dirname "$ENV_FILE")" 2>/dev/null

# Filter out system/build variables and save the rest for python-dotenv
env | grep -v '^PYTHON_SHA256\|^HOSTNAME\|^PYTHON_VERSION\|^UV_COMPILE_BYTECODE\|^PWD\|^HOME\|^LANG\|^GPG_KEY\|^TERM\|^SHLVL\|^PATH\|^_\|^OLDPWD\|^UV_LINK_MODE=' >"$ENV_FILE" && echo "Entrypoint: Environment saved to $ENV_FILE"

# Now, execute the command passed into the container (from docker-compose)
echo "Entrypoint: Executing command:" "$@"
exec "$@"
