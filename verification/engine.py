"""Deterministic evidence-based verification for TruthLatch."""

from datetime import datetime, timezone
from uuid import uuid4


def parse_time(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def verify(
    expected_observation,
    evidence,
    checked_at=None,
    max_age_seconds=3600,
    contradictory_observations=None,
):
    if not isinstance(expected_observation, str) or not expected_observation.strip():
        raise ValueError("expected_observation must be a non-empty string")
    if not isinstance(evidence, list):
        raise ValueError("evidence must be a list")
    if (
        isinstance(max_age_seconds, bool)
        or not isinstance(max_age_seconds, (int, float))
        or max_age_seconds < 0
    ):
        raise ValueError("max_age_seconds must be a non-negative number")

    now = parse_time(checked_at) if checked_at else datetime.now(timezone.utc)
    if now is None:
        raise ValueError("checked_at must be a timezone-aware ISO-8601 timestamp")

    contradictions = set(contradictory_observations or [])
    if expected_observation in contradictions:
        raise ValueError("Expected observation cannot also be contradictory")

    relevant = []
    for item in evidence:
        if not isinstance(item, dict):
            continue

        required = {
            "evidence_id", "source", "observation",
            "observed_at", "authoritative",
        }
        if not required.issubset(item):
            continue
        if not all(
            isinstance(item[key], str) and item[key].strip()
            for key in ("evidence_id", "source", "observation", "observed_at")
        ):
            continue
        if not isinstance(item["authoritative"], bool):
            continue
        if item["authoritative"] is not True:
            continue

        observed_at = parse_time(item["observed_at"])
        if observed_at is None or observed_at > now:
            continue
        if (now - observed_at).total_seconds() > max_age_seconds:
            continue
        if item["observation"] not in ({expected_observation} | contradictions):
            continue

        relevant.append({
            "evidence_id": item["evidence_id"],
            "source": item["source"],
            "observation": item["observation"],
            "observed_at": item["observed_at"],
            "authoritative": item["authoritative"],
        })

    states = {item["observation"] for item in relevant}

    if len(states) > 1:
        status = "UNKNOWN"
        explanation = "Fresh authoritative evidence conflicts."
    elif expected_observation in states:
        status = "VERIFIED"
        explanation = "Fresh authoritative evidence supports the expected state."
    elif states.intersection(contradictions):
        status = "CONTRADICTED"
        explanation = "Fresh authoritative evidence contradicts the expected state."
    else:
        status = "UNKNOWN"
        explanation = "No sufficient fresh authoritative evidence was found."

    return {
        "verification_id": str(uuid4()),
        "status": status,
        "explanation": explanation,
        "evidence": relevant,
        "checked_at": now.isoformat().replace("+00:00", "Z"),
    }
