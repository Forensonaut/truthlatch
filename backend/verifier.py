"""Adapter between the HTTP layer and the existing verification engine."""

from verification.engine import verify


def verify_request(request):
    """Verify a validated request and return the engine result."""
    return verify(
        expected_observation=request.expected_observation,
        evidence=[item.model_dump() for item in request.evidence],
        max_age_seconds=request.max_age_seconds,
        contradictory_observations=request.contradictory_observations,
    )
