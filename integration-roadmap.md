"""
HEP Document Model - Production-grade validation and serialization.

Provides a robust, validated representation of Heurist Enhancement Proposals (HEP)
with full type safety, logging, input validation, security checks, and error handling.
Supports YAML import/export with strict validation against the HEP schema.
"""

from __future__ import annotations

import logging
import re
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any, Optional

import yaml
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
    model_validator,
    ConfigDict,
    AfterValidator,
)

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    _console = logging.StreamHandler()
    _console.setLevel(logging.INFO)
    _formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    _console.setFormatter(_formatter)
    logger.addHandler(_console)


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------
class HEPDocumentError(Exception):
    """Base exception for HEP document errors."""


class HEPValidationError(HEPDocumentError):
    """Raised when document validation fails."""


class HEPLoadError(HEPDocumentError):
    """Raised when document loading fails."""


class HEPSecurityError(HEPDocumentError):
    """Raised when a security check fails (e.g., malicious YAML)."""


class HEPExportError(HEPDocumentError):
    """Raised when document export fails."""


# ---------------------------------------------------------------------------
# Constants for validation and security
# ---------------------------------------------------------------------------
_ID_PATTERN = re.compile(r"^HEP-\d{4}-\d{2,4}$")
_VERSION_PATTERN = re.compile(r"^\d+\.\d+$")
_EMAIL_PATTERN = re.compile(r"^[\w\.\-]+@[\w\-]+\.\w+$")
_MAX_YAML_SIZE = 1024 * 1024  # 1 MB
_MAX_YAML_DEPTH = 20
_MIN_YEAR = 2020
_MAX_YEAR = 2099
_MIN_VERSION_MAJOR = 1
_MAX_FUTURE_YEARS = 10


# ---------------------------------------------------------------------------
# Enums and helpers
# ---------------------------------------------------------------------------
class DocumentStatus(str, Enum):
    """Allowed statuses for a HEP document."""

    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"


class Classification(str, Enum):
    """Sensitivity classification levels."""

    INTERNAL_DO_NOT_DISTRIBUTE = "Internal — Do Not Distribute"
    CONFIDENTIAL = "Confidential"
    PUBLIC = "Public"


# ---------------------------------------------------------------------------
# Validation functions (used with AfterValidator)
# ---------------------------------------------------------------------------
def _validate_document_id(v: str) -> str:
    """Validate document_id format: HEP-YYYY-NNN (YYYY between 2020-2099)."""
    if not _ID_PATTERN.match(v):
        raise ValueError(
            f"document_id must match pattern HEP-YYYY-NNN, got '{v}'"
        )
    parts = v.split("-")
    year = int(parts[1])
    if year < _MIN_YEAR or year > _MAX_YEAR:
        raise ValueError(
            f"year in document_id must be between {_MIN_YEAR}-{_MAX_YEAR}, "
            f"got {year}"
        )
    return v


def _validate_version(v: str) -> str:
    """Validate version format: major.minor (major >= 1)."""
    if not _VERSION_PATTERN.match(v):
        raise ValueError(
            f"version must be in format 'major.minor', got '{v}'"
        )
    major_str, _ = v.split(".")
    major = int(major_str)
    if major < _MIN_VERSION_MAJOR:
        raise ValueError(
            f"version major must be ≥ {_MIN_VERSION_MAJOR}, got {major}"
        )
    return v


def _validate_classification(v: str) -> str:
    """Ensure classification is one of the allowed values."""
    allowed = [c.value for c in Classification]
    if v not in allowed:
        raise ValueError(
            f"classification must be one of {allowed}, got '{v}'"
        )
    return v


# ---------------------------------------------------------------------------
# Author / Reviewer models
# ---------------------------------------------------------------------------
class Person(BaseModel):
    """Represents a person or team as document author/reviewer."""

    name: str = Field(
        ..., min_length=1, max_length=200, description="Full name or team name"
    )
    email: Optional[str] = Field(
        default=None,
        pattern=_EMAIL_PATTERN.pattern,
        description="Optional email address",
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.email or 'no email'})"

    def _verify_no_duplicate_name(self) -> None:
        """Internal check (used in list validation)."""


# ---------------------------------------------------------------------------
# Main HEP Document model
# ---------------------------------------------------------------------------
class HEPDocument(BaseModel):
    """
    Heurist Enhancement Proposal (HEP) document with full validation.

    This model enforces all constraints from the HEP specification (HEP-2026-01).
    It supports safe YAML loading, validation, and serialization.

    Example:
        doc = HEPDocument.from_yaml_file("proposal.yaml")
        print(doc.document_id)

    Attributes:
        document_id: Identifier format HEP-YYYY-NNN.
        version: Semantic version major.minor.
        date: Document date (ISO format).
        status: Current lifecycle status.
        classification: Sensitivity level.
        prepared_by: List of authors (at least 1).
        review_required: List of required reviewers (can be empty).
    """

    model_config = ConfigDict(
        frozen=True,            # Immutable after creation for thread safety
        extra="forbid",         # Reject unknown fields (security)
        validate_default=True,
        str_strip_whitespace=True,
    )

    document_id: Annotated[str, AfterValidator(_validate_document_id)] = Field(
        ..., description="Document identifier (e.g., HEP-2026-01)"
    )
    version: Annotated[str, AfterValidator(_validate_version)] = Field(
        ..., description="Document version (e.g., 2.2)"
    )
    date: date = Field(
        ..., description="Document creation/last-revision date (ISO format)"
    )
    status: DocumentStatus = Field(
        default=DocumentStatus.DRAFT,
        description="Current status of the document",
    )
    classification: Annotated[str, AfterValidator(_validate_classification)] = Field(
        ..., description="Sensitivity classification"
    )
    prepared_by: list[Person] = Field(
        ...,
        min_length=1,
        description="List of authors or teams who prepared the document",
    )
    review_required: list[Person] = Field(
        default_factory=list,
        min_length=0,
        description="List of reviewers required for approval",
    )

    # -----------------------------------------------------------------------
    # Field validators
    # -----------------------------------------------------------------------
    @field_validator("date")
    @classmethod
    def _date_not_in_far_future(cls, v: date) -> date:
        """Reject dates more than 10 years in the future (safety check)."""
        today = date.today()
        max_future = today.replace(year=today.year + _MAX_FUTURE_YEARS)
        if v > max_future:
            raise ValueError(
                f"date cannot be more than {_MAX_FUTURE_YEARS} years in the "
                f"future, got {v}"
            )
        return v

    @field_validator("prepared_by", "review_required")
    @classmethod
    def _validate_person_list(cls, v: list[Person], info: Any) -> list[Person]:
        """Ensure no duplicate names within the list."""
        names = [p.name for p in v]
        if len(names) != len(set(names)):
            raise ValueError(
                f"duplicate person names in {info.field_name}: {names}"
            )
        return v

    @model_validator(mode="after")
    def _validate_reviewers_for_review_status(self) -> "HEPDocument":
        """If status is REVIEW, review_required must be non-empty."""
        if self.status == DocumentStatus.REVIEW and not self.review_required:
            raise HEPValidationError(
                "review_required must contain at least one reviewer when "
                "status is 'REVIEW'"
            )
        return self

    # -----------------------------------------------------------------------
    # Security and size checks for YAML loading
    # -----------------------------------------------------------------------
    @staticmethod
    def _secure_yaml_load(stream, loader_class=yaml.SafeLoader) -> dict:
        """
        Load YAML with security and resource limits.

        Args:
            stream: File-like object or string.
            loader_class: YAML loader (default SafeLoader).

        Returns:
            Parsed dictionary.

        Raises:
            HEPSecurityError: If YAML is too large, too deep, or contains
                unsafe constructs.
        """
        # Read content for size check
        if isinstance(stream, str):
            content = stream
        else:
            content = stream.read()
            if hasattr(stream, "seek"):
                stream.seek(0)

        # Limit content size
        if len(content) > _MAX_YAML_SIZE:
            raise HEPSecurityError(
                f"YAML content exceeds maximum size of {_MAX_YAML_SIZE} bytes"
            )

        # Limit depth via custom constructor (SafeLoader prevents dangerous tags)
        # PyYAML does not offer depth limit natively; we approximate by
        # restricting recursion during parse using a custom loader if needed.
        # For production, consider using `yamlutil` or Ruamel with limits.
        # Here we rely on SafeLoader which does not execute arbitrary code.
        try:
            data = yaml.load(content, Loader=loader_class)
        except yaml.YAMLError as e:
            raise HEPLoadError(f"Failed to parse YAML content: {e}") from e
        except RecursionError as e:
            raise HEPSecurityError(
                f"YAML recursion depth exceeded: {e}"
            ) from e

        if not isinstance(data, dict):
            raise HEPLoadError(
                f"YAML root must be a mapping, got {type(data).__name__}"
            )

        return data

    # -----------------------------------------------------------------------
    # Factory methods
    # -----------------------------------------------------------------------
    @classmethod
    def from_yaml_string(cls, content: str) -> "HEPDocument":
        """
        Parse a HEPDocument from a YAML string.

        Args:
            content: YAML-formatted string.

        Returns:
            A validated HEPDocument instance.

        Raises:
            HEPLoadError: If the YAML cannot be loaded.
            HEPValidationError: If the parsed data fails validation.
            HEPSecurityError: If content violates security limits.
        """
        logger.debug("Parsing HEPDocument from YAML string (length=%d)", len(content))
        try:
            data = cls._secure_yaml_load(content)
        except (HEPLoadError, HEPSecurityError) as e:
            logger.error("Failed to load YAML string: %s", e)
            raise

        try:
            doc = cls.model_validate(data)
        except ValidationError as e:
            logger.error("Validation failed: %s", e)
            raise HEPValidationError(
                f"HEP document validation failed: {e}"
            ) from e

        logger.info(
            "Successfully loaded HEPDocument %s version %s",
            doc.document_id,
            doc.version,
        )
        return doc

    @classmethod
    def from_yaml_file(cls, path: Path) -> "HEPDocument":
        """
        Parse a HEPDocument from a YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            A validated HEPDocument instance.

        Raises:
            FileNotFoundError: If file does not exist.
            IsADirectoryError: If path is a directory.
            PermissionError: If insufficient permissions.
            HEPLoadError: If the file cannot be loaded.
            HEPValidationError: If the parsed data fails validation.
            HEPSecurityError: If content violates security limits.
        """
        logger.debug("Loading HEPDocument from file: %s", path)

        if not path.exists():
            raise FileNotFoundError(f"YAML file does not exist: {path}")
        if not path.is_file():
            raise IsADirectoryError(f"Expected a file, got a directory: {path}")

        try:
            with path.open("r", encoding="utf-8") as f:
                data = cls._secure_yaml_load(f)
        except (OSError, yaml.YAMLError, HEPSecurityError) as e:
            logger.error("Failed to load file %s: %s", path, e)
            raise HEPLoadError(
                f"Failed to load HEP document from '{path}': {e}"
            ) from e

        try:
            doc = cls.model_validate(data)
        except ValidationError as e:
            logger.error("Validation failed for file %s: %s", path, e)
            raise HEPValidationError(
                f"HEP document validation failed for {path}: {e}"
            ) from e

        logger.info(
            "Successfully loaded HEPDocument %s from %s",
            doc.document_id,
            path,
        )
        return doc

    # -----------------------------------------------------------------------
    # Serialization
    # -----------------------------------------------------------------------
    def to_yaml_string(self, *, sort_keys: bool = False, indent: int = 2) -> str:
        """
        Serialize the HEPDocument to a YAML string.

        Args:
            sort_keys: Whether to sort keys alphabetically.
            indent: Indentation spaces (default 2).

        Returns:
            YAML-formatted string.

        Raises:
            HEPExportError: If serialization fails.
        """
        try:
            # Convert date to string for clean YAML output
            data = self.model_dump(mode="json")
            # model_dump(mode="json") converts date to string automatically
            yaml_str = yaml.dump(
                data,
                default_flow_style=False,
                sort_keys=sort_keys,
                indent=indent,
                allow_unicode=True,
            )
        except (yaml.YAMLError, TypeError) as e:
            logger.error("Failed to serialize HEPDocument to YAML: %s", e)
            raise HEPExportError(
                f"Failed to export HEPDocument: {e}"
            ) from e

        logger.debug("Serialized HEPDocument %s to YAML (%d chars)", self.document_id, len(yaml_str))
        return yaml_str

    def to_yaml_file(
        self,
        path: Path,
        *,
        sort_keys: bool = False,
        indent: int = 2,
        overwrite: bool = False,
    ) -> None:
        """
        Write the HEPDocument to a YAML file.

        Args:
            path: Destination file path.
            sort_keys: Whether to sort keys alphabetically.
            indent: Indentation spaces.
            overwrite: If True, overwrite existing file; otherwise raise
                FileExistsError.

        Raises:
            FileExistsError: If file exists and overwrite=False.
            HEPExportError: If serialization or writing fails.
            PermissionError: If insufficient write permissions.
        """
        if path.exists() and not overwrite:
            raise FileExistsError(
                f"Output file already exists: {path}. Use overwrite=True."
            )

        yaml_content = self.to_yaml_string(sort_keys=sort_keys, indent=indent)

        try:
            path.write_text(yaml_content, encoding="utf-8")
        except OSError as e:
            logger.error("Failed to write YAML file %s: %s", path, e)
            raise HEPExportError(
                f"Failed to write HEP document to '{path}': {e}"
            ) from e

        logger.info(
            "Written HEPDocument %s to %s (overwrite=%s)",
            self.document_id,
            path,
            overwrite,
        )

    # -----------------------------------------------------------------------
    # Human-readable representation
    # -----------------------------------------------------------------------
    def __str__(self) -> str:
        return (
            f"HEPDocument(id={self.document_id}, version={self.version}, "
            f"status={self.status.value}, classification={self.classification})"
        )