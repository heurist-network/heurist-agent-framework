# --- PROVENANCE (do not remove) --------------------------------------------
# canonical source repository : SAR-402 reference implementation
# exact source commit SHA     : 73bc7529929fdc00e0fdf09f5463338e34fc519d
# original source file path   : sar402_reference/sar402/schema.py
# date copied                 : 2026-07-31
# scope                       : verification-only Heurist adapter support
# status                      : NON-CANONICAL TEMPORARY COPY
# Canonical logic remains in the SAR-402 reference implementation at the path/commit above. Shared-core
# packaging was deferred pending actual Heurist interest or review -- this is
# a disposable local copy, not a package release. Future maintenance MUST
# diff this file against the recorded reference-implementation source commit before
# modification or any submission.
# -----------------------------------------------------------------------------
"""Schema loading and structural validation for SAR-402.

The committed schema is authoritative:
    knowledge-assets/profiles/sar-402/schema/sar-402-settlement-v0.1.schema.json

Validation backend selection:
    1. If `jsonschema` exposes a Draft 2020-12 validator, use it (authoritative).
    2. Otherwise fall back to a local structural validator that interprets the
       subset of JSON Schema this document uses (type, const, enum, required,
       properties, additionalProperties:false, pattern, $ref, allOf/if/then,
       not/const, items, minimum).

The fallback is NOT a silent skip: it actively enforces the same constraints.
`active_backend()` reports which one ran so callers and reports can be explicit
about coverage.
"""

from __future__ import annotations

import json
import re
from typing import List, Optional

from . import constants

# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------

_SCHEMA_CACHE: Optional[dict] = None


def load_schema() -> dict:
    """Load and cache the committed SAR-402 schema."""
    global _SCHEMA_CACHE
    if _SCHEMA_CACHE is None:
        with open(constants.SCHEMA_PATH, "r", encoding="utf-8") as handle:
            _SCHEMA_CACHE = json.load(handle)
        _assert_constants_match_schema(_SCHEMA_CACHE)
    return _SCHEMA_CACHE


def _assert_constants_match_schema(schema: dict) -> None:
    """Defensive: keep constants.py from drifting away from the committed schema."""
    props = schema["properties"]
    expectations = {
        "schema_id const": (props["schema_id"]["const"], constants.SCHEMA_ID),
        "profile const": (props["profile"]["const"], constants.PROFILE),
        "sar_type const": (props["sar_type"]["const"], constants.SAR_TYPE),
        "verification_point enum": (
            tuple(props["verification_point"]["enum"]),
            constants.VERIFICATION_POINTS,
        ),
        "verification_mode enum": (
            tuple(props["verification_mode"]["enum"]),
            constants.VERIFICATION_MODES,
        ),
        "payment_state enum": (
            tuple(props["payment_state"]["enum"]),
            constants.PAYMENT_STATES,
        ),
        "delivery_state enum": (
            tuple(props["delivery_state"]["enum"]),
            constants.DELIVERY_STATES,
        ),
        "settlement_state enum": (
            tuple(props["settlement_state"]["enum"]),
            constants.SETTLEMENT_STATES,
        ),
        "continuity predicates": (
            tuple(schema["$defs"]["continuity"]["required"]),
            constants.CONTINUITY_PREDICATES,
        ),
        "verdict enum": (
            tuple(schema["$defs"]["verdict"]["enum"]),
            constants.VERDICTS,
        ),
    }
    for label, (in_schema, in_constants) in expectations.items():
        if in_schema != in_constants:
            raise RuntimeError(
                f"SAR-402 constants drifted from committed schema ({label}): "
                f"schema={in_schema!r} constants={in_constants!r}"
            )


# ---------------------------------------------------------------------------
# Backend selection
# ---------------------------------------------------------------------------

def _jsonschema_2020_validator():
    """Return a jsonschema Draft 2020-12 validator class, or None if unavailable."""
    try:
        from jsonschema import Draft202012Validator  # type: ignore
    except Exception:
        return None
    return Draft202012Validator


def active_backend() -> str:
    return "jsonschema-draft2020-12" if _jsonschema_2020_validator() else "local-structural"


# ---------------------------------------------------------------------------
# Public structural validation entry point
# ---------------------------------------------------------------------------

def schema_errors(instance: dict) -> List[str]:
    """Return a list of structural schema violations (empty list == valid)."""
    schema = load_schema()
    validator_cls = _jsonschema_2020_validator()
    if validator_cls is not None:
        validator = validator_cls(schema)
        return [
            f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
            for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        ]
    errors: List[str] = []
    _LocalValidator(schema).validate(schema, instance, "<root>", errors)
    return errors


# ---------------------------------------------------------------------------
# Local structural validator (JSON Schema subset interpreter)
# ---------------------------------------------------------------------------

_TYPE_CHECKS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


class _LocalValidator:
    """Interprets the subset of JSON Schema used by the SAR-402 schema."""

    def __init__(self, root: dict):
        self.root = root

    def _resolve(self, node: dict) -> dict:
        if "$ref" in node:
            ref = node["$ref"]
            if not ref.startswith("#/"):
                raise RuntimeError(f"unsupported $ref: {ref}")
            target = self.root
            for part in ref[2:].split("/"):
                target = target[part]
            merged = dict(target)
            for key, value in node.items():
                if key != "$ref":
                    merged[key] = value
            return merged
        return node

    def matches(self, node: dict, instance) -> bool:
        probe: List[str] = []
        self.validate(node, instance, "<probe>", probe)
        return not probe

    def validate(self, node: dict, instance, path: str, errors: List[str]) -> None:
        node = self._resolve(node)

        if "const" in node:
            if instance != node["const"]:
                errors.append(f"{path}: expected const {node['const']!r}, got {instance!r}")

        if "enum" in node:
            if instance not in node["enum"]:
                errors.append(f"{path}: {instance!r} not in enum {node['enum']!r}")

        if "type" in node:
            checker = _TYPE_CHECKS.get(node["type"])
            if checker and not checker(instance):
                errors.append(f"{path}: expected type {node['type']}, got {type(instance).__name__}")
                # If the basic type is wrong, deeper checks are noise.
                return

        if "not" in node:
            sub = self._resolve(node["not"])
            if self.matches(sub, instance):
                errors.append(f"{path}: value {instance!r} is forbidden by 'not'")

        if "pattern" in node and isinstance(instance, str):
            if re.search(node["pattern"], instance) is None:
                errors.append(f"{path}: {instance!r} does not match pattern {node['pattern']!r}")

        if "minimum" in node and isinstance(instance, (int, float)) and not isinstance(instance, bool):
            if instance < node["minimum"]:
                errors.append(f"{path}: {instance} < minimum {node['minimum']}")

        if isinstance(instance, dict):
            self._validate_object(node, instance, path, errors)

        if isinstance(instance, list) and "items" in node:
            for idx, item in enumerate(instance):
                self.validate(node["items"], item, f"{path}[{idx}]", errors)

        for sub in node.get("allOf", []):
            self._validate_conditional(sub, instance, path, errors)

    def _validate_object(self, node: dict, instance: dict, path: str, errors: List[str]) -> None:
        properties = node.get("properties", {})
        for required in node.get("required", []):
            if required not in instance:
                errors.append(f"{path}: missing required property '{required}'")

        if node.get("additionalProperties", True) is False:
            allowed = set(properties)
            for key in instance:
                if key not in allowed:
                    errors.append(f"{path}: additional property '{key}' is not allowed")

        for key, value in instance.items():
            if key in properties:
                self.validate(properties[key], value, f"{path}/{key}", errors)

    def _validate_conditional(self, sub: dict, instance, path: str, errors: List[str]) -> None:
        sub = self._resolve(sub)
        if "if" in sub:
            if self.matches(sub["if"], instance):
                if "then" in sub:
                    self.validate(sub["then"], instance, path, errors)
            elif "else" in sub:
                self.validate(sub["else"], instance, path, errors)
        else:
            self.validate(sub, instance, path, errors)
