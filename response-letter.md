"""
Formal response generator for Heurist-Nautilus collaboration.
Production-grade module with full validation, logging, metrics, and type safety.

Provides a robust framework for generating structured, validated formal
responses to external collaboration proposals. Designed with security,
maintainability, testability, and observability in mind.
"""

import logging
import re
import sys
import uuid
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from threading import Lock
from typing import Dict, List, Optional, Sequence, Final


# ---------------------------------------------------------------------------
# __all__ – explicit module exports
# ---------------------------------------------------------------------------
__all__ = [
    "HeuristResponseError",
    "ValidationError",
    "GenerationError",
    "Phase",
    "AlignmentArea",
    "PlatformContext",
    "ResponseContent",
    "HeuristResponseGenerator",
]


# ---------------------------------------------------------------------------
# Logging configuration (standard production setup with deduplication protection)
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setLevel(logging.INFO)
    _formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
    _handler.setFormatter(_formatter)
    logger.addHandler(_handler)


# ---------------------------------------------------------------------------
# Custom exceptions for domain-specific errors
# ---------------------------------------------------------------------------

class HeuristResponseError(Exception):
    """Base exception for all Heurist response generation errors."""


class ValidationError(HeuristResponseError):
    """Raised when input validation fails."""


class GenerationError(HeuristResponseError):
    """Raised when response generation fails unexpectedly."""


# ---------------------------------------------------------------------------
# Enums and type aliases
# ---------------------------------------------------------------------------

class Phase(Enum):
    """Phases of the proposed collaboration."""
    TECHNICAL_ASSESSMENT = auto()
    LIMITED_PILOT = auto()
    EXPANDED_INTEGRATION = auto()


class AlignmentArea(Enum):
    """Natural alignment areas between platforms."""
    MCP_INTEROPERABILITY = auto()
    ECONOMIC_CONVERGENCE = auto()
    SHARED_INFRASTRUCTURE = auto()
    AUDIT_REPUTATION = auto()


# ---------------------------------------------------------------------------
# Configuration – template strings, limits, and tweakable constants
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class GeneratorConfiguration:
    """
    Immutable configuration for the response generator.

    Attributes:
        max_recipient_name_length: Maximum character length for recipient name.
        max_title_length: Maximum character length for recipient title.
        allowed_name_regex: Regex pattern for allowed characters in names/titles.
        subject_template: Template for the email subject line.
        intro_template: Template for the opening paragraph.
        alignment_section_template: Template for each alignment area.
        next_steps_template: Template for the next steps section.
        closing_template: Template for final paragraph.
    """
    max_recipient_name_length: int = 200
    max_title_length: int = 100
    allowed_name_regex: Final[re.Pattern] = re.compile(r"^[a-zA-Z0-9 .,;:!?'\"\-()]+$")
    subject_template: str = "Re: Heurist – {recipient_platform} Partnership Proposal"
    intro_template: str = (
        "Dear {recipient_name},\n\n"
        "Thank you for reaching out to us regarding the {recipient_platform}. "
        "We have carefully reviewed your proposal and are enthusiastic about "
        "the potential synergies between Heurist and the Nautilus ecosystem."
    )
    alignment_section_template: str = (
        "\n\n## {area_name}\n{description}"
    )
    next_steps_template: str = (
        "\n\n## Next Steps\n"
        "1. Schedule a technical deep-dive within the next two weeks.\n"
        "2. Define shared success metrics for the limited pilot phase.\n"
        "3. Begin MCP compatibility testing on a staging environment.\n"
        "4. Draft a joint communication plan for community announcements."
    )
    closing_template: str = (
        "\n\nWe look forward to building the future of interoperable AI agents together.\n\n"
        "Best regards,\n{team_name}\n{email_address}"
    )


# ---------------------------------------------------------------------------
# Metrics collector (simple, thread-safe)
# ---------------------------------------------------------------------------

class _Metrics:
    """Internal thread-safe metrics counter."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._counts: Counter[str] = Counter()

    def increment(self, metric_name: str, value: int = 1) -> None:
        """Increment a metric by the given value (thread-safe)."""
        with self._lock:
            self._counts[metric_name] += value

    def get(self, metric_name: str) -> int:
        """Return current value of a metric (thread-safe)."""
        with self._lock:
            return self._counts.get(metric_name, 0)

    def snapshot(self) -> Dict[str, int]:
        """Return a snapshot of all current metrics (thread-safe)."""
        with self._lock:
            return dict(self._counts)


_metrics = _Metrics()


# ---------------------------------------------------------------------------
# Data structures with full validation on construction
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PlatformContext:
    """
    Immutable context about the responding platform.

    Attributes:
        team_name: Official team or company name.
        email_address: Contact email for the team.
        cc_list: Optional list of stakeholders to carbon-copy.
    """
    team_name: str
    email_address: str
    cc_list: Sequence[str] = field(default_factory=lambda: [
        "Heurist Core Maintainers",
        "Mesh Agent Partnership Group",
    ])

    def __post_init__(self) -> None:
        """Validate critical fields after initialization."""
        if not self.team_name or not isinstance(self.team_name, str) or not self.team_name.strip():
            raise ValidationError("PlatformContext.team_name must be a non-empty string")
        if not self.email_address or not isinstance(self.email_address, str) or not self.email_address.strip():
            raise ValidationError("PlatformContext.email_address must be a non-empty string")
        if "@" not in self.email_address or "." not in self.email_address:
            raise ValidationError(f"Invalid email format: {self.email_address}")
        # Validate CC list items
        if not isinstance(self.cc_list, (list, tuple)):
            raise ValidationError("PlatformContext.cc_list must be a list or tuple")
        for name in self.cc_list:
            if not name or not isinstance(name, str):
                raise ValidationError(f"Invalid entry in cc_list: {name}")


@dataclass
class ResponseContent:
    """
    Structured content of a formal reply.

    Attributes:
        recipient: Name of the recipient.
        subject: Subject line of the response.
        body: Full body text.
        sender: Platform context of the sender.
        sent_at: Timestamp of generation (UTC).
        message_id: Unique identifier for traceability.
    """
    recipient: str
    subject: str
    body: str
    sender: PlatformContext
    sent_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))


# ---------------------------------------------------------------------------
# Core generator class
# ---------------------------------------------------------------------------

class HeuristResponseGenerator:
    """
    Generates the formal Heurist response to Kairos (Nautilus platform).

    This class encapsulates all business logic for response construction,
    with comprehensive type safety, input validation, logging, and metrics.

    Example usage:
        config = GeneratorConfiguration()
        context = PlatformContext(team_name="Heurist", email_address="partnerships@heurist.ai")
        generator = HeuristResponseGenerator(config=config, default_sender=context)
        response = generator.generate_response(
            recipient_name="Kairos",
            recipient_platform="Nautilus",
            alignment_areas=[AlignmentArea.MCP_INTEROPERABILITY, AlignmentArea.ECONOMIC_CONVERGENCE]
        )
    """

    def __init__(self, config: Optional[GeneratorConfiguration] = None,
                 default_sender: Optional[PlatformContext] = None) -> None:
        """
        Initialize the generator with configuration and optional default sender.

        Args:
            config: Generator configuration (uses defaults if None).
            default_sender: Default platform context to use if none provided.

        Raises:
            ValidationError: If config or default_sender are invalid.
        """
        self._config = config or GeneratorConfiguration()
        if default_sender:
            if not isinstance(default_sender, PlatformContext):
                raise ValidationError("default_sender must be a PlatformContext instance")
        self._default_sender = default_sender
        _metrics.increment("generator_initialized")

    def generate_response(
        self,
        recipient_name: str,
        recipient_platform: str,
        alignment_areas: Optional[Sequence[AlignmentArea]] = None,
        sender: Optional[PlatformContext] = None,
    ) -> ResponseContent:
        """
        Generate a full formal response.

        Args:
            recipient_name: Name of the recipient (e.g., "Kairos").
            recipient_platform: Platform name (e.g., "Nautilus").
            alignment_areas: List of alignment areas to highlight.
            sender: Sender's platform context (uses default if None).

        Returns:
            ResponseContent with recipient, subject, body, sender, timestamp, message_id.

        Raises:
            ValidationError: If any input validation fails.
            GenerationError: If generation fails unexpectedly.
        """
        _metrics.increment("generate_response_calls")
        logger.info("Starting response generation for %s from %s", recipient_name, recipient_platform)

        # Validate inputs
        self._validate_recipient(recipient_name)
        self._validate_recipient_platform(recipient_platform)
        if alignment_areas is None:
            alignment_areas = list(AlignmentArea)
        self._validate_alignment_areas(alignment_areas)

        effective_sender = sender or self._default_sender
        if not effective_sender:
            raise ValidationError("No sender provided and no default sender configured")

        logger.debug("Sender team: %s, email: %s", effective_sender.team_name, effective_sender.email_address)

        try:
            subject = self._build_subject(recipient_platform)
            logger.debug("Subject built: %s", subject)

            intro = self._build_intro(recipient_name, recipient_platform)
            logger.debug("Intro built")

            alignment_sections = self._build_alignment_sections(alignment_areas)
            logger.debug("Built %d alignment sections", len(alignment_sections))

            next_steps = self._config.next_steps_template
            closing = self._build_closing(effective_sender)
            logger.debug("Closing built")

            body = intro + alignment_sections + next_steps + closing
        except Exception as exc:
            _metrics.increment("generation_error")
            logger.error("Failed to build response: %s", exc, exc_info=True)
            raise GenerationError(f"Failed to generate response: {exc}") from exc

        content = ResponseContent(
            recipient=recipient_name,
            subject=subject,
            body=body,
            sender=effective_sender,
        )
        logger.info("Response generated successfully (message_id: %s)", content.message_id)
        _metrics.increment("response_generated")
        return content

    # ------------------------------------------------------------------
    # Input validation helpers
    # ------------------------------------------------------------------

    def _validate_recipient(self, name: str) -> None:
        """Validate recipient name against configuration rules.

        Args:
            name: Recipient name string.

        Raises:
            ValidationError: If name fails validation.
        """
        if not name or not isinstance(name, str):
            raise ValidationError("recipient_name must be a non-empty string")
        if len(name) > self._config.max_recipient_name_length:
            raise ValidationError(
                f"recipient_name exceeds max length {self._config.max_recipient_name_length}"
            )
        if not self._config.allowed_name_regex.fullmatch(name):
            raise ValidationError(
                f"recipient_name contains disallowed characters: '{name}'"
            )
        logger.debug("Recipient name validated: %s", name[:50])

    def _validate_recipient_platform(self, platform: str) -> None:
        """Validate recipient platform name.

        Args:
            platform: Platform name string.

        Raises:
            ValidationError: If platform fails validation.
        """
        if not platform or not isinstance(platform, str):
            raise ValidationError("recipient_platform must be a non-empty string")
        # Allow only alphanumeric, spaces, hyphens, underscores
        if not re.fullmatch(r"^[a-zA-Z0-9 _\-]+$", platform):
            raise ValidationError(f"recipient_platform contains invalid characters: '{platform}'")
        logger.debug("Recipient platform validated: %s", platform)

    def _validate_alignment_areas(self, areas: Sequence[AlignmentArea]) -> None:
        """Validate alignment areas list.

        Args:
            areas: Sequence of AlignmentArea values.

        Raises:
            ValidationError: If areas is empty or contains invalid items.
        """
        if not areas:
            raise ValidationError("alignment_areas cannot be empty")
        for area in areas:
            if not isinstance(area, AlignmentArea):
                raise ValidationError(f"Invalid alignment area: {area}")
        logger.debug("Alignment areas validated: %d items", len(areas))

    # ------------------------------------------------------------------
    # Body construction helpers
    # ------------------------------------------------------------------

    def _build_subject(self, platform: str) -> str:
        """Build the email subject line.

        Args:
            platform: The recipient's platform name.

        Returns:
            Formatted subject string.
        """
        return self._config.subject_template.format(recipient_platform=platform)

    def _build_intro(self, recipient_name: str, recipient_platform: str) -> str:
        """Build the introductory paragraph.

        Args:
            recipient_name: Name of the recipient.
            recipient_platform: Name of the recipient's platform.

        Returns:
            Formatted intro string.
        """
        return self._config.intro_template.format(
            recipient_name=recipient_name,
            recipient_platform=recipient_platform
        )

    def _build_alignment_sections(self, areas: Sequence[AlignmentArea]) -> str:
        """Build the alignment area sections from templates.

        Args:
            areas: Sequence of AlignmentArea to include.

        Returns:
            Concatenated string of all alignment sections.
        """
        sections: List[str] = []
        for area in areas:
            name = area.name.replace("_", " ").title()
            # Rich description for each alignment area
            description = self._get_alignment_description(area)
            section = self._config.alignment_section_template.format(
                area_name=name,
                description=description
            )
            sections.append(section)
        return "".join(sections)

    def _get_alignment_description(self, area: AlignmentArea) -> str:
        """Return a detailed description for a given alignment area.

        Args:
            area: AlignmentArea enum value.

        Returns:
            String description.
        """
        descriptions = {
            AlignmentArea.MCP_INTEROPERABILITY: (
                "Both platforms support the Model Context Protocol (MCP). "
                "Heurist Mesh agents and Nautilus agents can exchange tools, "
                "data sources, and services through a shared MCP registry, "
                "enabling cross-platform task execution."
            ),
            AlignmentArea.ECONOMIC_CONVERGENCE: (
                "Heurist's X402 pay-per-request model integrates with Nautilus "
                "NAU tokens via a smart contract bridge on Base Chain. "
                "Agents can earn and spend value on either platform, "
                "creating a unified agent economy."
            ),
            AlignmentArea.SHARED_INFRASTRUCTURE: (
                "Both ecosystems operate on the Base Chain. "
                "Common identity standards (ERC-8004, Nautilus DID) "
                "and liquidity pools for USDC/NAU reduce friction "
                "for cross-platform deployments."
            ),
            AlignmentArea.AUDIT_REPUTATION: (
                "Nautilus HELIX Chain provides an immutable audit trail. "
                "Heurist agents can publish actions to both HELIX and "
                "their own Mesh audit logs, building transparent reputation "
                "that spans both ecosystems."
            ),
        }
        return descriptions.get(area, "Alignment area to be explored jointly.")

    def _build_closing(self, sender: PlatformContext) -> str:
        """Build the closing paragraph including signature.

        Args:
            sender: PlatformContext with team_name and email_address.

        Returns:
            Formatted closing string.
        """
        return self._config.closing_template.format(
            team_name=sender.team_name,
            email_address=sender.email_address
        )


# ---------------------------------------------------------------------------
# Module-level convenience function
# ---------------------------------------------------------------------------

def quick_response(
    recipient_name: str,
    recipient_platform: str = "Nautilus",
    team_name: str = "Heurist Core Team",
    email_address: str = "partnerships@heurist.ai",
    alignment_areas: Optional[Sequence[AlignmentArea]] = None,
) -> ResponseContent:
    """
    Quick one-liner to generate a response with minimal setup.

    Args:
        recipient_name: Name of the recipient.
        recipient_platform: Platform name (default "Nautilus").
        team_name: Sender team name.
        email_address: Sender email address.
        alignment_areas: Optional list of alignment areas.

    Returns:
        Generated ResponseContent.

    Example:
        >>> response = quick_response("Kairos")
    """
    sender = PlatformContext(team_name=team_name, email_address=email_address)
    config = GeneratorConfiguration()
    generator = HeuristResponseGenerator(config=config, default_sender=sender)
    return generator.generate_response(
        recipient_name=recipient_name,
        recipient_platform=recipient_platform,
        alignment_areas=alignment_areas,
    )