"""
Research Notes: Nautilus Platform & Heurist Agent Framework Interoperability

This module provides a production‑quality data model and utility functions for
capturing, validating, and querying interoperability research between the
Nautilus Platform and the Heurist Agent Framework. It includes full type
annotations, comprehensive logging, input validation, and error handling.

The module is designed to be thread‑safe (all data classes are immutable) and
minimises external dependencies. Structured logging is used throughout to
enable traceability in production environments.
"""

import json
import logging
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

# Configure module‑level logger
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # Let the application configure handlers


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------
class ResearchNotesError(Exception):
    """Base exception for research notes module."""


class ValidationError(ResearchNotesError):
    """Raised when input data fails validation."""


class DataIntegrityError(ResearchNotesError):
    """Raised when internal data consistency is violated."""


class SerializationError(ResearchNotesError):
    """Raised when serialization or deserialization fails."""


class ConfigurationError(ResearchNotesError):
    """Raised when module configuration is invalid."""


# ---------------------------------------------------------------------------
# Enumerations for structured representation
# ---------------------------------------------------------------------------
class Platform(str, Enum):
    """Supported platforms for research facts."""

    NAUTILUS = "Nautilus"
    HEURIST = "Heurist"


class Priority(int, Enum):
    """Priority levels for open questions and integration points."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


# ---------------------------------------------------------------------------
# Data classes with built‑in validation
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Fact:
    """A single verifiable fact about a platform.

    Attributes:
        area: The category (e.g., 'Identity', 'Token Economy').
        details: Specific factual statement.
        platform: Which platform this fact belongs to.
        source: Optional reference to a trusted document or endpoint.

    Raises:
        ValidationError: If area or details are empty, or platform is invalid.
    """

    area: str
    details: str
    platform: Platform
    source: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate that area and details are non‑empty strings."""
        if not self.area or not self.area.strip():
            raise ValidationError("Fact 'area' must be a non‑empty string.")
        if not self.details or not self.details.strip():
            raise ValidationError("Fact 'details' must be a non‑empty string.")
        if not isinstance(self.platform, Platform):
            raise ValidationError("Fact 'platform' must be a Platform enum value.")
        if self.source is not None and not isinstance(self.source, str):
            raise ValidationError("Fact 'source' must be a string or None.")
        logger.debug(f"Validated Fact: area='{self.area}', platform={self.platform}")


@dataclass(frozen=True)
class Assumption:
    """An assumption made during research, tagged with confidence.

    Attributes:
        description: The assumption statement.
        confidence: A float in [0.0, 1.0] representing likelihood.

    Raises:
        ValidationError: If description is empty or confidence out of range.
    """

    description: str
    confidence: float = 0.5

    def __post_init__(self) -> None:
        if not self.description or not self.description.strip():
            raise ValidationError("Assumption 'description' must be non‑empty.")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValidationError(
                f"Assumption confidence must be between 0.0 and 1.0, got {self.confidence}"
            )
        logger.debug(f"Validated Assumption: confidence={self.confidence}")


@dataclass(frozen=True)
class OpenQuestion:
    """An unresolved question requiring further investigation.

    Attributes:
        question: The question text.
        category: The broad area (e.g., 'Identity & Trust').
        priority: How urgently this question should be addressed.

    Raises:
        ValidationError: If question or category are empty.
    """

    question: str
    category: str
    priority: Priority = Priority.MEDIUM

    def __post_init__(self) -> None:
        if not self.question or not self.question.strip():
            raise ValidationError("OpenQuestion 'question' must be non‑empty.")
        if not self.category or not self.category.strip():
            raise ValidationError("OpenQuestion 'category' must be non‑empty.")
        if not isinstance(self.priority, Priority):
            raise ValidationError("OpenQuestion 'priority' must be a Priority enum value.")
        logger.debug(f"Validated OpenQuestion: priority={self.priority}")


@dataclass(frozen=True)
class IntegrationPoint:
    """A concrete integration opportunity between the two platforms.

    Attributes:
        name: Short descriptor.
        description: Detailed explanation.
        priority: Strategic importance level.

    Raises:
        ValidationError: If name or description are empty.
    """

    name: str
    description: str
    priority: Priority = Priority.MEDIUM

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("IntegrationPoint 'name' must be non‑empty.")
        if not self.description or not self.description.strip():
            raise ValidationError("IntegrationPoint 'description' must be non‑empty.")
        if not isinstance(self.priority, Priority):
            raise ValidationError("IntegrationPoint 'priority' must be a Priority enum value.")
        logger.debug(f"Validated IntegrationPoint: name='{self.name}'")


# ---------------------------------------------------------------------------
# JSON encoder for enum serialization
# ---------------------------------------------------------------------------
class ResearchNotesEncoder(json.JSONEncoder):
    """Custom JSON encoder that serializes enum members to their values."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)


# ---------------------------------------------------------------------------
# Main research container (immutable after construction)
# ---------------------------------------------------------------------------
class ResearchNotes:
    """Container for all structured research data regarding Nautilus‑Heurist
    interoperability. Provides validation on construction, serialization, and
    query methods.

    Typical usage::

        notes = ResearchNotes(
            nautilus_facts=[...],
            heurist_facts=[...],
            assumptions=[...],
            open_questions=[...],
            integration_points=[...]
        )
        notes.validate()   # raises if any inconsistency
        json_output = notes.to_json()
        restored = ResearchNotes.from_json(json_output)

    The object is effectively immutable after creation. All collections are
    stored as tuples to guarantee immutability.

    Args:
        nautilus_facts: Sequence of Fact objects about Nautilus.
        heurist_facts: Sequence of Fact objects about Heurist.
        assumptions: Sequence of Assumption objects.
        open_questions: Sequence of OpenQuestion objects.
        integration_points: Sequence of IntegrationPoint objects.

    Raises:
        ValidationError: If any item fails validation or platform facts are inconsistent.
    """

    def __init__(
        self,
        nautilus_facts: Sequence[Fact] = (),
        heurist_facts: Sequence[Fact] = (),
        assumptions: Sequence[Assumption] = (),
        open_questions: Sequence[OpenQuestion] = (),
        integration_points: Sequence[IntegrationPoint] = (),
    ) -> None:
        # Convert inputs to tuples for immutability
        self._nautilus_facts: Tuple[Fact, ...] = tuple(nautilus_facts)
        self._heurist_facts: Tuple[Fact, ...] = tuple(heurist_facts)
        self._assumptions: Tuple[Assumption, ...] = tuple(assumptions)
        self._open_questions: Tuple[OpenQuestion, ...] = tuple(open_questions)
        self._integration_points: Tuple[IntegrationPoint, ...] = tuple(integration_points)

        # Validate all items
        self._validate_items()
        logger.info("ResearchNotes created successfully.")

    # -----------------------------------------------------------------------
    # Public properties (read‑only)
    # -----------------------------------------------------------------------
    @property
    def nautilus_facts(self) -> Tuple[Fact, ...]:
        """Facts specific to the Nautilus platform."""
        return self._nautilus_facts

    @property
    def heurist_facts(self) -> Tuple[Fact, ...]:
        """Facts specific to the Heurist platform."""
        return self._heurist_facts

    @property
    def assumptions(self) -> Tuple[Assumption, ...]:
        """Assumptions made during research."""
        return self._assumptions

    @property
    def open_questions(self) -> Tuple[OpenQuestion, ...]:
        """Open questions requiring further investigation."""
        return self._open_questions

    @property
    def integration_points(self) -> Tuple[IntegrationPoint, ...]:
        """Concrete integration opportunities."""
        return self._integration_points

    # -----------------------------------------------------------------------
    # Internal validation helpers
    # -----------------------------------------------------------------------
    def _validate_items(self) -> None:
        """Validate all items and ensure platform consistency.

        Raises:
            ValidationError: If any item is invalid or platform assignment is wrong.
        """
        logger.debug("Validating all items inside ResearchNotes.")

        for fact in self._nautilus_facts:
            if not isinstance(fact, Fact):
                raise ValidationError("nautilus_facts must contain only Fact instances.")
            if fact.platform != Platform.NAUTILUS:
                raise ValidationError(
                    f"Nautilus fact '{fact.details}' has wrong platform: {fact.platform}"
                )
        for fact in self._heurist_facts:
            if not isinstance(fact, Fact):
                raise ValidationError("heurist_facts must contain only Fact instances.")
            if fact.platform != Platform.HEURIST:
                raise ValidationError(
                    f"Heurist fact '{fact.details}' has wrong platform: {fact.platform}"
                )
        for assumption in self._assumptions:
            if not isinstance(assumption, Assumption):
                raise ValidationError("assumptions must contain only Assumption instances.")
        for question in self._open_questions:
            if not isinstance(question, OpenQuestion):
                raise ValidationError("open_questions must contain only OpenQuestion instances.")
        for point in self._integration_points:
            if not isinstance(point, IntegrationPoint):
                raise ValidationError("integration_points must contain only IntegrationPoint instances.")

        logger.debug("All items validated successfully.")

    # -----------------------------------------------------------------------
    # Public validation method
    # -----------------------------------------------------------------------
    def validate(self) -> bool:
        """Perform comprehensive consistency checks.

        Currently checks:
            - No duplicate facts (same area + details across both fact lists)
            - All items are valid (already done in __init__)

        Returns:
            True if all checks pass.

        Raises:
            DataIntegrityError: If duplicates or other inconsistencies are found.
            ValidationError: If any item is invalid (shouldn't happen after __init__).
        """
        self._validate_items()  # re‑validate to catch any mutation (though immutable)

        # Check for duplicate facts across both lists
        all_facts = self._nautilus_facts + self._heurist_facts
        seen: set[Tuple[str, str, Platform]] = set()
        for fact in all_facts:
            key = (fact.area, fact.details, fact.platform)
            if key in seen:
                raise DataIntegrityError(
                    f"Duplicate fact found: area='{fact.area}', details='{fact.details}', platform={fact.platform}"
                )
            seen.add(key)

        logger.info("ResearchNotes validated successfully.")
        return True

    # -----------------------------------------------------------------------
    # Serialization
    # -----------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Convert the research notes to a dictionary (suitable for JSON).

        Returns:
            dict with keys matching the five collections, each a list of dicts.
        """
        return {
            "nautilus_facts": [asdict(f) for f in self._nautilus_facts],
            "heurist_facts": [asdict(f) for f in self._heurist_facts],
            "assumptions": [asdict(a) for a in self._assumptions],
            "open_questions": [asdict(q) for q in self._open_questions],
            "integration_points": [asdict(p) for p in self._integration_points],
        }

    def to_json(self, indent: int = 2, sort_keys: bool = True) -> str:
        """Serialize the research notes to a JSON string.

        Args:
            indent: Number of spaces for indentation (default 2).
            sort_keys: Whether to sort dictionary keys (default True).

        Returns:
            JSON string representation.

        Raises:
            SerializationError: If JSON encoding fails.
        """
        try:
            return json.dumps(self.to_dict(), indent=indent, sort_keys=sort_keys, cls=ResearchNotesEncoder)
        except (TypeError, ValueError) as exc:
            raise SerializationError(f"Failed to serialize ResearchNotes to JSON: {exc}") from exc

    def to_file(self, path: Union[str, Path], indent: int = 2, sort_keys: bool = True) -> None:
        """Write the research notes as JSON to a file.

        Args:
            path: Filesystem path to write to.
            indent: JSON indentation (default 2).
            sort_keys: Whether to sort dictionary keys (default True).

        Raises:
            SerializationError: If writing fails.
            PermissionError: If file cannot be written.
        """
        path_obj = Path(path)
        try:
            content = self.to_json(indent=indent, sort_keys=sort_keys)
            path_obj.write_text(content, encoding="utf-8")
            logger.info(f"ResearchNotes written to {path_obj.resolve()}")
        except (OSError, json.JSONDecodeError) as exc:
            raise SerializationError(f"Failed to write ResearchNotes to file '{path}': {exc}") from exc

    # -----------------------------------------------------------------------
    # Deserialization
    # -----------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ResearchNotes":
        """Create a ResearchNotes instance from a dictionary.

        The dictionary should have keys matching the collection names, each
        containing a list of dicts with the appropriate fields.

        Args:
            data: Dictionary representation produced by to_dict().

        Returns:
            New ResearchNotes instance.

        Raises:
            ValidationError: If the dictionary structure is invalid.
            SerializationError: If reconstruction fails.
        """
        try:
            nautilus_facts = [
                Fact(
                    area=item.get("area", ""),
                    details=item.get("details", ""),
                    platform=Platform(item.get("platform", "")),
                    source=item.get("source"),
                )
                for item in data.get("nautilus_facts", [])
            ]
            heurist_facts = [
                Fact(
                    area=item.get("area", ""),
                    details=item.get("details", ""),
                    platform=Platform(item.get("platform", "")),
                    source=item.get("source"),
                )
                for item in data.get("heurist_facts", [])
            ]
            assumptions = [
                Assumption(
                    description=item.get("description", ""),
                    confidence=item.get("confidence", 0.5),
                )
                for item in data.get("assumptions", [])
            ]
            open_questions = [
                OpenQuestion(
                    question=item.get("question", ""),
                    category=item.get("category", ""),
                    priority=Priority(item.get("priority", Priority.MEDIUM)),
                )
                for item in data.get("open_questions", [])
            ]
            integration_points = [
                IntegrationPoint(
                    name=item.get("name", ""),
                    description=item.get("description", ""),
                    priority=Priority(item.get("priority", Priority.MEDIUM)),
                )
                for item in data.get("integration_points", [])
            ]
            return cls(
                nautilus_facts=nautilus_facts,
                heurist_facts=heurist_facts,
                assumptions=assumptions,
                open_questions=open_questions,
                integration_points=integration_points,
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise SerializationError(f"Failed to reconstruct ResearchNotes from dict: {exc}") from exc

    @classmethod
    def from_json(cls, json_str: str) -> "ResearchNotes":
        """Create a ResearchNotes instance from a JSON string.

        Args:
            json_str: Valid JSON string produced by to_json().

        Returns:
            New ResearchNotes instance.

        Raises:
            SerializationError: If JSON parsing fails.
            ValidationError: If reconstructed data fails validation.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as exc:
            raise SerializationError(f"Invalid JSON input: {exc}") from exc
        if not isinstance(data, dict):
            raise SerializationError("JSON input must be a dictionary.")
        return cls.from_dict(data)

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "ResearchNotes":
        """Load research notes from a JSON file.

        Args:
            path: Filesystem path to a JSON file produced by to_file().

        Returns:
            New ResearchNotes instance.

        Raises:
            SerializationError: If file cannot be read or parsed.
        """
        path_obj = Path(path)
        try:
            content = path_obj.read_text(encoding="utf-8")
            logger.info(f"ResearchNotes loaded from {path_obj.resolve()}")
            return cls.from_json(content)
        except (OSError, json.JSONDecodeError) as exc:
            raise SerializationError(f"Failed to load ResearchNotes from file '{path}': {exc}") from exc

    # -----------------------------------------------------------------------
    # Query convenience methods
    # -----------------------------------------------------------------------
    def query_facts_by_area(self, area: str) -> Tuple[Fact, ...]:
        """Return all facts (from both platforms) matching the given area.

        Args:
            area: Case‑sensitive area string.

        Returns:
            Tuple of matching Fact objects.
        """
        all_facts = self._nautilus_facts + self._heurist_facts
        return tuple(f for f in all_facts if f.area == area)

    def get_open_questions_by_priority(self, priority: Priority) -> Tuple[OpenQuestion, ...]:
        """Return open questions with the specified priority.

        Args:
            priority: Priority level to filter by.

        Returns:
            Tuple of matching OpenQuestion objects.
        """
        return tuple(q for q in self._open_questions if q.priority == priority)

    def get_integration_points_by_priority(self, priority: Priority) -> Tuple[IntegrationPoint, ...]:
        """Return integration points with the specified priority.

        Args:
            priority: Priority level to filter by.

        Returns:
            Tuple of matching IntegrationPoint objects.
        """
        return tuple(p for p in self._integration_points if p.priority == priority)

    # -----------------------------------------------------------------------
    # Representation
    # -----------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"ResearchNotes(nautilus_facts={len(self._nautilus_facts)}, "
            f"heurist_facts={len(self._heurist_facts)}, "
            f"assumptions={len(self._assumptions)}, "
            f"open_questions={len(self._open_questions)}, "
            f"integration_points={len(self._integration_points)})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResearchNotes):
            return NotImplemented
        return (
            self._nautilus_facts == other._nautilus_facts
            and self._heurist_facts == other._heurist_facts
            and self._assumptions == other._assumptions
            and self._open_questions == other._open_questions
            and self._integration_points == other._integration_points
        )

    def __hash__(self) -> int:
        return hash(
            (
                self._nautilus_facts,
                self._heurist_facts,
                self._assumptions,
                self._open_questions,
                self._integration_points,
            )
        )


# ---------------------------------------------------------------------------
# Module‑level convenience function
# ---------------------------------------------------------------------------
def load_research_notes(path: Union[str, Path]) -> ResearchNotes:
    """Load a ResearchNotes instance from a JSON file.

    This is a simple alias for ``ResearchNotes.from_file()`` for common use.

    Args:
        path: Path to a JSON research notes file.

    Returns:
        ResearchNotes instance.
    """
    return ResearchNotes.from_file(path)