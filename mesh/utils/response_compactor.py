from datetime import date, datetime
from math import isfinite
from typing import Any, Iterable, Optional


def _compact_float(value: float, max_decimals: int) -> float:
    if not isfinite(value):
        return value
    return round(value, max_decimals)


def _compact_timestamp(value: str) -> str:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        try:
            return date.fromisoformat(value).isoformat()
        except ValueError:
            return value


def compact_response_payload(
    value: Any,
    *,
    max_float_decimals: Optional[int] = None,
    drop_keys: Optional[Iterable[str]] = None,
    date_only_keys: Optional[Iterable[str]] = None,
) -> Any:
    drop_key_set = set(drop_keys or [])
    date_only_key_set = set(date_only_keys or [])

    def _walk(item: Any, parent_key: Optional[str] = None) -> Any:
        if type(item) is dict:
            compacted = {}
            for key, child in item.items():
                if key in drop_key_set:
                    continue
                compacted[key] = _walk(child, key)
            return compacted
        if type(item) is list:
            return [_walk(child, parent_key) for child in item]
        if type(item) is float and max_float_decimals is not None:
            return _compact_float(item, max_float_decimals)
        if type(item) is str and parent_key in date_only_key_set:
            return _compact_timestamp(item)
        return item

    return _walk(value)
