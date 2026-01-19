"""Proxy Fallback Client for handling rate limits via standby proxy servers."""

import logging
import os
from typing import Any, Dict, List, Optional

import aiohttp

logger = logging.getLogger(__name__)

RETRYABLE_STATUS_CODES = {
    429,  # Too Many Requests (rate limit on proxy itself)
    500,  # Internal Server Error
    502,  # Bad Gateway
    503,  # Service Unavailable
    504,  # Gateway Timeout
}


class ProxyFallbackClient:
    """Client for forwarding requests through standby proxy servers.

    When the primary API request hits a rate limit (429), this client
    forwards the request to standby proxy servers that have different IPs.
    If a proxy server fails (500, 402, timeout, etc.), it tries the next one.
    """

    def __init__(self):
        self.enabled = os.getenv("PROXY_ENABLED", "false").lower() == "true"
        servers_env = os.getenv("MESH_PROXY_URLS") or os.getenv("PROXY_SERVERS", "")
        self.servers = [s.strip() for s in servers_env.split(",") if s.strip()]
        self.auth_key = os.getenv("HEURIST_API_KEY", "")
        self.timeout = int(os.getenv("PROXY_TIMEOUT", "30"))
        self._current_server_idx = 0

        if self.enabled and self.servers:
            logger.info(f"ProxyFallbackClient initialized with {len(self.servers)} server(s)")
        elif self.enabled:
            logger.warning("ProxyFallbackClient enabled but no servers configured")

    def _get_servers_ordered(self) -> List[str]:
        """Get servers in round-robin order starting from current index.

        This ensures load distribution across servers when multiple requests come in.
        """
        if not self.servers:
            return []
        ordered = self.servers[self._current_server_idx:] + self.servers[:self._current_server_idx]
        self._current_server_idx = (self._current_server_idx + 1) % len(self.servers)

        return ordered

    async def forward_request(
        self,
        agent_name: str,
        api_url: str,
        method: str = "GET",
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Forward request to standby proxy server.

        Sends the complete payload (including headers with API keys) to the proxy.
        Tries ALL servers in round-robin order until one succeeds.
        On failure (500, 402, 429, timeout, connection error), moves to next server.

        Args:
            agent_name: Name of the agent making the request (for logging)
            api_url: The external API URL to call
            method: HTTP method (GET, POST, etc.)
            headers: Complete headers to forward (including Authorization if needed)
            params: Query parameters for the external API
            json_data: JSON body for POST requests

        Returns:
            {"status": "success", "data": {...}} on success
            {"status": "error", "error": "..."} on failure
        """
        if not self.enabled:
            return {"status": "error", "error": "Proxy fallback is not enabled"}

        if not self.servers:
            return {"status": "error", "error": "No proxy servers configured"}

        if not self.auth_key:
            return {"status": "error", "error": "HEURIST_API_KEY not configured for proxy authentication"}

        payload = {
            "agent_name": agent_name,
            "api_url": api_url,
            "method": method,
        }
        if headers:
            payload["headers"] = headers
        if params:
            payload["params"] = params
        if json_data:
            payload["json_data"] = json_data

        errors = []
        timeout_cfg = aiohttp.ClientTimeout(total=self.timeout)
        servers_to_try = self._get_servers_ordered()
        total_servers = len(servers_to_try)

        async with aiohttp.ClientSession() as session:
            for idx, server_url in enumerate(servers_to_try):
                proxy_endpoint = f"{server_url.rstrip('/')}/proxy"

                try:
                    logger.info(f"Proxy attempt {idx + 1}/{total_servers} | server={server_url} | agent={agent_name}")

                    async with session.post(
                        proxy_endpoint,
                        json=payload,
                        headers={
                            "Authorization": f"Bearer {self.auth_key}",
                            "Content-Type": "application/json",
                        },
                        timeout=timeout_cfg,
                    ) as response:
                        try:
                            response_data = await response.json()
                        except Exception:
                            response_data = {"error": f"Invalid JSON response (HTTP {response.status})"}

                        if response.status == 200 and response_data.get("status") == "success":
                            logger.info(f"Proxy fallback successful via {server_url}")
                            return response_data

                        if response.status in RETRYABLE_STATUS_CODES:
                            error_msg = response_data.get("error", f"HTTP {response.status}")
                            errors.append(f"{server_url}: {error_msg}")
                            logger.warning(f"Proxy server retryable error | server={server_url} | status={response.status} | error={error_msg}")
                            continue  # Try next server

                        error_msg = response_data.get("error", f"HTTP {response.status}")
                        errors.append(f"{server_url}: {error_msg}")
                        logger.warning(f"Proxy server error | server={server_url} | status={response.status} | error={error_msg}")
                        continue

                except aiohttp.ClientError as e:
                    error_msg = f"Connection error: {str(e)}"
                    errors.append(f"{server_url}: {error_msg}")
                    logger.warning(f"Proxy connection failed | server={server_url} | error={error_msg}")
                    continue

                except TimeoutError:
                    error_msg = "Request timeout"
                    errors.append(f"{server_url}: {error_msg}")
                    logger.warning(f"Proxy request timeout | server={server_url}")
                    continue

                except Exception as e:
                    error_msg = f"Unexpected error: {str(e)}"
                    errors.append(f"{server_url}: {error_msg}")
                    logger.error(f"Proxy unexpected error | server={server_url} | error={error_msg}")
                    continue

        # All servers failed
        logger.error(f"All {total_servers} proxy servers failed | agent={agent_name} | errors={errors}")
        return {
            "status": "error",
            "error": f"All {total_servers} proxy servers failed: {'; '.join(errors)}",
        }


# Singleton instance
_proxy_client: Optional[ProxyFallbackClient] = None


def get_proxy_client() -> ProxyFallbackClient:
    """Get or create the singleton ProxyFallbackClient instance."""
    global _proxy_client
    if _proxy_client is None:
        _proxy_client = ProxyFallbackClient()
    return _proxy_client
