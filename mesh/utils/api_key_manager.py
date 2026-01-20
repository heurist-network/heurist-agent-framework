"""
API Key Manager utility for handling multiple API keys with rotation support.

Supports two rotation modes:
- Error-based: Rotate on specific errors (e.g., 429 rate limit), skip on others (500, 404, 422)
- Time-based: Rotate after a specified interval
"""

import logging
import random
import time
from typing import Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

DEFAULT_NON_ROTATABLE_ERRORS = ["500", "404", "422", "not found", "unprocessable"]


class APIKeyManager:
    """
    Manages multiple API keys with rotation support.

    Args:
        api_keys: List of API keys
        rotation_mode: "error" for error-based rotation, "time" for time-based rotation
        rotation_interval: Seconds between rotations (only for time-based mode)
        non_rotatable_errors: List of error substrings that should NOT trigger rotation
        header_builder: Function that takes an API key and returns headers dict
        logger_name: Optional name for the logger (defaults to agent class name)
    """

    def __init__(
        self,
        api_keys: List[str],
        rotation_mode: str = "error",
        rotation_interval: int = 300,
        non_rotatable_errors: Optional[List[str]] = None,
        header_builder: Optional[Callable[[str], Dict[str, str]]] = None,
        logger_name: Optional[str] = None,
    ):
        if not api_keys:
            raise ValueError("No valid API keys provided")

        self.api_keys = api_keys
        self.rotation_mode = rotation_mode
        self.rotation_interval = rotation_interval
        self.non_rotatable_errors = non_rotatable_errors or DEFAULT_NON_ROTATABLE_ERRORS
        self.header_builder = header_builder or self._default_header_builder

        self.current_key_index = random.randint(0, len(self.api_keys) - 1)
        self.current_api_key = self.api_keys[self.current_key_index]
        self.last_rotation_time = time.time()
        self.headers = self.header_builder(self.current_api_key)

        self._logger_name = logger_name or "APIKeyManager"
        logger.info(
            f"{self._logger_name} initialized with {len(self.api_keys)} API key(s), "
            f"mode={rotation_mode}, starting with index {self.current_key_index} "
            f"(key: {self.mask_key(self.current_api_key)})"
        )

    @staticmethod
    def from_env(
        env_var: str,
        rotation_mode: str = "error",
        rotation_interval: int = 300,
        non_rotatable_errors: Optional[List[str]] = None,
        header_builder: Optional[Callable[[str], Dict[str, str]]] = None,
        logger_name: Optional[str] = None,
    ) -> "APIKeyManager":
        """
        Create an APIKeyManager from an environment variable.

        Args:
            env_var: Name of environment variable containing comma-separated API keys
            rotation_mode: "error" or "time"
            rotation_interval: Seconds between rotations (time-based mode)
            non_rotatable_errors: Error substrings that should NOT trigger rotation
            header_builder: Function to build headers from API key
            logger_name: Optional logger name
        """
        import os

        api_keys_str = os.getenv(env_var)
        if not api_keys_str:
            raise ValueError(f"{env_var} environment variable is required")

        api_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]
        if not api_keys:
            raise ValueError(f"No valid API keys found in {env_var}")

        return APIKeyManager(
            api_keys=api_keys,
            rotation_mode=rotation_mode,
            rotation_interval=rotation_interval,
            non_rotatable_errors=non_rotatable_errors,
            header_builder=header_builder,
            logger_name=logger_name,
        )

    @staticmethod
    def _default_header_builder(api_key: str) -> Dict[str, str]:
        """Default header builder using Bearer token."""
        return {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    @staticmethod
    def mask_key(key: str) -> str:
        """Returns masked API key for safe logging."""
        if len(key) <= 8:
            return "****"
        return f"{key[:4]}...{key[-4:]}"

    def get_headers(self) -> Dict[str, str]:
        """Returns current headers, rotating if in time-based mode."""
        if self.rotation_mode == "time":
            self._rotate_if_time_elapsed()
        return self.headers

    def _rotate_if_time_elapsed(self) -> bool:
        """Rotate key if enough time has passed (time-based mode)."""
        current_time = time.time()
        if current_time - self.last_rotation_time >= self.rotation_interval:
            return self._rotate_key()
        return False

    def _rotate_key(self) -> bool:
        """Rotates to the next API key."""
        if len(self.api_keys) <= 1:
            logger.warning(f"{self._logger_name}: Only one API key available, cannot rotate")
            return False

        previous_index = self.current_key_index
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.current_api_key = self.api_keys[self.current_key_index]
        self.headers = self.header_builder(self.current_api_key)
        self.last_rotation_time = time.time()

        logger.info(
            f"{self._logger_name}: Rotated API key: index {previous_index} -> {self.current_key_index} "
            f"(key: {self.mask_key(self.current_api_key)})"
        )
        return True

    def should_rotate_on_error(self, error_msg: str) -> bool:
        """Determines if the error should trigger key rotation."""
        error_lower = error_msg.lower()
        return not any(code in error_lower for code in self.non_rotatable_errors)

    def rotate_on_error(self, error_msg: str) -> bool:
        """
        Attempts to rotate key based on error message.

        Returns:
            True if rotation occurred, False otherwise.
        """
        if not self.should_rotate_on_error(error_msg):
            logger.error(f"{self._logger_name}: Non-rotatable error: {error_msg}")
            return False

        logger.warning(f"{self._logger_name}: Rotatable error encountered: {error_msg}")
        return self._rotate_key()

    async def request_with_rotation(
        self,
        request_func: Callable,
        url: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        timeout: int = 30,
    ) -> Dict:
        """
        Makes an API request with automatic key rotation on errors.

        Args:
            request_func: Async function to make the actual request (e.g., self._api_request)
            url: API endpoint URL
            method: HTTP method
            params: URL query parameters
            json_data: JSON request body
            timeout: Request timeout in seconds

        Returns:
            API response dict or error dict
        """
        attempted_keys = set()
        last_error = None

        while len(attempted_keys) < len(self.api_keys):
            attempted_keys.add(self.current_key_index)
            logger.info(
                f"{self._logger_name}: API request with key index {self.current_key_index} "
                f"(key: {self.mask_key(self.current_api_key)})"
            )

            try:
                result = await request_func(
                    url=url,
                    method=method,
                    headers=self.headers,
                    params=params,
                    json_data=json_data,
                    timeout=timeout,
                )

                if "error" in result:
                    error_msg = str(result.get("error", ""))
                    if not self.should_rotate_on_error(error_msg):
                        logger.error(f"{self._logger_name}: Non-rotatable error: {result['error']}")
                        return result

                    logger.warning(f"{self._logger_name}: Rotatable error encountered: {result['error']}")
                    last_error = result

                    if self._rotate_key():
                        continue
                    return result

                return result

            except Exception as e:
                error_msg = str(e)
                if not self.should_rotate_on_error(error_msg):
                    logger.error(f"{self._logger_name}: Non-rotatable exception: {e}")
                    return {"error": error_msg}

                logger.warning(f"{self._logger_name}: Exception during request, rotating key: {e}")
                last_error = {"error": error_msg}

                if self._rotate_key():
                    continue
                return {"error": error_msg}

        logger.error(f"{self._logger_name}: All {len(self.api_keys)} API keys exhausted")
        return last_error or {"error": "All API keys exhausted"}
