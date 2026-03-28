def calc_completeness(dataset: dict) -> int:
    required_fields = [
        dataset.get("title"),
        dataset.get("description"),
        dataset.get("license"),
        dataset.get("last_updated"),
        dataset.get("source_type"),
    ]
    filled = sum(1 for item in required_fields if item not in (None, "", []))
    return round((filled / len(required_fields)) * 100)


def calc_freshness(dataset: dict) -> int:
    if not dataset.get("last_updated"):
        return 0
    return 80


def calc_accessibility(resources: list[dict]) -> int:
    if not resources:
        return 0

    good = 0
    for resource in resources:
        if resource.get("latest_http_status") == 200:
            good += 1

    return round((good / len(resources)) * 100)


def calc_format_quality(resources: list[dict]) -> int:
    if not resources:
        return 0

    formats = {(r.get("format") or "").upper() for r in resources}

    if "CSV" in formats or "JSON" in formats or "GEOJSON" in formats:
        return 100
    if "XLSX" in formats:
        return 70
    if "PDF" in formats:
        return 20
    return 10


def calc_total_score(
    completeness: int,
    freshness: int,
    accessibility: int,
    format_quality: int,
) -> int:
    return round(
        completeness * 0.4
        + freshness * 0.3
        + accessibility * 0.2
        + format_quality * 0.1
    )


def calc_rank(total_score: int) -> str:
    if total_score >= 90:
        return "A"
    if total_score >= 75:
        return "B"
    if total_score >= 50:
        return "C"
    if total_score >= 25:
        return "D"
    return "E"
