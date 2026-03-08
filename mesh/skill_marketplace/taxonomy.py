"""Category and label helpers for the skill marketplace."""


def normalize_category(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip()
    if not cleaned:
        return None
    return cleaned


def normalize_labels(values: list[str] | None) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for value in values or []:
        cleaned = value.strip().lower().replace("_", "-").replace(" ", "-")
        cleaned = "-".join(part for part in cleaned.split("-") if part)
        if not cleaned:
            continue
        if cleaned in seen:
            continue
        seen.add(cleaned)
        normalized.append(cleaned)

    return normalized
