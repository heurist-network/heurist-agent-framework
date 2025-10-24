#!/usr/bin/env bash
set -euo pipefail

# deploy.sh <git-sha>
SHA="${1:-latest}"
REPO_DIR="/root/heurist-agent-framework"
COMPOSE_FILE="$REPO_DIR/docker-compose.yml"
STACK_NAME="mesh"

log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S')] $*"
}

log "===== Starting deployment for SHA=${SHA} ====="

# ─── 0) Ensure this node is in an active Swarm and is a manager ─────────────
log "Checking Docker Swarm status"
SWARM_STATE=$(docker info --format '{{.Swarm.LocalNodeState}}' 2>/dev/null || echo "inactive")
CTRL_AVAIL=$(docker info --format '{{.Swarm.ControlAvailable}}' 2>/dev/null || echo "false")

if [[ "$SWARM_STATE" != "active" ]]; then
  log "ERROR: not part of an active swarm (state=$SWARM_STATE). Aborting."
  exit 1
fi

if [[ "$CTRL_AVAIL" != "true" ]]; then
  log "ERROR: this node is not a Swarm manager (ControlAvailable=$CTRL_AVAIL). Aborting."
  exit 1
fi

# ─── 1) Update local repo with latest compose file etc. ─────────────────────────
log "Running pre-deploy git pull in ${REPO_DIR}"
cd "${REPO_DIR}"
git reset --hard origin/main
git pull origin main

# ─── 2) Pull the exact image tag ─────────────────────────────────────────────
IMAGE="heuristdotai/mesh:${SHA}"
log "Pulling image ${IMAGE}"
docker pull "${IMAGE}"

# ─── 3) Deploy the swarm stack ───────────────────────────────────────────────
log "Deploying stack '${STACK_NAME}' via ${COMPOSE_FILE}"
docker stack deploy \
    --with-registry-auth \
    -c "${COMPOSE_FILE}" \
    "${STACK_NAME}"

# ─── 4) Prune unused containers and images ───────────────────────────────────
docker container prune -f
docker image prune -f
docker image prune -a --filter "until=96h" -f

# ─── 5) Restart x402-gateway via PM2 Control API ─────────────────────────────
log "Restarting x402-gateway via PM2 Control API"
if [[ -n "${PM2_API_SECRET:-}" ]]; then
    # Use timeout and better error handling to prevent deployment failure
    response=$(curl -s --max-time 30 --connect-timeout 10 -X POST https://mesh.heurist.xyz/pm2-control/restart/x402-gateway \
        -H "Authorization: Bearer ${PM2_API_SECRET}" \
        -w "\n%{http_code}\n%{exit_code}" 2>/dev/null || echo -e "error\n000\n1")
    
    # Parse response: body, http_code, curl_exit_code
    body=$(echo "$response" | head -n-2)
    http_code=$(echo "$response" | tail -n2 | head -n1)
    curl_exit_code=$(echo "$response" | tail -n1)

    if [[ "$curl_exit_code" != "0" ]]; then
        log "WARNING: Network error during x402-gateway restart (curl exit code: $curl_exit_code)"
    elif [[ "$http_code" == "200" ]]; then
        log "Successfully restarted x402-gateway: $body"
    elif [[ "$http_code" == "504" ]]; then
        log "WARNING: Gateway timeout (504) when restarting x402-gateway - service may be overloaded"
    else
        log "WARNING: Failed to restart x402-gateway (HTTP $http_code): $body"
    fi
else
    log "WARNING: PM2_API_SECRET not set, skipping x402-gateway restart"
fi

log "===== Deployment finished ====="
