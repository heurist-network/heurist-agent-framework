"""URL validation utilities to prevent SSRF attacks.

Validates that URLs do not resolve to private/internal IP ranges
before fetching. Opt-in: call validate_url_not_private() before
any aiohttp/requests fetch of user- or admin-supplied URLs.
"""

import ipaddress
import socket
import logging
from typing import List
from urllib.parse import urlparse

from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Default blocked networks — private IPs, link-local, cloud metadata
DEFAULT_BLOCKED_NETWORKS: List[ipaddress.IPv4Network | ipaddress.IPv6Network] = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("fd00::/8"),
    ipaddress.ip_network("::1/128"),
]

# Opt-in flag: set to True to enable SSRF validation globally
# Default False to avoid breaking existing deployments
SSRF_VALIDATION_ENABLED: bool = False


def validate_url_not_private(url: str, blocked_networks=None) -> str:
    """Validate that a URL does not resolve to a private/internal IP.

    Resolves the hostname via DNS and checks against blocked networks.
    Raises HTTPException 400 if the URL is unsafe.

    Args:
        url: The URL to validate.
        blocked_networks: Override default blocked networks list.

    Returns:
        The original URL if validation passes.

    Raises:
        HTTPException: If the URL scheme is not http/https,
            hostname is missing, or IP resolves to a blocked range.
    """
    if not SSRF_VALIDATION_ENABLED:
        return url

    networks = blocked_networks or DEFAULT_BLOCKED_NETWORKS

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=400, detail="Only http and https URLs are allowed")

    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="Invalid URL: no hostname")

    try:
        addr_infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        raise HTTPException(status_code=400, detail=f"Cannot resolve hostname: {hostname}")

    for _, _, _, _, addr in addr_infos:
        ip_str = addr[0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            continue
        for net in networks:
            if ip in net:
                logger.warning(f"SSRF blocked: URL {url} resolves to private IP {ip_str}")
                raise HTTPException(
                    status_code=400,
                    detail=f"URL resolves to private/internal IP address ({ip_str}). Fetching internal URLs is not allowed.",
                )

    return url
