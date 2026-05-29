"""
Nautilus Core: Action Log Entry Model
======================================

Production-grade implementation of the HELIX Chain action log entry schema.
Provides validation, logging, and secure parsing for cross-platform audit trails
between Nautilus and Heurist ecosystems.

Usage:
    entry = ActionLogEntry.from_dict(data)
    chain_hash = entry.compute_hash()

Requirements:
    - Python 3.10+
    - pydantic>=2.0
    - python-json-logger>=2.0.7
"""

import hashlib
import logging
import re
from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
_logger = logging.getLogger("nautilus.helix.action_log")
_logger.setLevel(logging.DEBUG)
if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03dZ [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)


# ---------------------------------------------------------------------------
# Enum definitions for type safety
# ---------------------------------------------------------------------------
class Platform(str, Enum):
    """Origin platform for the action log entry."""

    NAUTILUS = "nautilus"
    HEURIST = "heurist"


class ActionType(str, Enum):
    """Type of action performed by an agent."""

    TASK_ASSIGN = "taskAssign"
    TOOL_CALL = "toolCall"
    PAYMENT = "payment"


# ---------------------------------------------------------------------------
# Reusable type aliases
# ---------------------------------------------------------------------------

EthereumAddress = Annotated[
    str,
    Field(
        pattern=r"^0x[a-fA-F0-9]{40}$",
        description="Ethereum address (40 hex characters + 0x prefix) on Base Chain.",
    ),
]

TokenId = Annotated[
    str,
    Field(
        pattern=r"^\d+$",
        description="Numeric token ID representing a Heurist Mesh Agent.",
    ),
]


def _validate_hex_payload(value: str) -> str:
    """
    Validate that the payload is a 0x-prefixed hex string with even length and ≤1 MB.

    Args:
        value: The payload string to validate.

    Returns:
        The validated payload string.

    Raises:
        ValueError: If validation fails.
    """
    if not isinstance(value, str) or not re.match(r"^0x[a-fA-F0-9]+$", value):
        raise ValueError("Payload must be a hex string starting with '0x'.")
    if len(value) > 2_097_152:
        raise ValueError("Payload exceeds 2,097,152 hex characters (1 MB raw).")
    # Ensure even hex length (excluding "0x")
    if len(value) % 2 != 0:
        raise ValueError("Payload hex body must have an even number of characters.")
    if len(value) == 2:  # just "0x"
        raise ValueError("Payload must contain at least one byte (≥ 2 hex chars after '0x').")
    return value


HexPayload = Annotated[str, AfterValidator(_validate_hex_payload)]

# ---------------------------------------------------------------------------
# Conditional agent ID type
# ---------------------------------------------------------------------------

NautilusAgentId = EthereumAddress
HeuristAgentId = Union[EthereumAddress, TokenId]


# ---------------------------------------------------------------------------
# Main model
# ---------------------------------------------------------------------------

class ActionLogEntry(BaseModel):
    """
    Immutable audit trail entry for agent actions across Nautilus and Heurist.

    Validates structural correctness per the HELIX Chain schema.
    Cryptographic anchoring (SHA-256 hash verification) is performed off‑chain.

    Attributes:
        actionId: UUID v4 (lowercase, hyphenated).
        agentId: Agent identifier – format depends on platform.
        platform: Origin platform ('nautilus' or 'heurist').
        type: Action type (taskAssign, toolCall, payment).
        timestamp: ISO 8601 UTC timestamp with optional milliseconds (RFC 3339).
        payload: Opaque binary data as 0x‑prefixed hex (max 1 MB).
    """

    # ------------------------------------------------------------------
    # Fields
    # ------------------------------------------------------------------
    actionId: str = Field(
        pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        description="UUID v4 (lowercase, hyphenated).",
        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    )

    agentId: Union[EthereumAddress, TokenId] = Field(
        description="Agent identifier. For nautilus agents must be an Ethereum address; for heurist agents it can be an address or numeric token ID.",
    )

    platform: Platform = Field(
        description="Origin platform.",
    )

    type: ActionType = Field(
        description="Action type performed.",
    )

    timestamp: str = Field(
        description="ISO 8601 UTC timestamp with optional milliseconds, ending with 'Z'. Example: 2025-03-15T14:30:00.000Z",
        examples=["2025-03-15T14:30:00.000Z"],
    )

    payload: HexPayload = Field(
        description="Opaque hex-encoded binary data (0x prefix). Max 1 MB raw. Must have even hex length.",
        examples=["0xabcdef0123456789"],
    )

    # ------------------------------------------------------------------
    # Model configuration
    # ------------------------------------------------------------------
    model_config = ConfigDict(
        frozen=True,               # Immutable after creation
        extra="forbid",            # Reject unknown fields
        strict=True,               # Ensure correct types
        use_enum_values=True,      # Serialize enums as their string values
        validate_assignment=False, # Not needed as model is frozen
        json_schema_extra={
            "description": "Action log entry for HELIX Chain audit trail.",
        },
    )

    # ------------------------------------------------------------------
    # Field validators
    # ------------------------------------------------------------------

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        """
        Ensure timestamp follows ISO 8601 UTC with optional milliseconds.

        Pattern: YYYY-MM-DDTHH:MM:SS[.mmm]Z

        Args:
            v: The timestamp string.

        Returns:
            The validated timestamp string.

        Raises:
            ValueError: If the timestamp does not match the expected pattern.
        """
        pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$"
        if not re.match(pattern, v):
            raise ValueError(
                "Timestamp must match ISO 8601 UTC (RFC 3339) with optional milliseconds and 'Z'."
            )
        return v

    @field_validator("platform")
    @classmethod
    def check_platform(cls, v: Platform) -> Platform:
        """Ensure platform is valid (redundant with Enum, but provides clear error)."""
        if v not in Platform:
            raise ValueError(f"Unsupported platform: {v}. Must be one of {list(Platform)}.")
        return v

    @field_validator("type")
    @classmethod
    def check_action_type(cls, v: ActionType) -> ActionType:
        """Ensure action type is valid."""
        if v not in ActionType:
            raise ValueError(f"Unsupported action type: {v}. Must be one of {list(ActionType)}.")
        return v

    @model_validator(mode="after")
    def validate_agent_id_by_platform(self) -> "ActionLogEntry":
        """
        Enforce agentId format according to platform.

        - nautilus: must be an Ethereum address (0x...40 hex chars).
        - heurist: can be Ethereum address or numeric token ID.

        Returns:
            The unchanged instance if validation passes.

        Raises:
            ValueError: If the agentId does not match the required format for the given platform.
        """
        platform = self.platform
        agent_id = self.agentId

        if platform == Platform.NAUTILUS:
            if not re.match(r"^0x[a-fA-F0-9]{40}$", agent_id):
                raise ValueError(
                    f"For platform '{platform.value}', agentId must be an Ethereum address "
                    f"(0x...40 hex chars). Got '{agent_id}'."
                )
        elif platform == Platform.HEURIST:
            # The union type EthereumAddress | TokenId already validates,
            # but we can add an extra check for clarity.
            if not (re.match(r"^0x[a-fA-F0-9]{40}$", agent_id) or re.match(r"^\d+$", agent_id)):
                raise ValueError(
                    f"For platform '{platform.value}', agentId must be an Ethereum address "
                    f"or a numeric token ID. Got '{agent_id}'."
                )
        else:
            # Should never happen due to the Enum, but defensive.
            raise ValueError(f"Unsupported platform: {platform}")

        _logger.debug(
            "Validated agentId='%s' for platform='%s'",
            agent_id[:10] + "…" if len(agent_id) > 10 else agent_id,
            platform.value,
        )
        return self

    # ------------------------------------------------------------------
    # Production helpers
    # ------------------------------------------------------------------

    def compute_hash(self, algorithm: str = "sha256") -> str:
        """
        Compute the hex digest of the canonical JSON representation of this entry.

        Used for off‑chain integrity checks (HELIX Chain anchoring).

        Args:
            algorithm: Hash algorithm (default 'sha256').

        Returns:
            Hex digest string.

        Raises:
            ValueError: If an unsupported algorithm is provided.
        """
        if algorithm not in hashlib.algorithms_available:
            raise ValueError(f"Unsupported hash algorithm: '{algorithm}'.")
        canonical = self.model_dump_json(exclude_none=True, sort_keys=True)
        h = hashlib.new(algorithm)
        h.update(canonical.encode("utf-8"))
        return h.hexdigest()

    def log_creation(self) -> None:
        """Log creation of this entry at INFO level with minimal PII."""
        _logger.info(
            "ActionLogEntry created: actionId=%s platform=%s type=%s timestamp=%s hash_prefix=%s",
            self.actionId,
            self.platform.value if isinstance(self.platform, Enum) else self.platform,
            self.type.value if isinstance(self.type, Enum) else self.type,
            self.timestamp,
            self.compute_hash()[:12],
        )

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], strict: bool = True
    ) -> Optional["ActionLogEntry"]:
        """
        Create an ActionLogEntry from a dictionary, with full error context.

        Args:
            data: Dictionary with keys matching the schema (str keys).
            strict: If True (default), raise on validation errors;
                    if False, log error and return None.

        Returns:
            Validated ActionLogEntry instance, or None if not strict and validation fails.

        Raises:
            pydantic.ValidationError: If strict=True and validation fails.
            TypeError: If strict=True and input is not a dict.
        """
        if not isinstance(data, dict):
            if strict:
                raise TypeError("Input must be a dictionary.")
            _logger.error("from_dict: Input is not a dict: %s", type(data).__name__)
            return None

        try:
            obj = cls(**data)
            obj.log_creation()
            return obj
        except Exception as exc:
            _logger.error(
                "Failed to create ActionLogEntry from dict: %s | data=%s",
                exc,
                {k: v for k, v in data.items() if k != "payload"},  # avoid logging large binary
            )
            if strict:
                raise
            return None

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        """Return unambiguous representation with actionId."""
        return (
            f"ActionLogEntry(actionId='{self.actionId}', "
            f"platform='{self.platform}', "
            f"type='{self.type}')"
        )

    def __str__(self) -> str:
        """Return user-friendly representation."""
        return (
            f"Action {self.actionId[:8]}… @ {self.timestamp} "
            f"[{self.platform}/{self.type}]"
        )