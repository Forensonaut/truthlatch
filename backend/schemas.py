"""Request and response contracts for the TruthLatch API."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    observation: str = Field(min_length=1)
    observed_at: str = Field(min_length=1)
    authoritative: bool


class VerificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    expected_observation: str = Field(min_length=1)
    evidence: list[EvidenceItem] = Field(default_factory=list)
    max_age_seconds: float = Field(default=3600, ge=0)
    contradictory_observations: list[str] = Field(default_factory=list)


class VerificationResponse(BaseModel):
    verification_id: str
    status: Literal["VERIFIED", "CONTRADICTED", "UNKNOWN"]
    explanation: str
    evidence: list[EvidenceItem]
    checked_at: str
