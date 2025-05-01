#!/bin/bash
set -e

# Run the environment setup script first, since there are a lot of os.environ.clear() calls in the code
echo "Entrypoint: Running environment setup..."
/app/.docker/env-setup.sh

# Now, execute the command passed into the container (CMD or docker-compose command)
echo "Entrypoint: Executing command:" "$@"
exec "$@"
